from __future__ import annotations

from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import (
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from pomodoro.core.timer import TimerConfig
from pomodoro.ui.styles import THEME_STYLESHEET


class SettingsDialog(QDialog):
    """Clean, minimal modal dialog for adjusting timer durations."""

    def __init__(self, current_config: TimerConfig, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.current_config = current_config
        self.saved_config: TimerConfig | None = None
        self._drag_pos = QPoint()

        self.setWindowTitle("Timer Settings")
        self.setFixedSize(300, 260)

        # Inherit stays-on-top so it is never obscured by parent
        flags = (
            Qt.WindowType.Dialog
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setWindowFlags(flags)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self._init_ui()
        self.setStyleSheet(THEME_STYLESHEET)

        # Center on parent if parent exists
        if parent:
            p_geo = parent.geometry()
            self.move(
                p_geo.center().x() - self.width() // 2,
                p_geo.center().y() - self.height() // 2,
            )

    def _init_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        container = QWidget(self)
        container.setObjectName("CentralWidget")
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(20, 16, 20, 18)
        container_layout.setSpacing(12)

        # Header
        top_bar = QHBoxLayout()
        lbl_title = QLabel("TIMER SETTINGS")
        lbl_title.setObjectName("TitleLabel")
        top_bar.addWidget(lbl_title)
        top_bar.addStretch()

        btn_close = QPushButton("✕")
        btn_close.setObjectName("IconButton")
        btn_close.setFixedSize(22, 22)
        btn_close.clicked.connect(self.reject)
        top_bar.addWidget(btn_close)

        container_layout.addLayout(top_bar)

        # Form fields
        form = QFormLayout()
        form.setSpacing(10)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)

        # Work Duration
        self.spin_work = QSpinBox()
        self.spin_work.setRange(1, 180)
        self.spin_work.setValue(self.current_config.work_duration // 60)
        self.spin_work.setSuffix(" min")
        lbl_work = QLabel("Focus Time:")
        lbl_work.setStyleSheet("color: #d4d4d8; font-size: 12px; font-weight: 500;")
        form.addRow(lbl_work, self.spin_work)

        # Short Break
        self.spin_short = QSpinBox()
        self.spin_short.setRange(1, 60)
        self.spin_short.setValue(self.current_config.short_break_duration // 60)
        self.spin_short.setSuffix(" min")
        lbl_short = QLabel("Short Break:")
        lbl_short.setStyleSheet("color: #d4d4d8; font-size: 12px; font-weight: 500;")
        form.addRow(lbl_short, self.spin_short)

        # Long Break
        self.spin_long = QSpinBox()
        self.spin_long.setRange(1, 90)
        self.spin_long.setValue(self.current_config.long_break_duration // 60)
        self.spin_long.setSuffix(" min")
        lbl_long = QLabel("Long Break:")
        lbl_long.setStyleSheet("color: #d4d4d8; font-size: 12px; font-weight: 500;")
        form.addRow(lbl_long, self.spin_long)

        # Cycles
        self.spin_cycles = QSpinBox()
        self.spin_cycles.setRange(1, 12)
        self.spin_cycles.setValue(self.current_config.sessions_per_cycle)
        lbl_cycles = QLabel("Cycles:")
        lbl_cycles.setStyleSheet("color: #d4d4d8; font-size: 12px; font-weight: 500;")
        form.addRow(lbl_cycles, self.spin_cycles)

        container_layout.addLayout(form)

        # Action Buttons
        btn_layout = QHBoxLayout()
        btn_cancel = QPushButton("Cancel")
        btn_cancel.setObjectName("SecondaryButton")
        btn_cancel.clicked.connect(self.reject)
        btn_layout.addWidget(btn_cancel)

        btn_save = QPushButton("Save")
        btn_save.setObjectName("PrimaryButton")
        btn_save.clicked.connect(self._save)
        btn_layout.addWidget(btn_save)

        container_layout.addLayout(btn_layout)
        main_layout.addWidget(container)

    def _save(self) -> None:
        self.saved_config = TimerConfig(
            work_duration=self.spin_work.value() * 60,
            short_break_duration=self.spin_short.value() * 60,
            long_break_duration=self.spin_long.value() * 60,
            sessions_per_cycle=self.spin_cycles.value(),
        )
        self.accept()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            wh = self.windowHandle()
            if wh is not None and wh.startSystemMove():
                return
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if event.buttons() == Qt.MouseButton.LeftButton and not self._drag_pos.isNull():
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self._drag_pos = QPoint()
