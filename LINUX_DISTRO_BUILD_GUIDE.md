# 🐧 Hướng Dẫn Đóng Gói Ứng Dụng Pomodoro Cho Mọi Bản Phân Phối Linux (Cross-Distro Build Guide)

Tài liệu này hướng dẫn chi tiết cách build và đóng gói ứng dụng **Pomodoro** để phân phối và chạy trên bất kỳ bản phân phối Linux nào (Ubuntu, Debian, Fedora, Arch Linux, openSUSE, Manjaro, Pop!_OS, Alpine,...).

---

## 📑 Mục Lục
1. [Bảng So Sánh Các Giải Pháp Phân Phối](#1-bảng-so-sánh-các-giải-pháp-phân-phối)
2. [Yêu Cầu Thư Viện Hệ Thống Theo Từng Distro](#2-yêu-cầu-thư-viện-hệ-thống-theo-từng-distro)
3. [Phương Pháp 1: Build Single Executable Binary (PyInstaller) - Khuyên Dùng](#3-phương-pháp-1-build-single-executable-binary-pyinstaller---khuyên-dùng)
4. [Phương Pháp 2: Đóng Gói AppImage (Chạy 1 Click Mọi Distro)](#4-phương-pháp-2-đóng-gói-appimage-chạy-1-click-mọi-distro)
5. [Phương Pháp 3: Đóng Gói Native Package (.deb & .rpm)](#5-phương-pháp-3-đóng-gói-native-package-deb--rpm)
6. [Phương Pháp 4: Phân Phối Chuẩn Python (pipx / uv tool)](#6-phương-pháp-4-phân-phối-chuẩn-python-pipx--uv-tool)
7. [Tích Hợp Desktop Cho Các Desktop Environment Khác (KDE, XFCE, Hyprland)](#7-tích-hợp-desktop-cho-các-desktop-environment-khác-kde-xfce-hyprland)

---

## 1. Bảng So Sánh Các Giải Pháp Phân Phối

| Phương pháp | Định dạng | Ưu điểm | Đối tượng người dùng |
| :--- | :---: | :--- | :--- |
| **PyInstaller Binary** | File binary đơn | Không cần cài đặt Python hay thư viện, chạy ngay bằng lệnh hoặc click đúp. | Người dùng mọi bản Linux |
| **AppImage** | `.AppImage` | Chuẩn đóng gói độc lập phổ biến nhất, tích hợp icon, metadata, chỉ cần cấp quyền thực thi là chạy. | Người dùng phổ thông, mọi distro |
| **Debian / Ubuntu Package** | `.deb` | Tích hợp sâu vào trình quản lý gói `apt` / `dpkg`, tự động cập nhật và gỡ cài đặt sạch sẽ. | Debian, Ubuntu, Mint, Pop!_OS |
| **Fedora / RedHat Package** | `.rpm` | Tích hợp vào `dnf` / `rpm`, chuẩn mực cho hệ sinh thái Red Hat. | Fedora, RHEL, openSUSE |
| **Python Tool** | `pipx` / `uv` | Siêu nhẹ, cập nhật tức thì từ mã nguồn, cách ly môi trường hoàn hảo. | Lập trình viên, Power Users |

---

## 2. Yêu Cầu Thư Viện Hệ Thống Theo Từng Distro

Pomodoro sử dụng **Qt6 (PyQt6)**, **SQLite** (tích hợp sẵn trong Python), **Desktop Notifications**, và **Audio Playback**. Dưới đây là lệnh cài đặt các gói hỗ trợ hệ thống cho từng bản phân phối:

### Ubuntu / Debian / Pop!_OS / Linux Mint
```bash
sudo apt update
sudo apt install -y python3 python3-pip libnotify-bin pipewire-audio-client-libraries alsa-utils
```

### Fedora / RHEL / AlmaLinux / Rocky Linux
```bash
sudo dnf install -y python3 python3-pip libnotify pipewire-utils alsa-utils
```

### Arch Linux / Manjaro / EndeavourOS
```bash
sudo pacman -Syu --needed python python-pip libnotify pipewire-pulse alsa-utils
```

### openSUSE (Tumbleweed / Leap)
```bash
sudo zypper install python3 python3-pip libnotify-tools pipewire-pulseaudio alsa-utils
```

---

## 3. Phương Pháp 1: Build Single Executable Binary (PyInstaller) - Khuyên Dùng

PyInstaller sẽ đóng gói toàn bộ mã nguồn Python, Qt6 runtime, và các file thư viện liên quan thành **duy nhất một file thực thi nhị phân (binary)** độc lập. Người nhận file không cần cài đặt Python.

### Các bước thực hiện:

1. **Cài đặt PyInstaller vào môi trường dev:**
   ```bash
   uv add --dev pyinstaller
   ```

2. **Chạy lệnh build nhị phân độc lập:**
   ```bash
   uv run pyinstaller \
       --name pomodoro \
       --onefile \
       --windowed \
       --add-data "src/pomodoro/assets:pomodoro/assets" \
       src/pomodoro/main.py
   ```

3. **Kết quả:**
   File binary độc lập sẽ xuất hiện tại:
   ```bash
   dist/pomodoro
   ```

4. **Kiểm tra và chạy thử trên bất kỳ máy Linux nào:**
   ```bash
   chmod +x dist/pomodoro
   ./dist/pomodoro
   ```

---

## 4. Phương Pháp 2: Đóng Gói AppImage (Chạy 1 Click Mọi Distro)

AppImage là định dạng "chạy ở mọi nơi" chuẩn của Linux. Ứng dụng được đóng gói kèm toàn bộ runtime thành 1 file duy nhất `Pomodoro-x86_64.AppImage`.

### Cách tạo AppImage đơn giản với `appimagetool`:

1. **Tải `appimagetool`:**
   ```bash
   wget -O appimagetool "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
   chmod +x appimagetool
   ```

2. **Chuẩn bị cấu trúc thư mục AppDir:**
   ```bash
   mkdir -p AppDir/usr/bin
   mkdir -p AppDir/usr/share/applications
   mkdir -p AppDir/usr/share/icons/hicolor/scalable/apps

   # Copy file binary từ PyInstaller vào AppDir
   cp dist/pomodoro AppDir/usr/bin/pomodoro

   # Copy Icon và Desktop file
   cp src/pomodoro/assets/pomodoro.svg AppDir/usr/share/icons/hicolor/scalable/apps/pomodoro.svg
   cp src/pomodoro/assets/pomodoro.svg AppDir/pomodoro.svg

   # Tạo file AppDir/pomodoro.desktop
   cat << 'EOF' > AppDir/pomodoro.desktop
   [Desktop Entry]
   Type=Application
   Name=Pomodoro
   Exec=pomodoro
   Icon=pomodoro
   Categories=Utility;Office;Productivity;
   EOF

   # Tạo AppRun (Entry point)
   cat << 'EOF' > AppDir/AppRun
   #!/bin/sh
   SELF=$(dirname "$(readlink -f "$0")")
   export PATH="$SELF/usr/bin:$PATH"
   exec "$SELF/usr/bin/pomodoro" "$@"
   EOF
   chmod +x AppDir/AppRun
   ```

3. **Đóng gói thành file `.AppImage`:**
   ```bash
   ./appimagetool AppDir Pomodoro-x86_64.AppImage
   ```

Bây giờ bạn có thể gửi file `Pomodoro-x86_64.AppImage` này cho người dùng Fedora, Arch, openSUSE, v.v. Họ chỉ cần click đúp là ứng dụng chạy ngay lập tức!

---

## 5. Phương Pháp 3: Đóng Gói Native Package (.deb & .rpm)

Sử dụng công cụ đa năng **`fpm`** (Effing Package Management) để xuất file `.deb` hoặc `.rpm` chỉ trong 1 lệnh duy nhất:

### Đóng gói `.deb` (Cho Debian, Ubuntu, Linux Mint):
```bash
# Cài đặt fpm (yêu cầu ruby)
sudo apt install -y ruby ruby-dev rubygems build-essential
sudo gem install --no-document fpm

# Đóng gói file binary dist/pomodoro thành .deb
fpm -s dir -t deb \
    -n pomodoro \
    -v 0.1.0 \
    --description "Minimalist Pomodoro Focus Timer" \
    dist/pomodoro=/usr/bin/pomodoro \
    src/pomodoro/assets/pomodoro.svg=/usr/share/icons/hicolor/scalable/apps/pomodoro.svg

# Cài đặt thử nghiệm:
sudo dpkg -i pomodoro_0.1.0_amd64.deb
```

### Đóng gói `.rpm` (Cho Fedora, RHEL, openSUSE):
```bash
fpm -s dir -t rpm \
    -n pomodoro \
    -v 0.1.0 \
    --description "Minimalist Pomodoro Focus Timer" \
    dist/pomodoro=/usr/bin/pomodoro \
    src/pomodoro/assets/pomodoro.svg=/usr/share/icons/hicolor/scalable/apps/pomodoro.svg

# Cài đặt thử nghiệm trên Fedora:
sudo dnf install ./pomodoro-0.1.0-1.x86_64.rpm
```

---

## 6. Phương Pháp 4: Phân Phối Chuẩn Python (pipx / uv tool)

Đối với người dùng đã cài sẵn Python trên bất kỳ hệ điều hành Linux nào, phương pháp phân phối qua `pipx` hoặc `uv tool` là sạch sẽ và thuận tiện nhất vì không gây xung đột thư viện hệ thống (PEP 668):

```bash
# 1. Cài đặt trực tiếp từ mã nguồn hoặc Git repository:
pipx install .

# Hoặc dùng uv:
uv tool install .
```

Sau khi cài đặt, người dùng có thể gõ lệnh `pomodoro` ở bất kỳ thư mục nào trên terminal hoặc tạo launcher tương ứng.

---

## 7. Tích Hợp Desktop Cho Các Desktop Environment Khác

Ngoài GNOME, các Desktop Environment khác trên Linux cũng tuân theo chuẩn **XDG Desktop Entry Specification**:

### 1. KDE Plasma (Kubuntu, Fedora KDE, Arch KDE)
- File desktop đặt tại: `~/.local/share/applications/pomodoro.desktop`.
- Icon đặt tại: `~/.local/share/icons/hicolor/scalable/apps/pomodoro.svg`.
- Khay hệ thống: KDE Plasma hỗ trợ `QSystemTrayIcon` trực tiếp và mượt mà hơn cả GNOME (không cần cài thêm extension).

### 2. XFCE / Cinnamon / MATE
- Tương thích 100% với file `.desktop` và system tray hiện tại.
- Cập nhật menu bằng:
  ```bash
  update-desktop-database ~/.local/share/applications
  ```

### 3. Tiling Window Managers (i3, Sway, Hyprland)
Người dùng i3/Sway/Hyprland thường sử dụng launcher như `rofi`, `wofi`, hoặc `tofi`:
- Ứng dụng tự động xuất hiện trong danh sách tìm kiếm của `rofi` / `wofi` sau khi cài file `.desktop`.
- Có thể thêm quy tắc cửa sổ nổi (floating rule) cho Pomodoro trong file cấu hình:
  - **Hyprland** (`~/.config/hypr/hyprland.conf`):
    ```ini
    windowrule = float, ^(Pomodoro)$
    windowrule = pin, ^(Pomodoro)$
    ```
  - **i3 / Sway** (`~/.config/i3/config` hoặc `~/.config/sway/config`):
    ```ini
    for_window [class="Pomodoro"] floating enable, sticky enable
    ```

---

## 💡 Tổng Kết Khuyên Dùng:
- **Nếu muốn chia sẻ nhanh cho bạn bè dùng bất kỳ distro nào:** Hãy dùng **Phương pháp 1 (PyInstaller)** để tạo 1 file nhị phân duy nhất, hoặc **Phương pháp 2 (AppImage)**.
- **Nếu muốn đưa lên kho phần mềm chính thức:** Hãy tạo file `.deb` cho Debian/Ubuntu PPA và `.rpm` cho Fedora COPR.
