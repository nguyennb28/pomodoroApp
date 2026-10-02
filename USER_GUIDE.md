# 📖 Hướng Dẫn Sử Dụng Pomodoro Pro (User Guide)

Tài liệu hướng dẫn chi tiết cách sử dụng ứng dụng **Pomodoro Focus Timer** trên Ubuntu GNOME.

---

## 📑 Mục Lục
1. [Khởi Động Ứng Dụng Như Native App (Ubuntu GNOME)](#1-khởi-động-ứng-dụng-như-native-app-ubuntu-gnome)
2. [Giao Diện & Các Chế Độ Màn Hình](#2-giao-diện--các-chế-độ-màn-hình)
   - [Chế độ Cửa sổ kèm To-Do List (Windowed)](#chế-độ-cửa-sổ-kèm-to-do-list-windowed)
   - [Chế độ Widget nổi siêu gọn (Compact)](#chế-độ-widget-nổi-siêu-gọn-compact)
   - [Chế độ Toàn màn hình (Fullscreen Zen Mode - F11)](#chế-độ-toàn-màn-hình-fullscreen-zen-mode---f11)
3. [Quản Lý Công Việc (To-Do List & SQLite)](#3-quản-lý-công-việc-to-do-list--sqlite)
4. [Tùy Chỉnh Thời Gian Trực Tiếp Trên Giao Diện (Settings)](#4-tùy-chỉnh-thời-gian-trực-tiếp-trên-giao-diện-settings)
5. [Tích Hợp Khay Hệ Thống GNOME Topbar (System Tray)](#5-tích-hợp-khay-hệ-thống-gnome-topbar-system-tray)
6. [Bảng Phím Tắt Nhanh (Hotkeys)](#6-bảng-phím-tắt-nhanh-hotkeys)
7. [Hệ Thống Chuông Báo & Thông Báo](#7-hệ-thống-chuông-báo--thông-báo)
8. [Cơ Sở Dữ Liệu & Vị Trí Lưu Trữ](#8-cơ-sở-dữ-liệu--vị-trí-lưu-trữ)

---

## 1. Khởi Động Ứng Dụng Như Native App (Ubuntu GNOME)

Ứng dụng đã được tích hợp hoàn toàn vào hệ điều hành Ubuntu:

- **Khởi động từ menu Ubuntu:**
  1. Nhấn phím <kbd>Super</kbd> (phím Windows) trên bàn phím.
  2. Gõ **`Pomodoro`**.
  3. Nhấp vào biểu tượng trái cà chua 🍅 màu đỏ để mở ứng dụng!
  4. *(Tùy chọn)* Chuột phải vào biểu tượng trên Ubuntu Dock -> chọn **Add to Favorites** để ghim vào thanh Dock bên trái.
- **Hoặc chạy từ Terminal:**
  ```bash
  pomodoro-app
  # hoặc: uv run pomodoro
  ```

---

## 2. Giao Diện & Các Chế Độ Màn Hình

Ứng dụng hỗ trợ 3 chế độ hiển thị linh hoạt phù hợp với từng nhu cầu làm việc:

### Chế độ Cửa sổ kèm To-Do List (Windowed)
Bố cục 2 cột trực quan:
- **Cột trái:** Đồng hồ đếm ngược số lớn, huy hiệu Focus/Break, biểu ngữ hiển thị Task đang tập trung (`🎯 Write Documentation`), đèn chu kỳ 4 phiên (`● ● ○ ○`), số phiên hoàn thành hôm nay, và các nút điều khiển.
- **Cột phải:** Danh sách công việc (To-Do list) đồng bộ SQLite.

### Chế độ Widget nổi siêu gọn (Compact)
- Bấm nút **📋** (hoặc phím <kbd>T</kbd>) trên thanh công cụ để ẩn cột công việc.
- Cửa sổ tự động thu gọn thành một widget nổi nhỏ gọn (300x240px). Bạn có thể ghim ở góc màn hình và bật chế độ **📌 Always-on-Top** để theo dõi khi đang code hoặc duyệt web.

### Chế độ Toàn màn hình (Fullscreen Zen Mode - F11)
- Bấm nút **⛶** (hoặc phím <kbd>F11</kbd>) để vào chế độ Zen Mode.
- Toàn bộ màn hình biến thành không gian tập trung tối đa với đồng hồ cực lớn (120px) và tên nhiệm vụ cần hoàn thành. Loại bỏ 100% mọi yếu tố gây xao nhãng.
- Nhấn <kbd>F11</kbd> hoặc <kbd>Esc</kbd> để trở về chế độ cửa sổ bình thường.

---

## 3. Giao Diện Dracula Dark Mode & Light Mode

Ứng dụng cung cấp 2 phong cách giao diện:
- **Dracula Theme (Mặc định):** Màu nền tím than `#282a36`, điểm nhấn tím `#bd93f9` cho Focus và xanh lá `#50fa7b` cho Break. Cực kỳ êm mắt khi làm việc lâu trong bóng tối.
- **Light Theme (Chế độ Sáng):** Màu nền trắng tối giản `#ffffff`, chữ đen xám tương phản cao, hiện đại và sạch sẽ.
- **Cách đổi:** Bấm vào nút **☀️ / 🌙** ở góc trên bên phải. Trạng thái theme được lưu tự động vào SQLite.

---

## 4. Kéo Thả Cửa Sổ Bằng Chuột (Mouse Window Dragging)

- Bạn có thể **dùng chuột trái nhấn giữ bất kỳ khu vực nào** trên cửa sổ (thanh tiêu đề, vùng đồng hồ số lớn, nền bảng điều khiển, vùng thống kê) và di chuyển chuột để kéo thả cửa sổ đến góc màn hình mong muốn.
- Kéo thả hoạt động mượt mà ở cả chế độ Widget thu nhỏ và Cửa sổ mở rộng.

---

## 5. Quản Lý Công Việc (To-Do List & SQLite)

Toàn bộ công việc được lưu trữ bền vững trong cơ sở dữ liệu SQLite:

- **Thêm công việc:** Nhập tên nhiệm vụ vào ô *"Add a focus task & press Enter..."* và nhấn <kbd>Enter</kbd>.
- **Chọn nhiệm vụ đang tập trung (Active Focus):** Bấm nút **🎯** bên cạnh task. Biểu ngữ trên đồng hồ sẽ hiển thị rõ nhiệm vụ bạn đang làm.
- **Tự động đếm Pomodoro:** Mỗi khi bạn hoàn thành 1 phiên Focus 25 phút, task đang kích hoạt sẽ **tự động được cộng thêm 1 quả cà chua** (ví dụ: `🍅 3`).
- **Đánh dấu hoàn thành:** Bấm vào checkbox để gạch ngang task đã xong.
- **Xóa task:** Bấm nút **✕** ở cuối mỗi dòng.

---

## 4. Tùy Chỉnh Thời Gian Trực Tiếp Trên Giao Diện (Settings)

Không cần phải khởi động lại ứng dụng hay gõ lệnh:

1. Bấm vào biểu tượng bánh răng **⚙** ở góc phải thanh tiêu đề (hoặc chuột phải vào Topbar icon -> chọn *Settings...*).
2. Một hộp thoại thiết lập hiện ra cho phép bạn tinh chỉnh:
   - **Focus Time:** Thời gian tập trung (1 - 180 phút, mặc định: 25).
   - **Short Break:** Thời gian nghỉ ngắn (1 - 60 phút, mặc định: 5).
   - **Long Break:** Thời gian nghỉ dài (1 - 90 phút, mặc định: 15).
   - **Cycles:** Số phiên làm việc trước khi nghỉ dài (mặc định: 4).
3. Bấm **Save**: Cấu hình mới sẽ được lưu vĩnh viễn vào SQLite và áp dụng ngay lập tức cho phiên tiếp theo.

---

## 5. Tích Hợp Khay Hệ Thống GNOME Topbar (System Tray)

Ứng dụng tích hợp với thanh Topbar trên cùng của Ubuntu GNOME:

- **Biểu tượng quả cà chua:** Luôn hiển thị trên khay hệ thống cạnh đồng hồ và khay mạng của Ubuntu.
- **Tooltip thời gian thực:** Rê chuột vào icon để xem nhanh trạng thái hiện tại (ví dụ: `Pomodoro: Focus (18:42)`).
- **Chuột trái:** Click vào icon để ẩn hoặc hiện cửa sổ Pomodoro.
- **Chuột phải (Context Menu):** 
  - Xem trạng thái hiện tại.
  - Bật / Ẩn cửa sổ (`Show / Hide Window`).
  - Bắt đầu / Tạm dừng (`Start / Pause Timer`).
  - Bỏ qua phiên (`Skip Session`).
  - Mở cài đặt (`Settings...`).
  - Thoát ứng dụng hoàn toàn (`Quit Pomodoro`).
- **Chạy nền:** Bấm nút **✕** trên cửa sổ sẽ ẩn ứng dụng xuống thanh Topbar để tiếp tục đếm giờ mà không làm phiền màn hình làm việc của bạn.

---

## 6. Bảng Phím Tắt Nhanh (Hotkeys)

| Phím tắt | Thao tác | Chức năng |
| :---: | :--- | :--- |
| <kbd>Space</kbd> | **Start / Pause** | Bắt đầu hoặc tạm dừng đếm giờ |
| <kbd>R</kbd> | **Reset** | Khôi phục thời gian phiên hiện tại về ban đầu |
| <kbd>S</kbd> | **Skip** | Bỏ qua phiên hiện tại chuyển sang giai đoạn kế tiếp |
| <kbd>P</kbd> | **Pin / Unpin** | Bật hoặc tắt chế độ luôn nổi trên cùng (Always on Top) |
| <kbd>T</kbd> | **Toggle Tasks** | Ẩn / Hiện thanh danh sách công việc To-Do list |
| <kbd>F11</kbd> | **Fullscreen** | Chuyển đổi qua lại chế độ toàn màn hình Zen Mode |
| <kbd>Esc</kbd> | **Hide / Exit** | Thoát toàn màn hình hoặc ẩn cửa sổ xuống Topbar |

---

## 7. Hệ Thống Chuông Báo & Thông Báo

- **Âm thanh Chime thanh thoát:** Phát qua PipeWire / PulseAudio / ALSA khi hết giờ.
- **Thông báo Desktop Native:** Gửi thông báo hệ thống qua `notify-send` kèm âm thanh, tự động đưa cửa sổ Pomodoro lên trước mắt người dùng khi hết phiên.

---

## 8. Cơ Sở Dữ Liệu & Vị Trí Lưu Trữ

Toàn bộ dữ liệu được quản lý cục bộ an toàn:
- **Cơ sở dữ liệu SQLite:** `~/.local/share/pomodoro/pomodoro.db`
  - Bảng `tasks`: Danh sách nhiệm vụ và số Pomodoro đã hoàn thành.
  - Bảng `settings`: Thời lượng focus, nghỉ ngắn, nghỉ dài được tùy chỉnh.
  - Bảng `sessions`: Nhật ký lịch sử các phiên làm việc.
- **Tệp Desktop Launcher:** `~/.local/share/applications/pomodoro.desktop`
- **File thực thi:** `~/.local/bin/pomodoro-app`
- **Icon ứng dụng:** `~/.local/share/icons/hicolor/scalable/apps/pomodoro.svg`
