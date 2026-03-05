from logger import get_logger

logger = get_logger("SignalEngine")


class SignalEngine:
    """
    Motor de generación de señales de trading.
    Produce señales BUY / SELL / HOLD basadas en medias móviles.
    """

    def __init__(self, config, regime_detector):
        self.config = config
        self.regime_detector = regime_detector

    def generate_signal(self, candles):
        """
        candles formato ccxt:
        [timestamp, open, high, low, close, volume]
        """

        if not candles or len(candles) < 20:
            logger.debug("No hay suficientes datos para generar señal")
            return None

        closes = [c[4] for c in candles]

        sma_fast = sum(closes[-5:]) / 5
        sma_slow = sum(closes[-20:]) / 20

        regime = None
        try:
            regime = self.regime_detector.detect_regime(candles)
        except Exception:
            pass

        if sma_fast > sma_slow:
            signal = "BUY"
        elif sma_fast < sma_slow:
            signal = "SELL"
        else:
            signal = "HOLD"

        logger.info(
            f"Signal={signal} | SMA_FAST={round(sma_fast,4)} | SMA_SLOW={round(sma_slow,4)} | REGIME={regime}"
        )

        return signal
