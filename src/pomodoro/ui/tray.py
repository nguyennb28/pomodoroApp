from __future__ import annotations

from typing import Callable
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QIcon, QPainter, QPixmap
from PyQt6.QtWidgets import QMenu, QSystemTrayIcon, QWidget


def create_tray_pixmap(size: int = 64) -> QPixmap:
    """Generate a clean minimalist tomato icon pixmap."""
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    # Red tomato body
    painter.setBrush(QColor("#ef4444"))
    painter.setPen(Qt.PenStyle.NoPen)
    margin = int(size * 0.12)
    painter.drawEllipse(margin, margin + int(size * 0.08), size - 2 * margin, size - 2 * margin)

    # Green stem/leaf
    painter.setBrush(QColor("#22c55e"))
    painter.drawEllipse(int(size * 0.42), int(size * 0.05), int(size * 0.16), int(size * 0.18))
    painter.drawEllipse(int(size * 0.30), int(size * 0.12), int(size * 0.20), int(size * 0.12))
    painter.drawEllipse(int(size * 0.50), int(size * 0.12), int(size * 0.20), int(size * 0.12))

    painter.end()
    return pixmap


class PomodoroTray(QSystemTrayIcon):
    """Integrates with GNOME Topbar / Taskbar System Tray."""

    def __init__(
        self,
        parent: QWidget,
        on_toggle_window: Callable[[], None],
        on_toggle_timer: Callable[[], None],
        on_skip_timer: Callable[[], None],
        on_open_settings: Callable[[], None],
        on_quit: Callable[[], None],
    ) -> None:
        icon = QIcon(create_tray_pixmap())
        super().__init__(icon, parent)
        self.parent_window = parent
        self.on_toggle_window = on_toggle_window
        self.on_toggle_timer = on_toggle_timer
        self.on_skip_timer = on_skip_timer
        self.on_open_settings = on_open_settings
        self.on_quit = on_quit

        self.setToolTip("Pomodoro Focus Timer")
        self._init_menu()
        self.activated.connect(self._on_tray_activated)

    def _init_menu(self) -> None:
        self.menu = QMenu()
        self.menu.setStyleSheet(
            """
            QMenu {
                background-color: #18181b;
                color: #fafafa;
                border: 1px solid #27272a;
                border-radius: 8px;
                padding: 4px;
            }
            QMenu::item {
                padding: 6px 20px;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background-color: #27272a;
            }
            QMenu::separator {
                height: 1px;
                background-color: #27272a;
                margin: 4px 8px;
            }
            """
        )

        self.act_status = self.menu.addAction("Pomodoro: Idle")
        self.act_status.setEnabled(False)

        self.menu.addSeparator()

        self.act_toggle_win = self.menu.addAction("Show / Hide Window")
        self.act_toggle_win.triggered.connect(self.on_toggle_window)

        self.act_toggle_timer = self.menu.addAction("Start Timer")
        self.act_toggle_timer.triggered.connect(self.on_toggle_timer)

        self.act_skip = self.menu.addAction("Skip Session")
        self.act_skip.triggered.connect(self.on_skip_timer)

        self.menu.addSeparator()

        self.act_settings = self.menu.addAction("Settings...")
        self.act_settings.triggered.connect(self.on_open_settings)

        self.menu.addSeparator()

        self.act_quit = self.menu.addAction("Quit Pomodoro")
        self.act_quit.triggered.connect(self.on_quit)

        self.setContextMenu(self.menu)

    def _on_tray_activated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        if reason in (
            QSystemTrayIcon.ActivationReason.Trigger,
            QSystemTrayIcon.ActivationReason.DoubleClick,
        ):
            self.on_toggle_window()

    def update_status(self, mode_name: str, remaining_str: str, is_running: bool) -> None:
        tooltip = f"Pomodoro: {mode_name} ({remaining_str})"
        self.setToolTip(tooltip)
        self.act_status.setText(tooltip)
        self.act_toggle_timer.setText("Pause Timer" if is_running else "Start Timer")
