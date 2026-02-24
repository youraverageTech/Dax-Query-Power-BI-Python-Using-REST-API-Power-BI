import logging
import os

def configure_basic_logging(level=logging.INFO, logfile=None):
    """Configure a very small logging setup: console + optional file.

    Call once at program start. Subsequent calls are no-ops.
    """
    logger = logging.getLogger()
    if logger.handlers:
        return logger

    logger.setLevel(level)

    fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")

    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    if logfile:
        os.makedirs(os.path.dirname(logfile), exist_ok=True)
        fh = logging.FileHandler(logfile, encoding="utf-8")
        fh.setLevel(level)
        fh.setFormatter(fmt)
        logger.addHandler(fh)

    return logger


def get_logger(name=None):
    """Return a named logger. Ensure `configure_basic_logging` was called first."""
    return logging.getLogger(name)
