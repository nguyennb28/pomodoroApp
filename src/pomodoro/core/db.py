from __future__ import annotations

import sqlite3
from datetime import date, datetime
from pathlib import Path
from typing import Any

from pomodoro.core.timer import TimerConfig


class Database:
    """Manages SQLite storage for tasks, settings, and session logs."""

    def __init__(self, db_path: Path | None = None) -> None:
        if db_path is None:
            data_dir = Path.home() / ".local" / "share" / "pomodoro"
            data_dir.mkdir(parents=True, exist_ok=True)
            self.db_path = data_dir / "pomodoro.db"
        else:
            self.db_path = db_path
            self.db_path.parent.mkdir(parents=True, exist_ok=True)

        self._init_schema()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def _init_schema(self) -> None:
        with self._get_connection() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    is_completed INTEGER NOT NULL DEFAULT 0,
                    pomodoros_spent INTEGER NOT NULL DEFAULT 0,
                    created_at TEXT NOT NULL,
                    completed_at TEXT
                );

                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id INTEGER,
                    session_type TEXT NOT NULL,
                    duration_seconds INTEGER NOT NULL,
                    timestamp TEXT NOT NULL,
                    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE SET NULL
                );
                """
            )

    # --- Task Methods ---

    def add_task(self, title: str) -> int:
        clean_title = title.strip()
        if not clean_title:
            return 0
        now = datetime.now().isoformat()
        with self._get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO tasks (title, is_completed, pomodoros_spent, created_at) VALUES (?, 0, 0, ?)",
                (clean_title, now),
            )
            return int(cursor.lastrowid)

    def get_tasks(self) -> list[dict[str, Any]]:
        with self._get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM tasks ORDER BY is_completed ASC, id DESC"
            ).fetchall()
            return [dict(row) for row in rows]

    def toggle_task(self, task_id: int) -> bool:
        with self._get_connection() as conn:
            row = conn.execute(
                "SELECT is_completed FROM tasks WHERE id = ?", (task_id,)
            ).fetchone()
            if not row:
                return False
            new_status = 0 if row["is_completed"] else 1
            completed_at = datetime.now().isoformat() if new_status else None
            conn.execute(
                "UPDATE tasks SET is_completed = ?, completed_at = ? WHERE id = ?",
                (new_status, completed_at, task_id),
            )
            return bool(new_status)

    def delete_task(self, task_id: int) -> None:
        with self._get_connection() as conn:
            conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))

    def increment_task_pomodoro(self, task_id: int) -> None:
        with self._get_connection() as conn:
            conn.execute(
                "UPDATE tasks SET pomodoros_spent = pomodoros_spent + 1 WHERE id = ?",
                (task_id,),
            )

    # --- Settings Methods ---

    def get_setting(self, key: str, default: str = "") -> str:
        with self._get_connection() as conn:
            row = conn.execute(
                "SELECT value FROM settings WHERE key = ?", (key,)
            ).fetchone()
            if row:
                return str(row["value"])
            return default

    def set_setting(self, key: str, value: str) -> None:
        with self._get_connection() as conn:
            conn.execute(
                "INSERT INTO settings (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value = excluded.value",
                (key, str(value)),
            )

    def load_timer_config(self) -> TimerConfig:
        try:
            work = int(self.get_setting("work_duration", str(25 * 60)))
            short = int(self.get_setting("short_break_duration", str(5 * 60)))
            long_b = int(self.get_setting("long_break_duration", str(15 * 60)))
            cycles = int(self.get_setting("sessions_per_cycle", "4"))
            return TimerConfig(
                work_duration=work,
                short_break_duration=short,
                long_break_duration=long_b,
                sessions_per_cycle=cycles,
            )
        except Exception:
            return TimerConfig()

    def save_timer_config(self, config: TimerConfig) -> None:
        self.set_setting("work_duration", str(config.work_duration))
        self.set_setting("short_break_duration", str(config.short_break_duration))
        self.set_setting("long_break_duration", str(config.long_break_duration))
        self.set_setting("sessions_per_cycle", str(config.sessions_per_cycle))

    # --- Session Log Methods ---

    def record_session(
        self,
        session_type: str,
        duration_seconds: int,
        task_id: int | None = None,
    ) -> None:
        now = datetime.now().isoformat()
        with self._get_connection() as conn:
            conn.execute(
                "INSERT INTO sessions (task_id, session_type, duration_seconds, timestamp) VALUES (?, ?, ?, ?)",
                (task_id, session_type, duration_seconds, now),
            )

    def get_today_sessions_count(self) -> int:
        today_prefix = date.today().isoformat() + "%"
        with self._get_connection() as conn:
            row = conn.execute(
                "SELECT COUNT(*) as count FROM sessions WHERE session_type = 'work' AND timestamp LIKE ?",
                (today_prefix,),
            ).fetchone()
            return int(row["count"]) if row else 0
