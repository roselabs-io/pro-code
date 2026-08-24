import json
import logging
import sys

_logger = logging.getLogger("blog")
if not _logger.handlers:
    _handler = logging.StreamHandler(sys.stdout)
    _handler.setFormatter(logging.Formatter("%(message)s"))
    _logger.addHandler(_handler)
    _logger.setLevel(logging.INFO)


def log_event(code: str, **fields: object) -> None:
    _logger.info(json.dumps({"event": code, **fields}))  # doctrine: allow
