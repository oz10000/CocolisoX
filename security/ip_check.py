import requests
from logger import get_logger

logger = get_logger("IPCheck")

def get_public_ip() -> str:
    """Obtiene la IP pública del runner."""
    try:
        response = requests.get('https://api.ipify.org', timeout=5)
        if response.status_code == 200:
            return response.text.strip()
    except Exception as e:
        logger.error(f"No se pudo obtener IP pública: {e}")
    return ""

def check_ip_blocked() -> bool:
    """Verifica si la IP actual está en la lista de bloqueadas (simulado)."""
    from config import Config
    config = Config.from_env()
    
    ip = get_public_ip()
    if not ip:
        logger.warning("No se pudo determinar IP, se asume no bloqueada")
        return False
    
    logger.info(f"IP pública detectada: {ip}")
    
    # Lista de IPs bloqueadas (simulada, vendría de config o archivo)
    blocked = config.BLOCKED_IPS
    if ip in blocked:
        logger.warning(f"IP {ip} está en lista de bloqueadas")
        return True
    
    # Aquí se podría consultar algún servicio externo o lista mantenida
    return False
