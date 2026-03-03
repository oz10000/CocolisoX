import pandas as pd
from logger import get_logger

logger = get_logger("BacktestEngine")

class BacktestEngine:
    """Ejecuta una simulación histórica."""
    
    def __init__(self, config, signal_engine, executor, state):
        self.config = config
        self.signal_engine = signal_engine
        self.executor = executor
        self.state = state
    
    def run(self):
        logger.info("Iniciando backtest")
        # Cargar datos históricos (simulado)
        data = self._load_historical_data()
        
        for index, row in data.iterrows():
            # En cada vela, generar señal y ejecutar
            ohlcv = [row[['open','high','low','close','volume']].tolist()]  # simplificado
            orderbook = {'bids': [[row['close'], 1]], 'asks': [[row['close'], 1]]}
            signal = self.signal_engine.generate_signal(ohlcv, orderbook)
            if signal['action'] != 'hold':
                self.executor.execute_signal(signal)
        
        # Calcular métricas al final
        from .metrics import calculate_metrics
        metrics = calculate_metrics(self.state.trade_history)
        logger.info(f"Métricas finales: {metrics}")
    
    def _load_historical_data(self):
        """Carga datos desde CSV o genera datos sintéticos."""
        # Placeholder: generar datos sintéticos
        import pandas as pd
        import numpy as np
        dates = pd.date_range(start=self.config.BACKTEST_START, end=self.config.BACKTEST_END, freq='5min')
        data = pd.DataFrame(index=dates)
        data['open'] = np.random.normal(50000, 1000, len(dates))
        data['high'] = data['open'] + np.random.uniform(0, 200, len(dates))
        data['low'] = data['open'] - np.random.uniform(0, 200, len(dates))
        data['close'] = data['open'] + np.random.normal(0, 100, len(dates))
        data['volume'] = np.random.uniform(10, 100, len(dates))
        return data
