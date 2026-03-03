import logging
import sys
from pathlib import Path

def get_logger(name: str) -> logging.Logger:
    """Configura y devuelve un logger con salida a consola y archivo."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    
    logger.setLevel(logging.INFO)
    
    # Formato
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Handler consola
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    
    # Handler archivo (opcional, en GitHub Actions se guardan logs como artefacto)
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    fh = logging.FileHandler(log_dir / "trading_bot.log")
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    
    return logger
