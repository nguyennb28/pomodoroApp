#!/usr/bin/env python3
"""
Install Pomodoro desktop entry and icons for Ubuntu GNOME.
Enables launching Pomodoro from Ubuntu Application Grid / Dock.
"""
from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path


def install_desktop() -> None:
    workspace_dir = Path(__file__).resolve().parent.parent
    user_home = Path.home()

    bin_dir = user_home / ".local" / "bin"
    app_dir = user_home / ".local" / "share" / "applications"
    icon_scalable_dir = user_home / ".local" / "share" / "icons" / "hicolor" / "scalable" / "apps"

    bin_dir.mkdir(parents=True, exist_ok=True)
    app_dir.mkdir(parents=True, exist_ok=True)
    icon_scalable_dir.mkdir(parents=True, exist_ok=True)

    # 1. Create launcher executable in ~/.local/bin/pomodoro-app
    launcher_path = bin_dir / "pomodoro-app"
    venv_pomodoro = workspace_dir / ".venv" / "bin" / "pomodoro"

    launcher_content = f"""#!/usr/bin/env bash
if [ -f "{venv_pomodoro}" ]; then
    exec "{venv_pomodoro}" "$@"
else
    exec uv run --project "{workspace_dir}" pomodoro "$@"
fi
"""
    launcher_path.write_text(launcher_content, encoding="utf-8")
    launcher_path.chmod(0o755)
    print(f"✓ Created launcher script: {launcher_path}")

    # 2. Install icon
    source_icon = workspace_dir / "src" / "pomodoro" / "assets" / "pomodoro.svg"
    target_icon = icon_scalable_dir / "pomodoro.svg"
    if source_icon.exists():
        shutil.copy2(source_icon, target_icon)
        print(f"✓ Installed icon to: {target_icon}")

    # 3. Create .desktop entry
    desktop_entry = f"""[Desktop Entry]
Type=Application
Name=Pomodoro
GenericName=Focus Timer
Comment=Minimalist Pomodoro Timer with To-Do list for Ubuntu GNOME
Exec={launcher_path}
Icon={target_icon}
Terminal=false
Categories=Utility;Office;Productivity;
StartupNotify=true
StartupWMClass=Pomodoro
Keywords=pomodoro;timer;focus;todo;productivity;
"""
    desktop_file = app_dir / "pomodoro.desktop"
    desktop_file.write_text(desktop_entry, encoding="utf-8")
    desktop_file.chmod(0o755)
    print(f"✓ Installed desktop entry: {desktop_file}")

    # 4. Update GNOME desktop database
    try:
        subprocess.run(
            ["update-desktop-database", str(app_dir)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        print("✓ Updated GNOME desktop database successfully")
    except Exception as e:
        print(f"! Notice: update-desktop-database exited with: {e}")

    print("\n🎉 Pomodoro is now installed as a native Ubuntu GNOME application!")
    print("You can search 'Pomodoro' in the Ubuntu Application menu (Super key) or pin it to your Ubuntu Dock.")


if __name__ == "__main__":
    install_desktop()
