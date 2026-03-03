from dataclasses import dataclass, field
from typing import Dict, List
import time

@dataclass
class Position:
    symbol: str
    side: str  # "long" o "short"
    entry_price: float
    quantity: float
    timestamp: float = field(default_factory=time.time)

@dataclass
class Order:
    id: str
    symbol: str
    side: str
    type: str
    price: float
    quantity: float
    status: str

class GlobalState:
    """Estado global del bot: balance, posiciones, órdenes, estadísticas."""
    
    def __init__(self):
        self.equity: float = 10000.0  # capital inicial
        self.balance: Dict[str, float] = {}  # moneda -> cantidad
        self.positions: List[Position] = []
        self.open_orders: List[Order] = []
        self.trade_history: List[Dict] = []
        self.daily_pnl: float = 0.0
        self.last_update: float = time.time()
    
    def update_balance(self, balances: Dict[str, float]):
        self.balance = balances
        # Calcular equity aproximado (en USDT)
        if "USDT" in balances:
            self.equity = balances["USDT"]
        # En un bot real se calcularía con precios
    
    def add_position(self, position: Position):
        self.positions.append(position)
    
    def close_position(self, symbol: str):
        self.positions = [p for p in self.positions if p.symbol != symbol]
    
    def add_trade(self, trade: Dict):
        self.trade_history.append(trade)
        self.daily_pnl += trade.get("pnl", 0.0)
