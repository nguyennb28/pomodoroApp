# 🍅 Pomodoro - Minimalist Desktop Focus Timer

Một ứng dụng Desktop Pomodoro tinh gọn, hiện đại và không gây phân tâm, được thiết kế theo triết lý **Strict Minimalism** và xây dựng trên nguyên lý **First Principles**.

---

## ✨ Tính năng nổi bật

- **Cửa sổ nổi Always-on-Top:** Thiết kế nhỏ gọn, có thể ghim trên cùng màn hình và kéo thả tự do đến bất kỳ góc nào mà không che khuất không gian làm việc.
- **Độ chính xác Monotonic:** Đếm giờ dựa trên `time.monotonic()` delta loại bỏ 100% hiện tượng trôi thời gian (clock drift).
- **Cảnh báo kép:**
  - **Âm thanh Chime thanh thoát:** Tự tổng hợp bằng sóng âm thanh (Dual-tone Harmonic Sine Wave), phát mượt mà qua PipeWire/PulseAudio/ALSA.
  - **Thông báo Desktop hệ điều hành:** Tích hợp với `notify-send` trên Linux.
- **Thống kê phiên làm việc:** Tự động lưu nhật ký các phiên hoàn thành vào `~/.local/share/pomodoro/stats.json`.
- **Chu kỳ Pomodoro chuẩn:** 4 phiên Focus (25m) xen kẽ Short Break (5m), sau đó là 1 phiên Long Break (15m). Đèn chỉ báo chu kỳ trực quan (`● ● ● ○`).

---

## ⌨️ Phím tắt nhanh (Hotkeys)

| Phím tắt | Chức năng |
| :---: | :--- |
| `Space` | **Bắt đầu / Tạm dừng** (Start / Pause) |
| `R` | **Đặt lại thời gian phiên hiện tại** (Reset) |
| `S` | **Bỏ qua phiên hiện tại** (Skip to next session) |
| `P` | **Bật / Tắt ghim luôn trên cùng** (Toggle Always on Top) |
| `Esc` / `Q` | **Đóng ứng dụng** (Close) |

---

## 🚀 Hướng dẫn cài đặt & khởi chạy

### Khởi chạy nhanh bằng `uv`
```bash
# Khởi chạy với cấu hình mặc định (25m focus, 5m break, 15m long break, 4 chu kỳ)
uv run pomodoro

# Hoặc tùy biến thời lượng (ví dụ: 50m làm việc, 10m nghỉ)
uv run pomodoro -w 50 -b 10 -l 20
```

### Chạy kiểm thử tự động
```bash
uv run pytest tests/
```
# pomodoroApp
