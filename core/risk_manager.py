from logger import get_logger

logger = get_logger("RiskManager")

class RiskManager:
    """Control de riesgo: tamaño de posición, stops, límites."""
    
    def __init__(self, config, state):
        self.config = config
        self.state = state
    
    def calculate_position_size(self, signal: dict, current_price: float) -> float:
        """Calcula cantidad a operar basado en % del capital."""
        equity = self.state.equity
        amount_usd = equity * (self.config.AMOUNT_PERCENT / 100.0)
        quantity = amount_usd / current_price
        logger.info(f"Tamaño posición calculado: {quantity} @ {current_price}")
        return quantity
    
    def check_daily_loss_limit(self) -> bool:
        """Retorna True si se ha excedido el límite diario de pérdida."""
        daily_loss_pct = (self.state.daily_pnl / self.state.equity) * 100
        if daily_loss_pct <= -self.config.MAX_DAILY_LOSS:
            logger.warning(f"Límite diario de pérdida alcanzado: {daily_loss_pct:.2f}%")
            return False  # No se puede operar
        return True
    
    def apply_stop_loss(self, position, current_price) -> bool:
        """Verifica si se debe activar stop loss."""
        if position.side == 'long':
            loss_pct = (current_price - position.entry_price) / position.entry_price * 100
            if loss_pct <= -self.config.STOP_LOSS_PCT:
                logger.info(f"Stop loss activado para {position.symbol}")
                return True
        return False
