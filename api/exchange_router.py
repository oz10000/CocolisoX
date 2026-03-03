from config import Config, Mode
from .binance_connector import BinanceConnector
from .bybit_connector import BybitConnector
from .public_data_connector import PublicDataConnector
from logger import get_logger

logger = get_logger("ExchangeRouter")

class ExchangeRouter:
    """Fábrica para crear la conexión al exchange según configuración."""
    
    @staticmethod
    def get_exchange(config: Config):
        exchange_name = config.EXCHANGE
        mode = config.MODE
        
        # Si es simulación, usar un conector público o virtual, pero aquí usamos el real con modo simulado
        # Para simulación usaremos PaperEngine que internamente usa VirtualExchange, no necesitamos exchange real.
        # No obstante, para obtener datos públicos podemos usar un conector público.
        if mode == Mode.SIMULATION:
            logger.info("Modo simulación: usando conector público para datos")
            return PublicDataConnector(config)
        
        # Para backtest, no necesitamos exchange en tiempo real
        if mode == Mode.BACKTEST:
            return None  # Backtest usará datos históricos
        
        # Modo real o testnet
        if exchange_name == "binance":
            return BinanceConnector(config)
        elif exchange_name == "bybit":
            return BybitConnector(config)
        else:
            raise ValueError(f"Exchange no soportado: {exchange_name}")
