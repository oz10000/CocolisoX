import os
from enum import Enum

class Mode(Enum):
    BACKTEST = "BACKTEST"
    SIMULATION = "SIMULATION"
    LIVE_TESTNET = "LIVE_TESTNET"
    LIVE_MAINNET = "LIVE_MAINNET"

class Config:
    """Configuración centralizada desde variables de entorno."""
    
    def __init__(self):
        self.MODE = Mode(os.getenv("TRADING_MODE", "SIMULATION"))
        
        # Exchange seleccionado
        self.EXCHANGE = os.getenv("EXCHANGE", "binance").lower()  # binance, bybit
        
        # API Keys (pueden estar vacías)
        self.API_KEY = os.getenv("API_KEY", "")
        self.API_SECRET = os.getenv("API_SECRET", "")
        self.API_PASSPHRASE = os.getenv("API_PASSPHRASE", "")  # para algunos exchanges
        
        # Testnet flag
        self.USE_TESTNET = os.getenv("USE_TESTNET", "false").lower() == "true"
        
        # Proxy / VPN
        self.HTTP_PROXY = os.getenv("HTTP_PROXY", "")
        self.HTTPS_PROXY = os.getenv("HTTPS_PROXY", "")
        
        # Parámetros de trading
        self.SYMBOL = os.getenv("SYMBOL", "BTC/USDT")
        self.TIMEFRAME = os.getenv("TIMEFRAME", "5m")
        self.AMOUNT_PERCENT = float(os.getenv("AMOUNT_PERCENT", "10"))  # % de equity por orden
        self.LEVERAGE = int(os.getenv("LEVERAGE", "1"))
        self.STOP_LOSS_PCT = float(os.getenv("STOP_LOSS_PCT", "2"))
        self.TAKE_PROFIT_PCT = float(os.getenv("TAKE_PROFIT_PCT", "0"))
        self.MAX_DAILY_LOSS = float(os.getenv("MAX_DAILY_LOSS", "5"))  # % del capital
        
        # Backtest
        self.BACKTEST_START = os.getenv("BACKTEST_START", "2025-01-01")
        self.BACKTEST_END = os.getenv("BACKTEST_END", "2025-02-01")
        self.BACKTEST_DATA_PATH = os.getenv("BACKTEST_DATA_PATH", "data/")
        
        # Simulación
        self.SIMULATION_SLIPPAGE = float(os.getenv("SIMULATION_SLIPPAGE", "0.001"))  # 0.1%
        self.SIMULATION_FEE = float(os.getenv("SIMULATION_FEE", "0.001"))  # 0.1%
        
        # Lista de IPs bloqueadas (simulada)
        self.BLOCKED_IPS = os.getenv("BLOCKED_IPS", "").split(",") if os.getenv("BLOCKED_IPS") else []
        
    @classmethod
    def from_env(cls):
        return cls()
