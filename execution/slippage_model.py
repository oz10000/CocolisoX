import random

class SlippageModel:
    """Modelo simple de slippage."""
    
    def __init__(self, config):
        self.slippage = config.SIMULATION_SLIPPAGE
    
    def apply(self, price, side, quantity):
        """Retorna precio ejecutado con slippage aleatorio."""
        if side == 'buy':
            return price * (1 + random.uniform(0, self.slippage))
        else:
            return price * (1 - random.uniform(0, self.slippage))
