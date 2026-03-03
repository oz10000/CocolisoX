import ccxt
from config import Config
from logger import get_logger

logger = get_logger("BybitConnector")

class BybitConnector:
    """Wrapper para la API de Bybit usando ccxt."""
    
    def __init__(self, config: Config):
        self.config = config
        self.exchange = ccxt.bybit({
            'apiKey': config.API_KEY,
            'secret': config.API_SECRET,
            'enableRateLimit': True,
        })
        
        if config.USE_TESTNET or config.MODE == Mode.LIVE_TESTNET:
            self.exchange.set_sandbox_mode(True)
            logger.info("Bybit en modo testnet")
        
        if config.HTTP_PROXY:
            self.exchange.proxies = {
                'http': config.HTTP_PROXY,
                'https': config.HTTPS_PROXY or config.HTTP_PROXY
            }
        
        self._load_markets()
    
    def _load_markets(self):
        try:
            self.exchange.load_markets()
        except Exception as e:
            logger.error(f"Error cargando markets: {e}")
    
    def fetch_balance(self):
        try:
            bal = self.exchange.fetch_balance()
            return bal['free']
        except Exception as e:
            logger.error(f"Error fetch_balance: {e}")
            return {}
    
    def fetch_positions(self):
        try:
            return self.exchange.fetch_positions()
        except Exception as e:
            logger.error(f"Error fetch_positions: {e}")
            return []
    
    def create_order(self, symbol, type, side, amount, price=None, params={}):
        try:
            return self.exchange.create_order(symbol, type, side, amount, price, params)
        except Exception as e:
            logger.error(f"Error create_order: {e}")
            raise
    
    def fetch_order_book(self, symbol, limit=10):
        try:
            return self.exchange.fetch_order_book(symbol, limit)
        except Exception as e:
            logger.error(f"Error fetch_order_book: {e}")
            return {'bids': [], 'asks': []}
    
    def fetch_ohlcv(self, symbol, timeframe, since=None, limit=None):
        try:
            return self.exchange.fetch_ohlcv(symbol, timeframe, since, limit)
        except Exception as e:
            logger.error(f"Error fetch_ohlcv: {e}")
            return []
