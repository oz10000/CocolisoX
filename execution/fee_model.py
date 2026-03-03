class FeeModel:
    """Modelo de comisiones de trading."""
    
    def __init__(self, config):
        self.fee_rate = config.SIMULATION_FEE  # Ejemplo, podría ser dinámico por exchange
    
    def calculate_fee(self, amount, price):
        return amount * price * self.fee_rate
