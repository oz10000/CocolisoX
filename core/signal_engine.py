import ccxt
from config import Config
from logger import get_logger

logger = get_logger("PublicDataConnector")

class PublicDataConnector:
    """Conector de solo lectura para datos públicos, sin API keys."""
    
    def __init__(self, config: Config):
        self.config = config
        exchange_class = getattr(ccxt, config.EXCHANGE)
        self.exchange = exchange_class({
            'enableRateLimit': True,
        })
        
        if config.HTTP_PROXY:
            self.exchange.proxies = {
                'http': config.HTTP_PROXY,
                'https': config.HTTPS_PROXY or config.HTTP_PROXY
            }
    
    def fetch_order_book(self, symbol, limit=10):
        try:
            return self.exchange.fetch_order_book(symbol, limit)
        except Exception as e:
            logger.error(f"Error fetch_order_book público: {e}")
            return {'bids': [], 'asks': []}
    
    def fetch_ohlcv(self, symbol, timeframe, since=None, limit=None):
        try:
            return self.exchange.fetch_ohlcv(symbol, timeframe, since, limit)
        except Exception as e:
            logger.error(f"Error fetch_ohlcv público: {e}")
            return []
    
    # Métodos que requieren autenticación no están implementados
    def fetch_balance(self):
        logger.warning("fetch_balance no disponible en modo público")
        return {}
    
    def fetch_positions(self):
        return []
    
    def create_order(self, *args, **kwargs):
        raise NotImplementedError("No se pueden crear órdenes en modo público")
