import logging
import sys

_LEVEL_PREFIX = {
    logging.DEBUG:    "DBG",
    logging.INFO:     " + ",
    logging.WARNING:  " ! ",
    logging.ERROR:    " x ",
    logging.CRITICAL: "!!!",
}


class LinuityFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        if getattr(record, "separator", False):
            return "\n" + "─" * 52 + "\n"
        parts = record.name.split(".")
        record.short_name = parts[-1]
        record.level_prefix = _LEVEL_PREFIX.get(record.levelno, "   ")
        return super().format(record)


def setup_daemon_logging() -> None:
    fmt = "%(asctime)s  [%(level_prefix)s]  %(short_name)-20s %(message)s"
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(LinuityFormatter(fmt=fmt, datefmt="%H:%M:%S"))
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.addHandler(handler)


def setup_cli_logging() -> None:
    fmt = "[%(level_prefix)s]  %(message)s"
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(LinuityFormatter(fmt=fmt))
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.addHandler(handler)


def log_separator(logger: logging.Logger) -> None:
    logger.info("", extra={"separator": True})
