from pomodoro.core.timer import (
    PomodoroTimer,
    SessionType,
    TimerConfig,
    TimerState,
)


def test_timer_initialization():
    config = TimerConfig(work_duration=1500, short_break_duration=300, long_break_duration=900)
    timer = PomodoroTimer(config=config)

    assert timer.state == TimerState.IDLE
    assert timer.current_session == SessionType.WORK
    assert timer.remaining_seconds == 1500
    assert timer.completed_sessions_in_cycle == 0
    assert timer.total_completed_sessions == 0
    assert PomodoroTimer.format_time(1500) == "25:00"


def test_timer_start_pause_reset():
    timer = PomodoroTimer(config=TimerConfig(work_duration=100))

    timer.start(now=100.0)
    assert timer.state == TimerState.RUNNING

    # Tick 10 seconds later
    remaining = timer.tick(now=110.0)
    assert remaining == 90.0
    assert timer.progress == 0.1

    timer.pause()
    assert timer.state == TimerState.PAUSED

    # Tick while paused should not advance
    timer.tick(now=120.0)
    assert timer.remaining_seconds == 90.0

    timer.reset()
    assert timer.state == TimerState.IDLE
    assert timer.remaining_seconds == 100.0
    assert timer.progress == 0.0


def test_timer_session_transition_to_short_break():
    completed = []
    timer = PomodoroTimer(
        config=TimerConfig(work_duration=10, short_break_duration=5),
        on_session_complete=lambda s: completed.append(s),
    )

    timer.start(now=0.0)
    timer.tick(now=10.0)  # Finishes work session

    assert completed == [SessionType.WORK]
    assert timer.completed_sessions_in_cycle == 1
    assert timer.total_completed_sessions == 1
    assert timer.current_session == SessionType.SHORT_BREAK
    assert timer.remaining_seconds == 5.0
    assert timer.state == TimerState.IDLE


def test_timer_cycle_to_long_break():
    completed = []
    timer = PomodoroTimer(
        config=TimerConfig(
            work_duration=5,
            short_break_duration=2,
            long_break_duration=10,
            sessions_per_cycle=2,  # cycle of 2 for fast test
        ),
        on_session_complete=lambda s: completed.append(s),
    )

    # Session 1: Work
    timer.start(now=0.0)
    timer.tick(now=5.0)
    assert timer.current_session == SessionType.SHORT_BREAK

    # Short break finishes
    timer.start(now=5.0)
    timer.tick(now=7.0)
    assert timer.current_session == SessionType.WORK
    assert timer.completed_sessions_in_cycle == 1

    # Session 2: Work (reaches 2 sessions -> triggers long break)
    timer.start(now=7.0)
    timer.tick(now=12.0)
    assert timer.current_session == SessionType.LONG_BREAK
    assert timer.remaining_seconds == 10.0
    assert timer.completed_sessions_in_cycle == 0


def test_timer_skip():
    timer = PomodoroTimer(config=TimerConfig(work_duration=100, short_break_duration=50))
    timer.start()
    timer.skip()

    assert timer.current_session == SessionType.SHORT_BREAK
    assert timer.remaining_seconds == 50.0
    assert timer.completed_sessions_in_cycle == 0
    assert timer.state == TimerState.IDLE
