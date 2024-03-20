import logging
from logging.handlers import TimedRotatingFileHandler

handler = TimedRotatingFileHandler(
    'bot.log', when='d', interval=1, backupCount=9
)

logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[handler]
)
