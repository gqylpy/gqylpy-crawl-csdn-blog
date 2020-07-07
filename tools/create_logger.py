import logging

from .generate_path import gen_path

from config import FE
from config import LOG_DIR
from config import DATETIME_FORMAT


def create_logger(
        log_file: str,
        name: str = 'gqylpy.log',
        level: int = logging.INFO,
        log_format: str = '[%(asctime)s] [%(filename)s line:%(lineno)d] %(levelname)s: %(message)s'
) -> 'logging object':
    log = logging.getLogger(name)
    log_format = logging.Formatter(log_format, datefmt=DATETIME_FORMAT)
    fh = logging.FileHandler(gen_path(LOG_DIR, log_file), encoding=FE)
    fh.setFormatter(log_format)
    log.addHandler(fh)
    log.setLevel(level)
    return log
