from __future__ import annotations

import shutil
import subprocess
from pomodoro.core.sound import SoundManager
from pomodoro.core.timer import SessionType


class Notifier:
    """Dispatches desktop notifications and sounds when sessions end."""

    def __init__(self, sound_manager: SoundManager | None = None) -> None:
        self.sound = sound_manager or SoundManager()
        self.has_notify_send = bool(shutil.which("notify-send"))

    def notify_session_complete(self, completed_session: SessionType) -> None:
        """Trigger chime and desktop notification."""
        # 1. Play audio chime
        self.sound.play_chime()

        # 2. Desktop notification
        if completed_session == SessionType.WORK:
            title = "Focus Session Completed!"
            message = "Well done. Step away and take a well-deserved break."
            urgency = "normal"
        elif completed_session == SessionType.SHORT_BREAK:
            title = "Short Break Over"
            message = "Ready to get back in the zone? Let's focus."
            urgency = "normal"
        else:
            title = "Long Break Over"
            message = "Full cycle complete! Refreshed and ready for the next focus block."
            urgency = "normal"

        self._send_desktop_notification(title, message, urgency)

    def _send_desktop_notification(
        self, title: str, message: str, urgency: str = "normal"
    ) -> None:
        if not self.has_notify_send:
            return

        try:
            subprocess.Popen(
                [
                    "notify-send",
                    "-a",
                    "Pomodoro",
                    "-u",
                    urgency,
                    title,
                    message,
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except Exception:
            pass
