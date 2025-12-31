# Mimi Bot Documentation

## About

Mimi Bot là Discord bot gửi lời chúc tự động vào ngày lễ, sinh nhật và thông báo thời tiết hằng ngày. Bot hỗ trợ lịch Dương và lịch Âm qua thư viện lunardate. Admin cấu hình channel gửi tin, role tag (optional), loại lời chúc (Static/AI), template tin nhắn tùy chỉnh, thời gian thông báo và ngôn ngữ.

### Tính năng chính (đã triển khai)

- **AI Wish Generation**: Tự động tạo lời chúc phong phú cho dịp lễ/sinh nhật (nếu chọn Wish Type = AI).
- **Multi-language Support**: Hỗ trợ Tiếng Việt (default) và English.
- **Flexible Countdown**: Cấu hình số ngày báo trước tùy ý (VD: 5, 7, 10 ngày).
- **Weather Notification**: Thông báo thời tiết hằng ngày với format đẹp, nhiều dòng.
- **Configurable Notification Time**: Tùy chỉnh giờ gửi thông báo hằng ngày.
- Quản lý ngày lễ tùy chỉnh và sinh nhật thành viên (Dương/Âm).
- Cấu hình theo server (channel, role, language, v.v.).
- Placeholder phong phú: `{user}`, `{mention_user}`, `{age}`, `{days}`, v.v.
- Backup/restore cấu hình JSON.

### Mục đích sử dụng

- Tăng tương tác cộng đồng Discord vào dịp đặc biệt.
- Tự động hóa lời chúc và thông báo đếm ngược.
- Thông báo thời tiết hằng ngày.

## Info

- **Phiên bản hiện tại**: 1.2.0 (Phase 2 Update)
- **Ngôn ngữ**: Python 3.8+ với discord.py (async).
- **Lưu trữ dữ liệu**: JSON Configs (`server_config.json`, `holidays.json`, `birthdays.json`).

## Hướng dẫn sử dụng

### Lệnh Config (`/config [function]`)

Menu cấu hình tổng hợp:

- `/config Setup` - Cài đặt cơ bản: Channel, Role, Wish Type (Static/AI), Template.
- `/config Language` - **[NEW]** Chọn ngôn ngữ hiển thị (Tiếng Việt / English).
- `/config Countdown` - **[UPDATE]** Cấu hình đếm ngược và **Số ngày báo trước** (VD: 5, 10).
- `/config Notification Time` - Cấu hình giờ gửi thông báo (HH:MM).
- `/config Log Channel` - Cấu hình channel ghi log (khởi động, lỗi).
- `/config View` - Xem toàn bộ cấu hình.
- `/config Export` / `Import` - Sao lưu và khôi phục cấu hình.
- `/config Delete` - Xóa cấu hình server.

### Lệnh Ngày lễ (`/holiday`)

- `/holiday add` - Thêm ngày lễ (modal).
- `/holiday list` - Xem danh sách.
- `/holiday remove` - Xóa ngày lễ.
- `/holiday update` - Sửa tên ngày lễ.

### Lệnh Sinh nhật (`/birthday`)

- `/birthday add [date] [user] [type]` - Thêm sinh nhật.
- `/birthday list` - Xem danh sách.
- `/birthday remove` - Xóa sinh nhật.
- `/birthday update` - Cập nhật thông tin.

### Lệnh Thời tiết (`/weather`)

- `/weather setup` - Chọn channel.
- `/weather add` - Thêm vị trí.
- `/weather list`, `/weather view` - Xem danh sách/cấu hình.
- `/weather update`, `/weather delete`.
- `/weather enable` / `disable`.
- **Note**: Lệnh `/weather test` đã bị xóa (dùng `/test Weather` thay thế).

### Lệnh Test (`/test`)

- `/test Wish` - Test lời chúc (Static/AI).
- `/test Birthday` - Test chúc mừng sinh nhật.
- `/test Countdown Birthday/Tet`.
- `/test Weather`.

### Lệnh Khác

- `/help` - Xem hướng dẫn chi tiết.
- `/info view`, `/about`, `/ping`.
- `/clear message` - Xóa tin nhắn hàng loạt.
- `/announcement` - Tạo thông báo custom.

## Cấu trúc Config Mới (`server_config.json`)

```json
{
  "guild_id": {
    "language": "vi",  // vi hoặc en
    "wish_type": "AI", // Static hoặc AI
    "notification_time": {"hour": 7, "minute": 30},
    "countdown": {
      "frequency": "Monthly",
      "days_before": [5, 10], // List các ngày báo trước
      "template_birthday": "...",
      "template_tet": "..."
    },
    "weather": { ... }
  }
}
```

## Template Mặc định Mới

- **Birthday**: `🎂 Chúc mừng Sinh nhật {user} {mention_user}! @everyone`
  - Tag user trực tiếp để nhận thông báo.

## Tính năng đã triển khai

- [x] AI Wish Generation (Mock Service)
- [x] Multi-language Support (Config & Core)
- [x] Flexible Countdown Days
- [x] Updated Birthday Template
- [x] Weather Notification Format (Multi-line)
- [x] Consolidated Config Commands
- [x] Notification Time Config

## Tính năng chưa triển khai

- [ ] Web Dashboard quản lý trực quan.
- [ ] Integration với Real AI API (OpenAI/Gemini) thay vì Mock.
- [ ] Custom timezone (hiện tại fixed Asia/Ho_Chi_Minh).
