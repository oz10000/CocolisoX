from logger import get_logger
from .virtual_exchange import VirtualExchange
from execution.fee_model import FeeModel
from execution.slippage_model import SlippageModel

logger = get_logger("PaperEngine")

class PaperEngine:
    """Motor de simulación que imita un exchange sin dinero real."""
    
    def __init__(self, config, state):
        self.config = config
        self.state = state
        self.virtual_exchange = VirtualExchange(config)
        self.fee_model = FeeModel(config)
        self.slippage_model = SlippageModel(config)
    
    def execute_signal(self, signal: dict):
        """Ejecuta una señal en el entorno simulado."""
        action = signal['action']
        if action == 'hold':
            return
        
        symbol = self.config.SYMBOL
        # Obtener precio del libro simulado
        ob = self.virtual_exchange.fetch_order_book(symbol)
        if not ob['asks'] or not ob['bids']:
            logger.warning("Orden book vacío")
            return
        
        price = ob['asks'][0][0] if action == 'buy' else ob['bids'][0][0]
        
        # Calcular cantidad (simplificado)
        quantity = (self.state.equity * self.config.AMOUNT_PERCENT / 100) / price
        
        # Aplicar slippage
        executed_price = self.slippage_model.apply(price, action, quantity)
        
        # Simular ejecución
        fee = self.fee_model.calculate_fee(quantity, executed_price)
        cost = quantity * executed_price + fee
        
        if action == 'buy':
            self.state.equity -= cost
            self.state.add_position({
                'symbol': symbol,
                'side': 'long',
                'entry_price': executed_price,
                'quantity': quantity
            })
        else:  # sell
            self.state.equity += cost
            self.state.close_position(symbol)
        
        logger.info(f"Orden simulada: {action} {quantity} @ {executed_price}")
