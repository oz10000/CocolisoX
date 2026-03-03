from logger import get_logger

logger = get_logger("LiveTrader")

class LiveTrader:
    """Ejecuta un ciclo de trading en vivo (una iteración)."""
    
    def __init__(self, config, exchange, signal_engine, executor, risk_manager, state):
        self.config = config
        self.exchange = exchange
        self.signal_engine = signal_engine
        self.executor = executor
        self.risk_manager = risk_manager
        self.state = state
    
    def run_once(self):
        """Una pasada: obtener datos, generar señal, ejecutar."""
        logger.info("Ejecutando ciclo de trading")
        
        symbol = self.config.SYMBOL
        timeframe = self.config.TIMEFRAME
        
        # Obtener datos de mercado
        ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=100)
        orderbook = self.exchange.fetch_order_book(symbol)
        
        if not ohlcv or not orderbook:
            logger.error("No se pudieron obtener datos de mercado")
            return
        
        # Generar señal
        signal = self.signal_engine.generate_signal(ohlcv, orderbook)
        
        # Ejecutar si procede
        if signal['action'] != 'hold':
            self.executor.execute_signal(signal)
        
        # Actualizar estado con balance
        balance = self.exchange.fetch_balance()
        self.state.update_balance(balance)
        
        logger.info(f"Ciclo completado. Equity: {self.state.equity}")
