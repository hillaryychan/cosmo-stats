import signal
import sys
from types import FrameType
from typing import NoReturn


def sigint_handler(_signum: int, _frame: FrameType | None) -> NoReturn:
    sys.exit()


def register_signal_handlers() -> None:
    signal.signal(signal.SIGINT, sigint_handler)
