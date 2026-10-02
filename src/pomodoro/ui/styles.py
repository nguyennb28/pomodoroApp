"""Theme stylesheets: Dracula Dark Mode & Minimalist Light Mode."""

DRACULA_THEME = """
QWidget#CentralWidget {
    background-color: #282a36;
    border: 1px solid #44475a;
    border-radius: 16px;
}

QLabel#TitleLabel {
    color: #6272a4;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}

QLabel#ModeBadge {
    background-color: #44475a;
    color: #bd93f9;
    font-size: 11px;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 10px;
    letter-spacing: 1px;
}

QLabel#ModeBadge[mode="break"] {
    color: #50fa7b;
}

QLabel#TimerDisplay {
    color: #f8f8f2;
    font-size: 52px;
    font-weight: 700;
    letter-spacing: -1px;
    font-family: "JetBrains Mono", "SF Mono", "Fira Code", "Roboto Mono", "Courier New", monospace;
}

QLabel#TimerDisplay[fullscreen="true"] {
    font-size: 120px;
}

QLabel#ActiveTaskBanner {
    color: #8be9fd;
    background-color: rgba(139, 233, 253, 0.12);
    border: 1px dashed #8be9fd;
    border-radius: 8px;
    padding: 6px 12px;
    font-size: 12px;
    font-weight: 500;
}

QLabel#SessionDots {
    color: #bd93f9;
    font-size: 13px;
    letter-spacing: 4px;
}

QLabel#StatsLabel {
    color: #6272a4;
    font-size: 11px;
    font-weight: 500;
}

/* PushButtons */
QPushButton {
    font-family: inherit;
    font-size: 12px;
    font-weight: 600;
    border-radius: 8px;
    padding: 8px 16px;
    border: 1px solid transparent;
}

QPushButton#PrimaryButton {
    background-color: #bd93f9;
    color: #282a36;
}

QPushButton#PrimaryButton:hover {
    background-color: #ff79c6;
    color: #282a36;
}

QPushButton#PrimaryButton:pressed {
    background-color: #bd93f9;
}

QPushButton#SecondaryButton {
    background-color: #21222c;
    color: #f8f8f2;
    border: 1px solid #44475a;
}

QPushButton#SecondaryButton:hover {
    background-color: #44475a;
    color: #50fa7b;
}

QPushButton#IconButton {
    background-color: transparent;
    color: #6272a4;
    padding: 4px;
    font-size: 14px;
    border-radius: 6px;
    border: none;
}

QPushButton#IconButton:hover {
    color: #f8f8f2;
    background-color: #44475a;
}

QPushButton#IconButton[active="true"] {
    color: #8be9fd;
    background-color: rgba(139, 233, 253, 0.18);
}

QPushButton#CloseButton:hover {
    color: #ff5555;
    background-color: rgba(255, 85, 85, 0.18);
}

/* To-Do List Inputs & Items (Dracula) */
QScrollArea {
    background: transparent;
    border: none;
}

QScrollArea > QWidget > QWidget {
    background: transparent;
}

QLineEdit#TaskInput {
    background-color: #21222c;
    color: #f8f8f2;
    border: 1px solid #44475a;
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 12px;
}

QLineEdit#TaskInput:focus {
    border: 1px solid #bd93f9;
}

TaskItemWidget {
    background-color: #21222c;
    border: 1px solid #44475a;
    border-radius: 8px;
}

TaskItemWidget[active="true"] {
    background-color: #282a36;
    border: 1.5px solid #bd93f9;
}

QLabel#TaskTitle {
    color: #f8f8f2;
    font-size: 12px;
    font-weight: 500;
}

QLabel#TaskTitle[completed="true"] {
    color: #6272a4;
    text-decoration: line-through;
}

QLabel#EmptyTasksLabel {
    color: #6272a4;
    font-size: 11px;
    padding: 20px 0;
}

QCheckBox {
    spacing: 6px;
}

QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border: 1px solid #6272a4;
    border-radius: 4px;
    background-color: #21222c;
}

QCheckBox::indicator:checked {
    background-color: #bd93f9;
    border-color: #bd93f9;
}

QPushButton#TaskFocusBtn {
    background-color: #44475a;
    color: #f8f8f2;
    border: none;
    border-radius: 4px;
    font-size: 11px;
    padding: 2px;
}

QPushButton#TaskFocusBtn:hover {
    color: #8be9fd;
}

QPushButton#TaskFocusBtn[active="true"] {
    background-color: rgba(139, 233, 253, 0.25);
    color: #8be9fd;
    border: 1px solid #8be9fd;
}

QPushButton#TaskDeleteBtn {
    background-color: transparent;
    color: #6272a4;
    border: none;
    border-radius: 4px;
    font-size: 11px;
    padding: 2px;
}

QPushButton#TaskDeleteBtn:hover {
    color: #ff5555;
    background-color: rgba(255, 85, 85, 0.18);
}

QLabel#TaskPomoCount {
    color: #ff5555;
    font-size: 11px;
    font-weight: 700;
}

/* SpinBoxes */
QSpinBox {
    background-color: #21222c;
    color: #f8f8f2;
    border: 1px solid #44475a;
    border-radius: 6px;
    padding: 6px 8px;
}

QSpinBox:focus {
    border: 1px solid #bd93f9;
}
"""

LIGHT_THEME = """
QWidget#CentralWidget {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
}

QLabel#TitleLabel {
    color: #64748b;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}

QLabel#ModeBadge {
    background-color: #eff6ff;
    color: #2563eb;
    font-size: 11px;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 10px;
    letter-spacing: 1px;
}

QLabel#ModeBadge[mode="break"] {
    background-color: #ecfdf5;
    color: #059669;
}

QLabel#TimerDisplay {
    color: #0f172a;
    font-size: 52px;
    font-weight: 700;
    letter-spacing: -1px;
    font-family: "JetBrains Mono", "SF Mono", "Fira Code", "Roboto Mono", "Courier New", monospace;
}

QLabel#TimerDisplay[fullscreen="true"] {
    font-size: 120px;
}

QLabel#ActiveTaskBanner {
    color: #2563eb;
    background-color: rgba(37, 99, 235, 0.08);
    border: 1px dashed #3b82f6;
    border-radius: 8px;
    padding: 6px 12px;
    font-size: 12px;
    font-weight: 500;
}

QLabel#SessionDots {
    color: #2563eb;
    font-size: 13px;
    letter-spacing: 4px;
}

QLabel#StatsLabel {
    color: #64748b;
    font-size: 11px;
    font-weight: 500;
}

/* PushButtons */
QPushButton {
    font-family: inherit;
    font-size: 12px;
    font-weight: 600;
    border-radius: 8px;
    padding: 8px 16px;
    border: 1px solid transparent;
}

QPushButton#PrimaryButton {
    background-color: #0f172a;
    color: #ffffff;
}

QPushButton#PrimaryButton:hover {
    background-color: #334155;
    color: #ffffff;
}

QPushButton#PrimaryButton:pressed {
    background-color: #0f172a;
}

QPushButton#SecondaryButton {
    background-color: #f8fafc;
    color: #334155;
    border: 1px solid #cbd5e1;
}

QPushButton#SecondaryButton:hover {
    background-color: #f1f5f9;
    color: #0f172a;
}

QPushButton#IconButton {
    background-color: transparent;
    color: #64748b;
    padding: 4px;
    font-size: 14px;
    border-radius: 6px;
    border: none;
}

QPushButton#IconButton:hover {
    color: #0f172a;
    background-color: #f1f5f9;
}

QPushButton#IconButton[active="true"] {
    color: #2563eb;
    background-color: rgba(37, 99, 235, 0.12);
}

QPushButton#CloseButton:hover {
    color: #ef4444;
    background-color: rgba(239, 68, 68, 0.12);
}

/* To-Do List Inputs & Items (Light) */
QScrollArea {
    background: transparent;
    border: none;
}

QScrollArea > QWidget > QWidget {
    background: transparent;
}

QLineEdit#TaskInput {
    background-color: #f1f5f9;
    color: #09090b;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 12px;
}

QLineEdit#TaskInput:focus {
    border: 1px solid #2563eb;
}

TaskItemWidget {
    background-color: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
}

TaskItemWidget[active="true"] {
    background-color: #eff6ff;
    border: 1.5px solid #2563eb;
}

QLabel#TaskTitle {
    color: #09090b;
    font-size: 12px;
    font-weight: 600;
}

QLabel#TaskTitle[completed="true"] {
    color: #94a3b8;
    text-decoration: line-through;
}

QLabel#EmptyTasksLabel {
    color: #64748b;
    font-size: 11px;
    padding: 20px 0;
}

QCheckBox {
    spacing: 6px;
}

QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border: 1px solid #94a3b8;
    border-radius: 4px;
    background-color: #ffffff;
}

QCheckBox::indicator:checked {
    background-color: #2563eb;
    border-color: #2563eb;
}

QPushButton#TaskFocusBtn {
    background-color: #ffffff;
    color: #334155;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    font-size: 11px;
    padding: 2px;
}

QPushButton#TaskFocusBtn:hover {
    color: #2563eb;
    border-color: #2563eb;
}

QPushButton#TaskFocusBtn[active="true"] {
    background-color: #eff6ff;
    color: #2563eb;
    border: 1px solid #2563eb;
}

QPushButton#TaskDeleteBtn {
    background-color: transparent;
    color: #94a3b8;
    border: none;
    border-radius: 4px;
    font-size: 11px;
    padding: 2px;
}

QPushButton#TaskDeleteBtn:hover {
    color: #ef4444;
    background-color: rgba(239, 68, 68, 0.12);
}

QLabel#TaskPomoCount {
    color: #ef4444;
    font-size: 11px;
    font-weight: 700;
}

/* SpinBoxes */
QSpinBox {
    background-color: #f8fafc;
    color: #0f172a;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 6px 8px;
}

QSpinBox:focus {
    border: 1px solid #2563eb;
}
"""

THEME_STYLESHEET = DRACULA_THEME


def get_theme_stylesheet(theme: str) -> str:
    """Return QSS stylesheet for given theme ('dracula' or 'light')."""
    if theme == "light":
        return LIGHT_THEME
    return DRACULA_THEME
