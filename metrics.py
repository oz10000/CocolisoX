import numpy as np

def calculate_metrics(trades):
    """Calcula métricas de rendimiento a partir de la lista de trades."""
    if not trades:
        return {}
    
    pnls = [t.get('pnl', 0) for t in trades]
    total_pnl = sum(pnls)
    win_trades = [p for p in pnls if p > 0]
    loss_trades = [p for p in pnls if p < 0]
    win_rate = len(win_trades) / len(trades) if trades else 0
    profit_factor = abs(sum(win_trades) / sum(loss_trades)) if sum(loss_trades) != 0 else float('inf')
    
    # Drawdown (simplificado, necesitaría equity curve)
    max_drawdown = 0  # placeholder
    
    # Sharpe (necesita retornos diarios)
    sharpe = 0
    
    return {
        'total_trades': len(trades),
        'total_pnl': total_pnl,
        'win_rate': win_rate,
        'profit_factor': profit_factor,
        'max_drawdown': max_drawdown,
        'sharpe': sharpe
    }
