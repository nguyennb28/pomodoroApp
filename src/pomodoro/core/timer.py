from __future__ import annotations

import time
from dataclasses import dataclass
from enum import Enum
from typing import Callable


class SessionType(str, Enum):
    WORK = "work"
    SHORT_BREAK = "short_break"
    LONG_BREAK = "long_break"

    @property
    def display_name(self) -> str:
        match self:
            case SessionType.WORK:
                return "Focus"
            case SessionType.SHORT_BREAK:
                return "Short Break"
            case SessionType.LONG_BREAK:
                return "Long Break"


class TimerState(str, Enum):
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"


@dataclass
class TimerConfig:
    work_duration: int = 25 * 60
    short_break_duration: int = 5 * 60
    long_break_duration: int = 15 * 60
    sessions_per_cycle: int = 4


class PomodoroTimer:
    """Accurate, monotonic clock-based Pomodoro state machine."""

    def __init__(
        self,
        config: TimerConfig | None = None,
        on_tick: Callable[[float], None] | None = None,
        on_state_change: Callable[[TimerState, SessionType], None] | None = None,
        on_session_complete: Callable[[SessionType], None] | None = None,
    ) -> None:
        self.config = config or TimerConfig()
        self.on_tick = on_tick
        self.on_state_change = on_state_change
        self.on_session_complete = on_session_complete

        self.current_session: SessionType = SessionType.WORK
        self.state: TimerState = TimerState.IDLE
        self.completed_sessions_in_cycle: int = 0
        self.total_completed_sessions: int = 0

        self.duration_seconds: float = float(self._get_duration_for(self.current_session))
        self.remaining_seconds: float = self.duration_seconds
        self._last_tick_time: float | None = None

    def _get_duration_for(self, session_type: SessionType) -> int:
        match session_type:
            case SessionType.WORK:
                return self.config.work_duration
            case SessionType.SHORT_BREAK:
                return self.config.short_break_duration
            case SessionType.LONG_BREAK:
                return self.config.long_break_duration

    def _emit_state_change(self) -> None:
        if self.on_state_change:
            self.on_state_change(self.state, self.current_session)

    def _emit_tick(self) -> None:
        if self.on_tick:
            self.on_tick(self.remaining_seconds)

    def start(self, now: float | None = None) -> None:
        """Start or resume the timer."""
        if self.state == TimerState.RUNNING:
            return

        current_time = time.monotonic() if now is None else now
        self._last_tick_time = current_time
        self.state = TimerState.RUNNING
        self._emit_state_change()

    def pause(self) -> None:
        """Pause the running timer."""
        if self.state != TimerState.RUNNING:
            return

        self.state = TimerState.PAUSED
        self._last_tick_time = None
        self._emit_state_change()

    def toggle(self) -> None:
        """Toggle between start and pause."""
        if self.state == TimerState.RUNNING:
            self.pause()
        else:
            self.start()

    def reset(self) -> None:
        """Reset the current session back to full duration in idle state."""
        self.state = TimerState.IDLE
        self._last_tick_time = None
        self.duration_seconds = float(self._get_duration_for(self.current_session))
        self.remaining_seconds = self.duration_seconds
        self._emit_state_change()
        self._emit_tick()

    def skip(self) -> None:
        """Skip current session immediately to next session."""
        self._advance_to_next_session(completed=False)

    def tick(self, now: float | None = None) -> float:
        """Advance time using monotonic delta. Returns remaining seconds."""
        if self.state != TimerState.RUNNING:
            return self.remaining_seconds

        current_time = time.monotonic() if now is None else now

        if self._last_tick_time is not None:
            delta = current_time - self._last_tick_time
            if delta > 0:
                self.remaining_seconds -= delta
        self._last_tick_time = current_time

        if self.remaining_seconds <= 0:
            self.remaining_seconds = 0
            self._handle_session_finished()
        else:
            self._emit_tick()

        return self.remaining_seconds

    def _handle_session_finished(self) -> None:
        completed_session = self.current_session
        self.state = TimerState.COMPLETED
        self._last_tick_time = None
        self._emit_tick()
        self._emit_state_change()

        if self.on_session_complete:
            self.on_session_complete(completed_session)

        # Transition to next session
        self._advance_to_next_session(completed=True)

    def _advance_to_next_session(self, completed: bool) -> None:
        if self.current_session == SessionType.WORK:
            if completed:
                self.completed_sessions_in_cycle += 1
                self.total_completed_sessions += 1

            if self.completed_sessions_in_cycle >= self.config.sessions_per_cycle:
                self.current_session = SessionType.LONG_BREAK
                self.completed_sessions_in_cycle = 0
            else:
                self.current_session = SessionType.SHORT_BREAK
        else:
            # Finishing break -> start new work session
            self.current_session = SessionType.WORK

        self.state = TimerState.IDLE
        self._last_tick_time = None
        self.duration_seconds = float(self._get_duration_for(self.current_session))
        self.remaining_seconds = self.duration_seconds

        self._emit_state_change()
        self._emit_tick()

    @property
    def progress(self) -> float:
        """Returns elapsed progress as a fraction between 0.0 and 1.0."""
        if self.duration_seconds <= 0:
            return 1.0
        elapsed = self.duration_seconds - self.remaining_seconds
        return max(0.0, min(1.0, elapsed / self.duration_seconds))

    @staticmethod
    def format_time(seconds: float) -> str:
        """Format seconds into MM:SS string."""
        total_seconds = max(0, int(round(seconds)))
        minutes = total_seconds // 60
        secs = total_seconds % 60
        return f"{minutes:02d}:{secs:02d}"
