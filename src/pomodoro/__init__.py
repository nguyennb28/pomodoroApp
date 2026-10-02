"""Pomodoro - Minimalist desktop focus timer."""

from pomodoro.core.timer import PomodoroTimer, SessionType, TimerConfig, TimerState
from pomodoro.main import main

__version__ = "0.1.0"

__all__ = [
    "main",
    "PomodoroTimer",
    "SessionType",
    "TimerConfig",
    "TimerState",
    "__version__",
]
