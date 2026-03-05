"""Small helpers to make navigation less obviously scripted."""

import random
import time


def human_delay(min_seconds: float = 1.5, max_seconds: float = 4.0) -> None:
    """Sleep a random amount, roughly mimicking human pause-to-read time.

    Using a fixed delay between every page/action is itself a bot signal --
    real users don't move at a constant cadence. A random interval within a
    sane range is a small, cheap improvement over `time.sleep(2)`.
    """
    time.sleep(random.uniform(min_seconds, max_seconds))


def human_type(element, text: str, min_delay: float = 0.03, max_delay: float = 0.15) -> None:
    """Type into an element one character at a time with small random gaps,
    instead of Selenium's instantaneous `send_keys(text)`.
    """
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(min_delay, max_delay))


# NOTE: delay ranges tuned to avoid bot detection while staying realistic.
