import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

log_name = 'logs/bot.log'
Path(log_name).parent.mkdir(parents=True, exist_ok=True)

handler = TimedRotatingFileHandler(
    log_name, when='d', interval=1, backupCount=9
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[handler]
)
