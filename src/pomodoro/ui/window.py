from __future__ import annotations

from PyQt6.QtCore import QEvent, QObject, QPoint, Qt, QTimer
from PyQt6.QtGui import QKeyEvent, QMouseEvent
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from pomodoro.core.db import Database
from pomodoro.core.notifier import Notifier
from pomodoro.core.timer import (
    PomodoroTimer,
    SessionType,
    TimerConfig,
    TimerState,
)
from pomodoro.ui.settings_dialog import SettingsDialog
from pomodoro.ui.styles import get_theme_stylesheet
from pomodoro.ui.todo_widget import TodoListWidget
from pomodoro.ui.tray import PomodoroTray


class PomodoroWindow(QWidget):
    """
    Multifunctional minimalist Pomodoro application.
    Supports Dracula / Light themes, smooth mouse dragging,
    Compact Floating Widget, Windowed with Tasks, and Fullscreen Zen Mode.
    """

    def __init__(
        self,
        config: TimerConfig | None = None,
        notifier: Notifier | None = None,
        db: Database | None = None,
    ) -> None:
        super().__init__()
        self.db = db or Database()
        self.config = config or self.db.load_timer_config()
        self.notifier = notifier or Notifier()

        self.current_theme = self.db.get_setting("theme", "dracula")
        self.timer = PomodoroTimer(
            config=self.config,
            on_tick=self._handle_tick,
            on_state_change=self._handle_state_change,
            on_session_complete=self._handle_session_complete,
        )

        self._drag_pos = QPoint()
        self.is_pinned = True
        self.is_fullscreen_mode = False
        self.show_tasks_panel = True

        self._init_window_flags()
        self._init_ui()
        self._apply_theme()
        self._setup_mouse_drag_filters()

        # Initialize System Tray
        self.tray = PomodoroTray(
            parent=self,
            on_toggle_window=self.toggle_window_visibility,
            on_toggle_timer=self.timer.toggle,
            on_skip_timer=self.timer.skip,
            on_open_settings=self.open_settings,
            on_quit=self.quit_application,
        )
        self.tray.show()

        # 100ms UI ticker calling monotonic timer
        self._qtimer = QTimer(self)
        self._qtimer.setInterval(100)
        self._qtimer.timeout.connect(self._on_qtimer_timeout)
        self._qtimer.start()

        self._update_display()

    def _init_window_flags(self) -> None:
        flags = (
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Window
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setWindowFlags(flags)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(620, 360)

    def _init_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Central container widget
        self.central_widget = QWidget(self)
        self.central_widget.setObjectName("CentralWidget")
        self.container_layout = QVBoxLayout(self.central_widget)
        self.container_layout.setContentsMargins(16, 12, 16, 14)
        self.container_layout.setSpacing(10)

        # 1. Top bar: Title + Theme Toggle + Mode Buttons + Window controls
        top_bar = QHBoxLayout()
        top_bar.setContentsMargins(0, 0, 0, 0)

        self.title_label = QLabel("POMODORO")
        self.title_label.setObjectName("TitleLabel")
        top_bar.addWidget(self.title_label)

        top_bar.addStretch()

        # Theme toggle button (Dracula vs Light)
        self.btn_theme = QPushButton("☀️" if self.current_theme == "dracula" else "🌙")
        self.btn_theme.setObjectName("IconButton")
        self.btn_theme.setToolTip("Toggle Theme (Dracula / Light)")
        self.btn_theme.setFixedSize(26, 26)
        self.btn_theme.clicked.connect(self.toggle_theme)
        top_bar.addWidget(self.btn_theme)

        # Task panel toggle button
        self.btn_tasks_toggle = QPushButton("📋")
        self.btn_tasks_toggle.setObjectName("IconButton")
        self.btn_tasks_toggle.setProperty("active", "true")
        self.btn_tasks_toggle.setToolTip("Toggle Tasks Panel (T)")
        self.btn_tasks_toggle.setFixedSize(26, 26)
        self.btn_tasks_toggle.clicked.connect(self.toggle_tasks_panel)
        top_bar.addWidget(self.btn_tasks_toggle)

        # Settings button
        self.btn_settings = QPushButton("⚙")
        self.btn_settings.setObjectName("IconButton")
        self.btn_settings.setToolTip("Settings")
        self.btn_settings.setFixedSize(26, 26)
        self.btn_settings.clicked.connect(self.open_settings)
        top_bar.addWidget(self.btn_settings)

        # Fullscreen Zen Mode button
        self.btn_fullscreen = QPushButton("⛶")
        self.btn_fullscreen.setObjectName("IconButton")
        self.btn_fullscreen.setToolTip("Toggle Fullscreen Zen Mode (F11)")
        self.btn_fullscreen.setFixedSize(26, 26)
        self.btn_fullscreen.clicked.connect(self.toggle_fullscreen)
        top_bar.addWidget(self.btn_fullscreen)

        # Pin button
        self.pin_btn = QPushButton("📌")
        self.pin_btn.setObjectName("IconButton")
        self.pin_btn.setProperty("active", "true")
        self.pin_btn.setToolTip("Always on Top (P)")
        self.pin_btn.setFixedSize(26, 26)
        self.pin_btn.clicked.connect(self.toggle_pin)
        top_bar.addWidget(self.pin_btn)

        # Close button
        self.close_btn = QPushButton("✕")
        self.close_btn.setObjectName("IconButton")
        self.close_btn.setProperty("isClose", "true")
        self.close_btn.setToolTip("Hide to Tray (Esc)")
        self.close_btn.setFixedSize(26, 26)
        self.close_btn.clicked.connect(self.hide)
        top_bar.addWidget(self.close_btn)

        self.container_layout.addLayout(top_bar)

        # 2. Main Content Area (Timer Pane + Todo Pane)
        self.content_layout = QHBoxLayout()
        self.content_layout.setSpacing(16)

        # --- Left Pane: Timer ---
        self.timer_pane = QWidget()
        timer_pane_layout = QVBoxLayout(self.timer_pane)
        timer_pane_layout.setContentsMargins(0, 0, 0, 0)
        timer_pane_layout.setSpacing(8)

        # Status Badge
        badge_layout = QHBoxLayout()
        self.mode_badge = QLabel("FOCUS")
        self.mode_badge.setObjectName("ModeBadge")
        self.mode_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        badge_layout.addStretch()
        badge_layout.addWidget(self.mode_badge)
        badge_layout.addStretch()
        timer_pane_layout.addLayout(badge_layout)

        # Active Task Banner
        self.lbl_active_task = QLabel("No active task")
        self.lbl_active_task.setObjectName("ActiveTaskBanner")
        self.lbl_active_task.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_active_task.setVisible(False)
        timer_pane_layout.addWidget(self.lbl_active_task)

        # Big Countdown Display
        self.timer_label = QLabel("25:00")
        self.timer_label.setObjectName("TimerDisplay")
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        timer_pane_layout.addWidget(self.timer_label)

        # Session Indicators & Today Stats
        info_layout = QHBoxLayout()
        self.dots_label = QLabel("○ ○ ○ ○")
        self.dots_label.setObjectName("SessionDots")
        info_layout.addWidget(self.dots_label)

        info_layout.addStretch()

        today_count = self.db.get_today_sessions_count()
        self.stats_label = QLabel(f"{today_count} done today")
        self.stats_label.setObjectName("StatsLabel")
        info_layout.addWidget(self.stats_label)
        timer_pane_layout.addLayout(info_layout)

        # Controls Row
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(8)

        self.btn_reset = QPushButton("↺")
        self.btn_reset.setObjectName("SecondaryButton")
        self.btn_reset.setToolTip("Reset Session (R)")
        self.btn_reset.setFixedWidth(44)
        self.btn_reset.clicked.connect(self.timer.reset)
        controls_layout.addWidget(self.btn_reset)

        self.btn_toggle = QPushButton("Start")
        self.btn_toggle.setObjectName("PrimaryButton")
        self.btn_toggle.setToolTip("Start / Pause (Space)")
        self.btn_toggle.clicked.connect(self.timer.toggle)
        controls_layout.addWidget(self.btn_toggle, stretch=1)

        self.btn_skip = QPushButton("⏭")
        self.btn_skip.setObjectName("SecondaryButton")
        self.btn_skip.setToolTip("Skip Session (S)")
        self.btn_skip.setFixedWidth(44)
        self.btn_skip.clicked.connect(self.timer.skip)
        controls_layout.addWidget(self.btn_skip)

        timer_pane_layout.addLayout(controls_layout)
        self.content_layout.addWidget(self.timer_pane, stretch=1)

        # --- Right Pane: Todo List ---
        self.todo_widget = TodoListWidget(db=self.db)
        self.todo_widget.active_task_changed.connect(self._on_active_task_changed)
        self.content_layout.addWidget(self.todo_widget, stretch=1)

        self.container_layout.addLayout(self.content_layout)
        main_layout.addWidget(self.central_widget)

    # --- Mouse Drag Event Filters ---

    def _setup_mouse_drag_filters(self) -> None:
        """Allow dragging the window by clicking on any background/label element."""
        widgets = [
            self,
            self.central_widget,
            self.title_label,
            self.timer_pane,
            self.timer_label,
            self.dots_label,
            self.stats_label,
            self.mode_badge,
            self.lbl_active_task,
            self.todo_widget,
        ]
        for w in widgets:
            w.installEventFilter(self)

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if self.is_fullscreen_mode:
            return super().eventFilter(watched, event)

        if event.type() == QEvent.Type.MouseButtonPress:
            from PyQt6.QtWidgets import QPushButton, QLineEdit, QCheckBox, QSpinBox
            if isinstance(watched, (QPushButton, QLineEdit, QCheckBox, QSpinBox)):
                return False

            mouse_event = cast(QMouseEvent, event)
            if mouse_event.button() == Qt.MouseButton.LeftButton:
                # 1. Native Wayland / X11 Compositor Grab (Wayland Protocol Compliant)
                wh = self.windowHandle()
                if wh is not None and wh.startSystemMove():
                    return True

                # 2. Fallback to manual delta move (for standard X11)
                self._drag_pos = mouse_event.globalPosition().toPoint() - self.frameGeometry().topLeft()
        elif event.type() == QEvent.Type.MouseMove:
            mouse_event = cast(QMouseEvent, event)
            if mouse_event.buttons() == Qt.MouseButton.LeftButton and not self._drag_pos.isNull():
                self.move(mouse_event.globalPosition().toPoint() - self._drag_pos)
                return True
        elif event.type() == QEvent.Type.MouseButtonRelease:
            self._drag_pos = QPoint()

        return super().eventFilter(watched, event)

    # --- Theme Management ---

    def _apply_theme(self) -> None:
        qss = get_theme_stylesheet(self.current_theme)
        self.setStyleSheet(qss)
        self.btn_theme.setText("☀️" if self.current_theme == "dracula" else "🌙")

    def toggle_theme(self) -> None:
        self.current_theme = "light" if self.current_theme == "dracula" else "dracula"
        self.db.set_setting("theme", self.current_theme)
        self._apply_theme()
        self._update_display()

    # --- Mode & Window Management ---

    def toggle_tasks_panel(self) -> None:
        self.show_tasks_panel = not self.show_tasks_panel
        self.todo_widget.setVisible(self.show_tasks_panel)
        self.btn_tasks_toggle.setProperty("active", "true" if self.show_tasks_panel else "false")
        self.btn_tasks_toggle.style().unpolish(self.btn_tasks_toggle)
        self.btn_tasks_toggle.style().polish(self.btn_tasks_toggle)

        if self.show_tasks_panel:
            self.resize(620, 360)
        else:
            self.resize(300, 240)

    def toggle_fullscreen(self) -> None:
        self.is_fullscreen_mode = not self.is_fullscreen_mode
        if self.is_fullscreen_mode:
            self.showFullScreen()
            self.timer_label.setProperty("fullscreen", "true")
        else:
            self.showNormal()
            self.timer_label.setProperty("fullscreen", "false")
            if self.show_tasks_panel:
                self.resize(620, 360)
            else:
                self.resize(300, 240)

        self.timer_label.style().unpolish(self.timer_label)
        self.timer_label.style().polish(self.timer_label)

    def toggle_pin(self) -> None:
        self.is_pinned = not self.is_pinned
        self.pin_btn.setProperty("active", "true" if self.is_pinned else "false")
        self.pin_btn.style().unpolish(self.pin_btn)
        self.pin_btn.style().polish(self.pin_btn)

        flags = self.windowFlags()
        if self.is_pinned:
            flags |= Qt.WindowType.WindowStaysOnTopHint
        else:
            flags &= ~Qt.WindowType.WindowStaysOnTopHint

        self.setWindowFlags(flags)
        self.show()

    def toggle_window_visibility(self) -> None:
        if self.isVisible():
            self.hide()
        else:
            self.show()
            self.raise_()
            self.activateWindow()

    def open_settings(self) -> None:
        dialog = SettingsDialog(self.timer.config, parent=self)
        dialog.setStyleSheet(get_theme_stylesheet(self.current_theme))
        if dialog.exec() and dialog.saved_config:
            new_cfg = dialog.saved_config
            self.timer.config = new_cfg
            self.db.save_timer_config(new_cfg)
            if self.timer.state == TimerState.IDLE:
                self.timer.reset()
            self._update_display()

    def quit_application(self) -> None:
        self.tray.hide()
        self.close()

    # --- Active Task & Events ---

    def _on_active_task_changed(self, task_id: int | None, title: str | None) -> None:
        if title:
            self.lbl_active_task.setText(f"🎯 {title}")
            self.lbl_active_task.setVisible(True)
        else:
            self.lbl_active_task.setVisible(False)

    def _on_qtimer_timeout(self) -> None:
        self.timer.tick()

    def _handle_tick(self, remaining_seconds: float) -> None:
        time_str = PomodoroTimer.format_time(remaining_seconds)
        self.timer_label.setText(time_str)

        is_running = (self.timer.state == TimerState.RUNNING)
        self.tray.update_status(
            self.timer.current_session.display_name,
            time_str,
            is_running,
        )

    def _handle_state_change(
        self, state: TimerState, session_type: SessionType
    ) -> None:
        self._update_display()

    def _handle_session_complete(self, completed_session: SessionType) -> None:
        self.notifier.notify_session_complete(completed_session)

        if completed_session == SessionType.WORK:
            self.db.record_session(
                session_type="work",
                duration_seconds=self.timer.config.work_duration,
                task_id=self.todo_widget.active_task_id,
            )
            self.todo_widget.record_pomodoro_completed()

        today_count = self.db.get_today_sessions_count()
        self.stats_label.setText(f"{today_count} done today")
        self._update_display()

        self.show()
        self.raise_()
        self.activateWindow()

    def _update_display(self) -> None:
        time_str = PomodoroTimer.format_time(self.timer.remaining_seconds)
        self.timer_label.setText(time_str)

        is_break = self.timer.current_session in (
            SessionType.SHORT_BREAK,
            SessionType.LONG_BREAK,
        )
        self.mode_badge.setText(
            self.timer.current_session.display_name.upper()
        )
        self.mode_badge.setProperty("mode", "break" if is_break else "work")
        self.mode_badge.style().unpolish(self.mode_badge)
        self.mode_badge.style().polish(self.mode_badge)

        if self.timer.state == TimerState.RUNNING:
            self.btn_toggle.setText("Pause")
        else:
            self.btn_toggle.setText("Start")

        cycle_count = self.timer.completed_sessions_in_cycle
        dots = []
        for i in range(self.timer.config.sessions_per_cycle):
            if i < cycle_count:
                dots.append("●")
            else:
                dots.append("○")
        self.dots_label.setText(" ".join(dots))

        is_running = (self.timer.state == TimerState.RUNNING)
        self.tray.update_status(
            self.timer.current_session.display_name,
            time_str,
            is_running,
        )

    # --- Mouse Dragging & Keyboard shortcuts ---

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton and not self.is_fullscreen_mode:
            wh = self.windowHandle()
            if wh is not None and wh.startSystemMove():
                return
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if event.buttons() == Qt.MouseButton.LeftButton and not self._drag_pos.isNull() and not self.is_fullscreen_mode:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self._drag_pos = QPoint()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        key = event.key()
        if key == Qt.Key.Key_Space:
            self.timer.toggle()
        elif key == Qt.Key.Key_R:
            self.timer.reset()
        elif key == Qt.Key.Key_S:
            self.timer.skip()
        elif key == Qt.Key.Key_P:
            self.toggle_pin()
        elif key == Qt.Key.Key_T:
            self.toggle_tasks_panel()
        elif key == Qt.Key.Key_F11:
            self.toggle_fullscreen()
        elif key in (Qt.Key.Key_Escape, Qt.Key.Key_Q):
            if self.is_fullscreen_mode:
                self.toggle_fullscreen()
            else:
                self.hide()
        else:
            super().keyPressEvent(event)
