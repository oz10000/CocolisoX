from logger import get_logger

logger = get_logger("RegimeDetector")

class RegimeDetector:
    """Detecta el régimen de mercado (tendencia, rango, volatilidad)."""
    
    def __init__(self, config):
        self.config = config
    
    def detect(self, ohlcv: list) -> str:
        """
        Retorna el régimen: 'trending_up', 'trending_down', 'ranging', 'volatile'.
        Placeholder.
        """
        # Lógica placeholder
        return 'ranging'
