from __future__ import annotations

import os

import structlog
from dotenv import load_dotenv

_ = load_dotenv()


if os.getenv("PROD"):
    # JSON renderer for production to be fluentbit compatible
    structlog.configure(processors=[structlog.processors.JSONRenderer()])


def foo(bar: str) -> str:
    """Summary line.

    Extended description of function.

    Args:
        bar: Description of input argument.

    Returns:
        Description of return value
    """
    log = structlog.stdlib.get_logger()
    log.info("foo", key=bar)
    return bar


if __name__ == "__main__":  # pragma: no cover
    pass
