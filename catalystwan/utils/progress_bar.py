# Copyright 2024 Cisco Systems, Inc. and its affiliates

import sys
import time
from typing import List, Optional, TextIO

BAR_TEMPLATE = "%s[%s%s] %i/%i - %s\r"
BAR_FILLED_CHAR = "="
BAR_EMPTY_CHAR = " "
ETA_INTERVAL = 1
ETA_SMA_WINDOW = 9


class ProgressBar:
    """Lightweight, self-contained terminal progress bar replacing the unmaintained clint library."""

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.done()
        return False

    def __init__(
        self,
        label: str = "",
        width: int = 32,
        hide: Optional[bool] = None,
        empty_char: str = BAR_EMPTY_CHAR,
        filled_char: str = BAR_FILLED_CHAR,
        expected_size: Optional[int] = None,
        every: int = 1,
        stream: Optional[TextIO] = None,
    ):
        self.label = label
        self.width = width
        self.stream = stream or sys.stderr
        if hide is None:
            try:
                self.hide = not self.stream.isatty()
            except AttributeError:
                self.hide = True
        else:
            self.hide = hide
        self.empty_char = empty_char
        self.filled_char = filled_char
        self.expected_size = expected_size
        self.every = every
        self.start = time.time()
        self.ittimes: List[float] = []
        self.eta: float = 0.0
        self.etadelta = time.time()
        self.etadisp = self.format_time(self.eta)
        self.last_progress = 0
        if self.expected_size:
            self.show(0)

    def show(self, progress: int, count: Optional[int] = None):
        if count is not None:
            self.expected_size = count
        if self.expected_size is None:
            raise ValueError("expected_size not initialized")
        self.last_progress = progress
        if (time.time() - self.etadelta) > ETA_INTERVAL:
            self.etadelta = time.time()
            self.ittimes = self.ittimes[-ETA_SMA_WINDOW:] + [-(self.start - time.time()) / (progress + 1)]
            self.eta = sum(self.ittimes) / float(len(self.ittimes)) * (self.expected_size - progress)
            self.etadisp = self.format_time(self.eta)
        if self.expected_size > 0:
            x = int(self.width * progress / self.expected_size)
        else:
            x = self.width
        if not self.hide:
            if ((progress % self.every) == 0) or (progress == self.expected_size):
                self.stream.write(
                    BAR_TEMPLATE
                    % (
                        self.label,
                        self.filled_char * x,
                        self.empty_char * (self.width - x),
                        progress,
                        self.expected_size,
                        self.etadisp,
                    )
                )
                self.stream.flush()

    def done(self):
        self.elapsed = time.time() - self.start
        elapsed_disp = self.format_time(self.elapsed)
        if not self.hide:
            self.stream.write(
                BAR_TEMPLATE
                % (
                    self.label,
                    self.filled_char * self.width,
                    self.empty_char * 0,
                    self.last_progress,
                    self.expected_size or self.last_progress,
                    elapsed_disp,
                )
            )
            self.stream.write("\n")
            self.stream.flush()

    @staticmethod
    def format_time(seconds: float) -> str:
        return time.strftime("%H:%M:%S", time.gmtime(max(0.0, seconds)))
