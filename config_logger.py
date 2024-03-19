import logging
from logging.handlers import TimedRotatingFileHandler

handler = TimedRotatingFileHandler('bot_log.log', when='d', interval=1)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[handler]
)
