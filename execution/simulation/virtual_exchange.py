import random
import time

class VirtualExchange:
    """Simula un exchange con order book dinámico."""
    
    def __init__(self, config):
        self.config = config
        self.symbol = config.SYMBOL
        self.last_price = 50000.0  # precio inicial ficticio
    
    def fetch_order_book(self, symbol, limit=10):
        """Genera un order book simulado alrededor del último precio."""
        mid = self.last_price
        spread = mid * 0.001  # 0.1% spread
        bids = [[mid - spread * (i+1), random.randint(1, 10)] for i in range(limit)]
        asks = [[mid + spread * (i+1), random.randint(1, 10)] for i in range(limit)]
        # Actualizar precio ligeramente
        self.last_price *= (1 + random.uniform(-0.001, 0.001))
        return {'bids': bids, 'asks': asks}
    
    def fetch_ohlcv(self, symbol, timeframe, since=None, limit=None):
        """Genera velas simuladas."""
        ohlcv = []
        for i in range(limit or 100):
            ts = int(time.time() * 1000) - i * 60000  # cada minuto
            o = self.last_price
            h = o * (1 + random.uniform(0, 0.002))
            l = o * (1 - random.uniform(0, 0.002))
            c = o * (1 + random.uniform(-0.001, 0.001))
            v = random.randint(100, 1000)
            ohlcv.append([ts, o, h, l, c, v])
            self.last_price = c
        return ohlcv[::-1]
