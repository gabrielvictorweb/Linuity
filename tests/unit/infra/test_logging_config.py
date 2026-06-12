import logging

from linuity.infra.logging_config import setup_cli_logging, setup_daemon_logging


def test_setup_daemon_logging_adds_handler():
    root = logging.getLogger()
    before = len(root.handlers)
    setup_daemon_logging()
    assert len(root.handlers) > before
    root.handlers = root.handlers[:before]


def test_setup_cli_logging_adds_handler():
    root = logging.getLogger()
    before = len(root.handlers)
    setup_cli_logging()
    assert len(root.handlers) > before
    root.handlers = root.handlers[:before]
