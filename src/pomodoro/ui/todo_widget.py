from __future__ import annotations

from typing import Any, Callable
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from pomodoro.core.db import Database


class TaskItemWidget(QWidget):
    """A single clean task row in the to-do list."""

    def __init__(
        self,
        task: dict[str, Any],
        is_active: bool,
        on_toggle: Callable[[int], None],
        on_set_active: Callable[[int], None],
        on_delete: Callable[[int], None],
    ) -> None:
        super().__init__()
        self.task_id = int(task["id"])
        self.is_completed = bool(task["is_completed"])
        self.pomodoros_spent = int(task.get("pomodoros_spent", 0))

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(8)

        # Checkbox
        self.chk = QCheckBox()
        self.chk.setChecked(self.is_completed)
        self.chk.stateChanged.connect(lambda: on_toggle(self.task_id))
        layout.addWidget(self.chk)

        # Title Label
        title_text = str(task["title"])
        self.lbl_title = QLabel(title_text)
        self.lbl_title.setObjectName("TaskTitle")
        self.lbl_title.setProperty("completed", "true" if self.is_completed else "false")
        layout.addWidget(self.lbl_title, stretch=1)

        # Pomodoros badge
        if self.pomodoros_spent > 0:
            lbl_pomos = QLabel(f"🍅 {self.pomodoros_spent}")
            lbl_pomos.setObjectName("TaskPomoCount")
            layout.addWidget(lbl_pomos)

        # Active Focus button
        if not self.is_completed:
            self.btn_focus = QPushButton("🎯" if is_active else "○")
            self.btn_focus.setObjectName("TaskFocusBtn")
            self.btn_focus.setProperty("active", "true" if is_active else "false")
            self.btn_focus.setToolTip("Set as active focus task" if not is_active else "Currently active task")
            self.btn_focus.setFixedSize(28, 24)
            self.btn_focus.clicked.connect(lambda: on_set_active(self.task_id))
            layout.addWidget(self.btn_focus)

        # Delete button
        btn_del = QPushButton("✕")
        btn_del.setObjectName("TaskDeleteBtn")
        btn_del.setFixedSize(22, 22)
        btn_del.setToolTip("Delete task")
        btn_del.clicked.connect(lambda: on_delete(self.task_id))
        layout.addWidget(btn_del)

        # Container styling property
        self.setProperty("active", "true" if is_active else "false")


class TodoListWidget(QWidget):
    """Minimalist, distraction-free To-Do list backed by SQLite."""

    active_task_changed = pyqtSignal(object, object)  # (task_id, title)

    def __init__(self, db: Database) -> None:
        super().__init__()
        self.db = db
        self.active_task_id: int | None = None
        self.active_task_title: str | None = None

        self._init_ui()
        self.refresh_tasks()

    def _init_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(10)

        # Header
        header_layout = QHBoxLayout()
        lbl_header = QLabel("TASKS")
        lbl_header.setObjectName("TitleLabel")
        header_layout.addWidget(lbl_header)
        header_layout.addStretch()
        main_layout.addLayout(header_layout)

        # Input field
        self.input_task = QLineEdit()
        self.input_task.setObjectName("TaskInput")
        self.input_task.setPlaceholderText("Add a focus task & press Enter...")
        self.input_task.returnPressed.connect(self._add_task)
        main_layout.addWidget(self.input_task)

        # Scroll area for tasks
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.tasks_container = QWidget()
        self.tasks_layout = QVBoxLayout(self.tasks_container)
        self.tasks_layout.setContentsMargins(0, 0, 0, 0)
        self.tasks_layout.setSpacing(6)
        self.tasks_layout.addStretch()

        self.scroll_area.setWidget(self.tasks_container)
        main_layout.addWidget(self.scroll_area, stretch=1)

    def _add_task(self) -> None:
        title = self.input_task.text().strip()
        if not title:
            return
        task_id = self.db.add_task(title)
        self.input_task.clear()

        # If no active task, set this as active
        if self.active_task_id is None:
            self.set_active_task(task_id, title)

        self.refresh_tasks()

    def set_active_task(self, task_id: int | None, title: str | None = None) -> None:
        if self.active_task_id == task_id:
            # Toggle off
            self.active_task_id = None
            self.active_task_title = None
        else:
            self.active_task_id = task_id
            self.active_task_title = title
            if title is None and task_id is not None:
                for t in self.db.get_tasks():
                    if t["id"] == task_id:
                        self.active_task_title = t["title"]
                        break

        self.active_task_changed.emit(self.active_task_id, self.active_task_title)
        self.refresh_tasks()

    def refresh_tasks(self) -> None:
        # Clear layout
        while self.tasks_layout.count() > 1:
            item = self.tasks_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        tasks = self.db.get_tasks()
        if not tasks:
            empty_lbl = QLabel("No tasks yet. Create one to stay focused!")
            empty_lbl.setObjectName("EmptyTasksLabel")
            empty_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tasks_layout.insertWidget(0, empty_lbl)
            return

        for task in tasks:
            is_active = (self.active_task_id == task["id"])
            item_widget = TaskItemWidget(
                task=task,
                is_active=is_active,
                on_toggle=self._toggle_task,
                on_set_active=lambda tid: self.set_active_task(tid),
                on_delete=self._delete_task,
            )
            self.tasks_layout.insertWidget(self.tasks_layout.count() - 1, item_widget)

    def _toggle_task(self, task_id: int) -> None:
        self.db.toggle_task(task_id)
        if self.active_task_id == task_id:
            self.set_active_task(None)
        else:
            self.refresh_tasks()

    def _delete_task(self, task_id: int) -> None:
        self.db.delete_task(task_id)
        if self.active_task_id == task_id:
            self.set_active_task(None)
        else:
            self.refresh_tasks()

    def record_pomodoro_completed(self) -> None:
        """Called when a work session finishes."""
        if self.active_task_id is not None:
            self.db.increment_task_pomodoro(self.active_task_id)
            self.refresh_tasks()
