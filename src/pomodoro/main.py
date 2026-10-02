from __future__ import annotations

import argparse
import signal
import sys
from PyQt6.QtWidgets import QApplication

from pomodoro.core.db import Database
from pomodoro.core.notifier import Notifier
from pomodoro.core.sound import SoundManager
from pomodoro.core.timer import TimerConfig
from pomodoro.ui.window import PomodoroWindow


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Pomodoro: Minimalist desktop focus timer for Ubuntu GNOME."
    )
    parser.add_argument(
        "-w",
        "--work",
        type=int,
        default=None,
        help="Focus work duration in minutes",
    )
    parser.add_argument(
        "-b",
        "--break",
        dest="short_break",
        type=int,
        default=None,
        help="Short break duration in minutes",
    )
    parser.add_argument(
        "-l",
        "--long-break",
        type=int,
        default=None,
        help="Long break duration in minutes",
    )
    parser.add_argument(
        "-c",
        "--cycles",
        type=int,
        default=None,
        help="Work sessions per long break cycle",
    )
    return parser.parse_args()


def main() -> None:
    # Allow terminal Ctrl+C to terminate cleanly
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    args = parse_args()
    db = Database()

    # Load config from database first, then override with CLI args if specified
    saved_config = db.load_timer_config()

    work_duration = (args.work * 60) if args.work is not None else saved_config.work_duration
    short_break = (
        (args.short_break * 60)
        if args.short_break is not None
        else saved_config.short_break_duration
    )
    long_break = (
        (args.long_break * 60)
        if args.long_break is not None
        else saved_config.long_break_duration
    )
    cycles = args.cycles if args.cycles is not None else saved_config.sessions_per_cycle

    config = TimerConfig(
        work_duration=work_duration,
        short_break_duration=short_break,
        long_break_duration=long_break,
        sessions_per_cycle=cycles,
    )

    app = QApplication(sys.argv)
    app.setApplicationName("Pomodoro")
    app.setApplicationDisplayName("Pomodoro Focus")
    app.setDesktopFileName("pomodoro")
    # Keep app running in GNOME Topbar tray when window is closed/hidden
    app.setQuitOnLastWindowClosed(False)

    sound_manager = SoundManager()
    notifier = Notifier(sound_manager=sound_manager)

    window = PomodoroWindow(config=config, notifier=notifier, db=db)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
