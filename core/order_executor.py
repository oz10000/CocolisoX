from typing import Optional
from logger import get_logger
from .fee_model import FeeModel
from .slippage_model import SlippageModel

logger = get_logger("OrderExecutor")

class OrderExecutor:
    """Ejecuta órdenes reales en el exchange, aplicando slippage y fees."""
    
    def __init__(self, config, exchange, state, risk_manager):
        self.config = config
        self.exchange = exchange
        self.state = state
        self.risk_manager = risk_manager
        self.fee_model = FeeModel(config)
        self.slippage_model = SlippageModel(config)
    
    def execute_signal(self, signal: dict):
        """Ejecuta una señal de trading."""
        if not self.risk_manager.check_daily_loss_limit():
            logger.warning("Límite diario de pérdida excedido, no se ejecuta orden")
            return
        
        action = signal['action']
        if action == 'hold':
            return
        
        symbol = self.config.SYMBOL
        price = signal.get('price', 0)
        if price == 0:
            # Obtener precio actual del orderbook
            ob = self.exchange.fetch_order_book(symbol)
            price = ob['asks'][0][0] if action == 'buy' else ob['bids'][0][0]
        
        # Calcular cantidad
        quantity = self.risk_manager.calculate_position_size(signal, price)
        if quantity <= 0:
            logger.warning("Cantidad calculada <= 0, no se ejecuta")
            return
        
        # Aplicar slippage estimado
        executed_price = self.slippage_model.apply(price, action, quantity)
        
        # Enviar orden
        try:
            order = self.exchange.create_order(
                symbol=symbol,
                type='market',  # o limit según estrategia
                side=action,
                amount=quantity
            )
            logger.info(f"Orden ejecutada: {order}")
            
            # Actualizar estado (simplificado)
            self.state.add_trade({
                'symbol': symbol,
                'side': action,
                'price': executed_price,
                'quantity': quantity,
                'timestamp': order.get('timestamp')
            })
            
        except Exception as e:
            logger.error(f"Error ejecutando orden: {e}")
