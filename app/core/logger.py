import sys
from loguru import logger

logger.remove()

LOG_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
    "<level>{message}</level>"
)


logger.add(
    sys.stdout,
    format = LOG_FORMAT,
    level= "INFO"
    )

logger.add(
    "logs/app.log", 
    rotation="5 MB",
    level = "DEBUG"
)

__all__ = ["logger"]
