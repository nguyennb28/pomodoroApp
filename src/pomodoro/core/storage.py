from __future__ import annotations

import json
from datetime import date, datetime
from pathlib import Path
from pomodoro.core.timer import SessionType


class SessionStorage:
    """Manages recording and reading completed session statistics."""

    def __init__(self, data_path: Path | None = None) -> None:
        if data_path is None:
            self.data_dir = Path.home() / ".local" / "share" / "pomodoro"
            self.file_path = self.data_dir / "stats.json"
        else:
            self.file_path = data_path
            self.data_dir = self.file_path.parent

        self._ensure_storage()

    def _ensure_storage(self) -> None:
        try:
            self.data_dir.mkdir(parents=True, exist_ok=True)
            if not self.file_path.exists():
                self.file_path.write_text(
                    json.dumps({"sessions": []}, indent=2), encoding="utf-8"
                )
        except Exception:
            pass

    def record_session(self, session_type: SessionType, duration_seconds: int) -> None:
        """Record a completed session."""
        try:
            self._ensure_storage()
            data = {"sessions": []}
            if self.file_path.exists():
                try:
                    data = json.loads(self.file_path.read_text(encoding="utf-8"))
                except Exception:
                    data = {"sessions": []}

            data.setdefault("sessions", []).append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "session_type": session_type.value,
                    "duration_seconds": duration_seconds,
                }
            )

            self.file_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        except Exception:
            pass

    def get_today_work_sessions(self) -> int:
        """Count how many focus/work sessions were completed today."""
        try:
            if not self.file_path.exists():
                return 0
            data = json.loads(self.file_path.read_text(encoding="utf-8"))
            today_str = date.today().isoformat()
            count = 0
            for session in data.get("sessions", []):
                if session.get("session_type") == SessionType.WORK.value:
                    ts = session.get("timestamp", "")
                    if ts.startswith(today_str):
                        count += 1
            return count
        except Exception:
            return 0
