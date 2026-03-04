#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict


# ==========================================================
# ENUMS
# ==========================================================

class Direction(Enum):
    LONG = 1
    SHORT = -1


# ==========================================================
# TRADE STRUCTURE
# ==========================================================

@dataclass
class Trade:
    id: int
    symbol: str
    direction: Direction
    entry_time: pd.Timestamp
    entry_price: float
    size: float
    stop_loss: float
    risk_points: float

    highest_price: float = field(init=False)
    lowest_price: float = field(init=False)
    trailing_active: bool = False

    exit_time: Optional[pd.Timestamp] = None
    exit_price: Optional[float] = None

    def __post_init__(self):
        self.highest_price = self.entry_price
        self.lowest_price = self.entry_price

    @property
    def is_closed(self):
        return self.exit_time is not None

    @property
    def pnl(self):
        if not self.is_closed:
            return 0.0
        if self.direction == Direction.LONG:
            return (self.exit_price - self.entry_price) * self.size
        else:
            return (self.entry_price - self.exit_price) * self.size

    @property
    def R(self):
        if not self.is_closed:
            return None
        if self.direction == Direction.LONG:
            return (self.exit_price - self.entry_price) / self.risk_points
        else:
            return (self.entry_price - self.exit_price) / self.risk_points

    @property
    def risk_amount(self):
        return self.size * self.risk_points


# ==========================================================
# TRAILING ENGINE
# ==========================================================

class ValidatedTrailingEngine:

    def __init__(self, config: Dict):

        self.initial_capital = config["initial_capital"]
        self.cash = self.initial_capital

        self.risk_per_trade = config["risk_per_trade"]
        self.max_total_risk = config.get("max_total_risk", 0.05)

        self.sl_atr_mult = config["sl_atr_mult"]
        self.trailing_mult = config["trailing_distance_mult"]
        self.trailing_activation_R = config.get("trailing_activation_R", 1.0)

        self.open_trades: List[Trade] = []
        self.closed_trades: List[Trade] = []
        self.next_id = 0

        self.equity_curve = []

    # ------------------------------------------------------

    def _total_open_risk(self):
        return sum(t.risk_amount for t in self.open_trades)

    # ------------------------------------------------------

    def open_trade(self, symbol, timestamp, entry_price, direction, atr):

        if atr is None or np.isnan(atr) or atr <= 0:
            return None

        if direction == Direction.LONG:
            stop = entry_price - self.sl_atr_mult * atr
            risk_points = entry_price - stop
        else:
            stop = entry_price + self.sl_atr_mult * atr
            risk_points = stop - entry_price

        if risk_points <= 0:
            return None

        risk_amount = self.cash * self.risk_per_trade

        if self._total_open_risk() + risk_amount > self.cash * self.max_total_risk:
            return None

        size = risk_amount / risk_points

        trade = Trade(
            id=self.next_id,
            symbol=symbol,
            direction=direction,
            entry_time=timestamp,
            entry_price=entry_price,
            size=size,
            stop_loss=stop,
            risk_points=risk_points
        )

        self.open_trades.append(trade)
        self.next_id += 1
        return trade.id

    # ------------------------------------------------------

    def update_bar(self, symbol, timestamp, high, low, close, atr):

        to_close = []

        for trade in self.open_trades:

            if trade.symbol != symbol:
                continue

            if trade.direction == Direction.LONG:

                trade.highest_price = max(trade.highest_price, high)

                if not trade.trailing_active:
                    if high >= trade.entry_price + self.trailing_activation_R * trade.risk_points:
                        trade.trailing_active = True

                if trade.trailing_active:
                    new_stop = trade.highest_price - self.trailing_mult * atr
                    trade.stop_loss = max(trade.stop_loss, new_stop)

                if low <= trade.stop_loss:
                    self._close_trade(trade, timestamp, trade.stop_loss)
                    to_close.append(trade)

            else:

                trade.lowest_price = min(trade.lowest_price, low)

                if not trade.trailing_active:
                    if low <= trade.entry_price - self.trailing_activation_R * trade.risk_points:
                        trade.trailing_active = True

                if trade.trailing_active:
                    new_stop = trade.lowest_price + self.trailing_mult * atr
                    trade.stop_loss = min(trade.stop_loss, new_stop)

                if high >= trade.stop_loss:
                    self._close_trade(trade, timestamp, trade.stop_loss)
                    to_close.append(trade)

        for t in to_close:
            self.open_trades.remove(t)

        # Mark-to-market
        unrealized = 0.0
        for t in self.open_trades:
            if t.direction == Direction.LONG:
                unrealized += (close - t.entry_price) * t.size
            else:
                unrealized += (t.entry_price - close) * t.size

        equity = self.cash + unrealized
        self.equity_curve.append((timestamp, equity))

    # ------------------------------------------------------

    def _close_trade(self, trade, timestamp, exit_price):

        pnl = trade.pnl if trade.is_closed else (
            (exit_price - trade.entry_price) * trade.size
            if trade.direction == Direction.LONG
            else (trade.entry_price - exit_price) * trade.size
        )

        self.cash += pnl
        trade.exit_time = timestamp
        trade.exit_price = exit_price
        self.closed_trades.append(trade)

    # ------------------------------------------------------

    def results(self):

        if not self.closed_trades:
            return {"final_equity": self.cash}

        Rs = np.array([t.R for t in self.closed_trades if t.R is not None])

        wins = Rs[Rs > 0]
        losses = Rs[Rs <= 0]

        win_rate = len(wins) / len(Rs) if len(Rs) > 0 else 0
        avg_win = np.mean(wins) if len(wins) > 0 else 0
        avg_loss = abs(np.mean(losses)) if len(losses) > 0 else 0

        expectancy = win_rate * avg_win - (1 - win_rate) * avg_loss

        profit_factor = (
            np.sum(wins) / abs(np.sum(losses))
            if len(losses) > 0 else np.inf
        )

        equity_series = pd.Series(
            [v for _, v in self.equity_curve],
            index=[t for t, _ in self.equity_curve]
        )

        rolling_max = equity_series.cummax()
        drawdown = (equity_series - rolling_max) / rolling_max * 100

        return {
            "final_equity": self.cash,
            "total_trades": len(Rs),
            "win_rate": win_rate,
            "avg_win_R": avg_win,
            "avg_loss_R": avg_loss,
            "expectancy_R": expectancy,
            "profit_factor": profit_factor,
            "max_drawdown_%": drawdown.min()
        }
