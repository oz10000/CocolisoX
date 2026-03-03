import os
import requests
from logger import get_logger

logger = get_logger("VPNGuard")

def configure_proxy_from_env():
    """Configura proxies para requests y otras librerías desde variables de entorno."""
    http_proxy = os.getenv("HTTP_PROXY") or os.getenv("http_proxy")
    https_proxy = os.getenv("HTTPS_PROXY") or os.getenv("https_proxy")
    
    if http_proxy or https_proxy:
        proxies = {}
        if http_proxy:
            proxies['http'] = http_proxy
        if https_proxy:
            proxies['https'] = https_proxy
        
        # Configurar para requests
        session = requests.Session()
        session.proxies.update(proxies)
        # Reemplazar la sesión por defecto (opcional)
        # requests.sessions.default_session = lambda: session
        
        # Configurar variables de entorno para otras librerías (como ccxt)
        if http_proxy:
            os.environ['HTTP_PROXY'] = http_proxy
        if https_proxy:
            os.environ['HTTPS_PROXY'] = https_proxy
        
        logger.info(f"Proxy configurado: HTTP={http_proxy}, HTTPS={https_proxy}")
    else:
        logger.info("No se configuró proxy")
