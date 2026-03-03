#!/usr/bin/env python3
"""
Punto de entrada principal del Trading Engine Bot.
Detecta el modo de ejecución, configura los componentes y ejecuta el ciclo correspondiente.
"""
import os
import sys
import time
from config import Config, Mode
from logger import get_logger
from state import GlobalState
from api.exchange_router import ExchangeRouter
from core.signal_engine import SignalEngine
from core.regime_detector import RegimeDetector
from core.risk_manager import RiskManager
from execution.order_executor import OrderExecutor
from live.live_trader import LiveTrader
from simulation.paper_engine import PaperEngine
from backtest.backtest_engine import BacktestEngine
from security.ip_check import check_ip_blocked
from security.vpn_guard import configure_proxy_from_env

logger = get_logger("Main")

def main():
    logger.info("Iniciando Trading Engine Bot")
    
    # 1. Cargar configuración
    config = Config.from_env()
    logger.info(f"Modo seleccionado: {config.MODE.value}")
    
    # 2. Configurar proxy si existe
    configure_proxy_from_env()
    
    # 3. Verificar IP si estamos en modo real/testnet
    if config.MODE in (Mode.LIVE_MAINNET, Mode.LIVE_TESTNET):
        if check_ip_blocked():
            logger.error("IP bloqueada por el exchange. Cambiando a modo SIMULATION")
            config.MODE = Mode.SIMULATION
            # Forzar uso de simulación
            os.environ["TRADING_MODE"] = "SIMULATION"
    
    # 4. Inicializar estado global
    state = GlobalState()
    
    # 5. Crear conexión a exchange según modo
    exchange = ExchangeRouter.get_exchange(config)
    
    # 6. Inicializar módulos core
    regime_detector = RegimeDetector(config)
    signal_engine = SignalEngine(config, regime_detector)
    risk_manager = RiskManager(config, state)
    
    # 7. Inicializar ejecutor de órdenes (real o simulado)
    if config.MODE == Mode.SIMULATION:
        executor = PaperEngine(config, state)
    else:
        executor = OrderExecutor(config, exchange, state, risk_manager)
    
    # 8. Ejecutar según modo
    if config.MODE == Mode.BACKTEST:
        engine = BacktestEngine(config, signal_engine, executor, state)
        engine.run()
    else:
        # Live / Simulation / Testnet: ejecutar un ciclo de trading
        trader = LiveTrader(config, exchange, signal_engine, executor, risk_manager, state)
        trader.run_once()  # Una iteración para GitHub Actions
    
    logger.info("Bot finalizado correctamente")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.exception("Error fatal")
        sys.exit(1)
