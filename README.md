# 🤖 Mimi Bot v2.0

Mimi Bot là một Discord bot mạnh mẽ được thiết kế để tự động hóa việc gửi lời chúc ngày lễ, sinh nhật và cập nhật thời tiết hàng ngày. Với sự hỗ trợ của AI và đa ngôn ngữ, Mimi Bot mang lại trải nghiệm tương tác tuyệt vời cho Server Discord của bạn.

## ✨ Tính Năng Nổi Bật

- **AI Wish Generation**: Tự động tạo lời chúc phong phú, không trùng lặp cho các dịp đặc biệt.
- **Hỗ Trợ Đa Ngôn Ngữ**: Tùy chỉnh ngôn ngữ hiển thị (Tiếng Việt 🇻🇳 / English 🇺🇸).
- **Cấu Hình Đếm Ngược Linh Hoạt**: Cấu hình số ngày báo trước tùy ý (VD: 10, 7, 5 ngày) cho Tết và Sinh nhật.
- **Thông Báo Thời Tiết**: Cập nhật thời tiết hàng ngày với giao diện đẹp mắt, emoji sinh động.
- **Quản Lý Sinh Nhật & Ngày Lễ**: Hỗ trợ cả lịch Dương và lịch Âm (Lunar date).
- **Hệ Thống Lệnh /Config Gọn Gàng**: Toàn bộ cài đặt được tích hợp trong một lệnh duy nhất.
- **Thông Báo Tùy Chỉnh**: Tạo thông báo (announcement) chuyên nghiệp với preview.

## 🚀 Cài Đặt

1. **Clone repository:**

   ```bash
   git clone https://github.com/Arter2507/Mimi_bot_v2.git
   cd Mimi_bot_v2
   ```

2. **Cài đặt dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Cấu hình biến môi trường:**
   Tạo file `.env` tại thư mục gốc:

   ```env
   DISCORD_TOKEN=your_bot_token_here
   WEATHER_API_KEY=your_openweathermap_api_key_here
   ```

4. **Khởi chạy bot:**
   ```bash
   python main.py
   ```

## 🛠️ Hướng Dẫn Sử Dụng

### Cài đặt ban đầu

Sử dụng lệnh `/config Setup` để thiết lập channel gửi tin nhắn, role tag và loại lời chúc (Static/AI).

### Các lệnh quan trọng

- `/config`: Menu cấu hình tổng hợp (Ngôn ngữ, Thời gian, Countdown, Backup...).
- `/birthday add`: Thêm ngày sinh nhật (Dương/Âm).
- `/holiday add`: Thêm ngày lễ tùy chỉnh.
- `/weather`: Quản lý thông báo thời tiết.
- `/help`: Xem hướng dẫn chi tiết theo quyền hạn.

## 📁 Cấu Trúc Thư Mục

- `bot.py`: Logic cốt lõi của bot và các task chạy ngầm.
- `cogs/`: Chứa các module lệnh (Config, Weather, Birthday, Info...).
- `core/`: Các dịch vụ xử lý (AI Wish, i18n, Weather service).
- `modals/`: Các giao diện nhập liệu (Modal).
- `views/`: Các thành phần giao diện tương tác (Button, View).
- `documents/`: Tài liệu hướng dẫn chi tiết.

## 📄 Tài Liệu

Xem tài liệu chi tiết tại [documentation.md](documents/documentation.md).

## 🤝 Đóng Góp

Nếu bạn có ý tưởng hoặc gặp lỗi, vui lòng tạo Issue hoặc Gửi Pull Request!

---

_Mimi Bot - Gắn kết cộng đồng qua từng lời chúc._
