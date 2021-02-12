import logging

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from logging import LogRecord  # noqa

    from clikit.api.io import IO  # noqa


class IOHandler(logging.Handler):
    def __init__(self, io):  # type: ("IO") -> None
        self._io = io

        super().__init__()

    def emit(self, record):  # type: ("LogRecord") -> None
        try:
            msg = self.format(record)
            level = record.levelname.lower()
            err = level in ("warning", "error", "exception", "critical")
            if err:
                self._io.error_line(msg)
            else:
                self._io.write_line(msg)
        except Exception:
            self.handleError(record)
