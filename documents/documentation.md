# Holiday Bot Documentation

## About

Mimi Bot là Discord bot gửi lời chúc tự động vào ngày lễ và ngày sinh nhật tùy chỉnh. Bot hỗ trợ lịch Dương và lịch Âm qua thư viện lunardate. Admin cấu hình channel gửi tin, role tag (optional), loại lời chúc (Static/AI), và template tin nhắn tùy chỉnh. Bot chạy task hàng ngày lúc 7:00 để kiểm tra và gửi thông báo kèm nút tương tác ăn mừng.

### Tính năng chính (đã triển khai)

- Quản lý ngày lễ tùy chỉnh (Dương lịch/Âm lịch).
- Quản lý sinh nhật thành viên (Dương lịch/Âm lịch, lưu user_id và tên).
- Cấu hình theo server (channel, role, wish_type, template).
- Placeholder trong template: `{date_name}`, `{date}`, `{time}`, `{role_mention}`, `{everyone}`, `{here}`, `{guild}`.
- Nút button tương tác ăn mừng (ngăn click trùng lặp).
- Gửi lời chúc tự động hàng ngày.
- Đếm ngược cố định 5 ngày trước sinh nhật và Tết (Dương/Âm).
- Đếm ngược Tết theo tần suất (Monthly/Weekly) có thể cấu hình.
- Backup/restore cấu hình server.
- Lệnh test (wish, birthday, countdown).
- Lệnh announcement với modal (title, description, icon, image, footer) và preview.
- Lệnh admin: ping, restart, stop, sync, clear_cache.

### Mục đích sử dụng

- Tăng tương tác cộng đồng Discord vào dịp đặc biệt.
- Tự động hóa lời chúc và thông báo đếm ngược.

## Info

- **Phiên bản hiện tại**: 1.0.0.
- **Ngôn ngữ**: Python 3.8+ với discord.py (async).
- **Thư viện chính**:
  - `discord.py`
  - `lunardate`
  - `python-dotenv`
- **Lưu trữ dữ liệu**: File JSON cục bộ trong thư mục `json_config/`:
  - `holidays.json` (danh sách ngày lễ tùy chỉnh)
  - `birthdays.json` (danh sách sinh nhật)
  - `server_config.json` (cấu hình theo guild)
- **Yêu cầu hệ thống**:
  - Python 3.8+
  - File `.env` chứa `DISCORD_TOKEN` và `GUILD_ID` (tùy chọn để sync nhanh).
- **Quyền bot cần thiết**:
  - Send Messages
  - Manage Messages
  - Mention Everyone (nếu dùng @everyone)
  - Use Slash Commands
  - Read Message History

## Ngày lễ mặc định

### Dương lịch

- 01-01: Tết Dương Lịch
- 30-04: Giải phóng miền Nam
- 01-05: Quốc tế Lao động
- 02-09: Quốc khánh Việt Nam

### Âm lịch

- 01-01: Tết Nguyên Đán
- 15-08: Tết Trung Thu

## Yêu cầu hệ thống

- Python 3.8+
- Thư viện: `discord.py`, `lunardate`, `python-dotenv`.
- File `.env` chứa `DISCORD_TOKEN` và `GUILD_ID` (tùy chọn).

## Cài đặt

1. Tạo bot trên Discord Developer Portal và lấy token.
2. Cài dependencies: `pip install -r requirements.txt`.
3. Tạo file `.env`:
   ```env
   DISCORD_TOKEN=your_token_here
   GUILD_ID=your_guild_id_here
   ```
4. Chạy Run Bot: `py main.py`

## Hướng dẫn sử dụng

### Bot sử dụng `Slash Commands` phân nhóm.

1. Nhóm cấu hình `/config`

`/config setup`: Modal cài đặt ban đầu (role optional, channel, wish_type, template).
`/config view`: Xem cấu hình hiện tại.
`/config delete`: Xóa cấu hình server.
`/config export`: Xuất cấu hình server ra file JSON.
`/config import`: Nhập cấu hình từ file JSON.
`/config countdown`: Modal cấu hình đếm ngược Tết (tần suất, template birthday, template tet).

2. Nhóm thông tin `/info`

`/info view`: Xem thông tin server (ID, member count, created at).

3. Nhóm ngày lễ `/holiday`

`/holiday add`: Thêm ngày lễ (date DD-MM, name, type Solar/Lunar).
`/holiday list`: Xem danh sách ngày lễ.
`/holiday remove`: Xóa theo ngày DD-MM.
`/holiday update`: Cập nhật tên ngày lễ.

4. Nhóm ngày sinh nhật `/birthday`

`/birthday add`: Thêm sinh nhật (date DD-MM-YYYY, user optional mặc định là người dùng lệnh, type Solar/Lunar).
`/birthday list`: Xem danh sách sinh nhật (mention user).
`/birthday remove`: Xóa tất cả sinh nhật theo ngày DD-MM-YYYY.
`/birthday update`: Cập nhật tên lưu trữ cho sinh nhật theo ngày.

5. Công cụ & Test `/test group`

`/test wish [date_or_name]`: Test lời chúc (nếu không nhập thì dùng ngày hiện tại).
`/test birthday`: Modal nhập tên user để test lời chúc sinh nhật.
`/test countdown_birthday [user]`: Test đếm ngược sinh nhật cho user.
`/test countdown_tet`: Test báo cáo đếm ngược Tết Dương/Âm.

6. Lệnh khác

`/about`: Thông tin bot.
`/help`: Hướng dẫn sử dụng (embed chi tiết).
`/ping`: Kiểm tra latency.
`/announcement [channel] [mention]`: Modal tạo thông báo (title, description, icon, image, footer), preview, gửi vào channel chỉ định hoặc channel cấu hình.
`/restart, /stop, /clear_cache, /sync`: Lệnh admin.

## Cấu trúc dữ liệu

### Holidays (`holidays.json`)

Danh sách object: `{"date": "DD-MM", "name": "Tên", "type": "Solar"/"Lunar"}`

### Birthdays (`birthdays.json`)

Danh sách object: `{"user_id": int, "user_name": str, "date": "DD-MM-YYYY", "type": "Solar"/"Lunar"}`

### Server Config (`server_config.json`)

Object theo guild_id: `{"role_id": int/null, "channel_id": int, "wish_type": str, "content_template": str, "countdown": {frequency, template_birthday, template_tet}}`

## Mẫu tin nhắn (Template)

Placeholder:

- `{date_name}`: Tên sự kiện
- `{date}`: DD/MM/YYYY
- `{time}`: HH:MM
- `{role_mention}`: Tag role hoặc @everyone
- `{everyone}`, `{here}`
- `{guild}`: Tên server

Trong countdown: `{days}`, `{age}`, `{user}`

## Phân luồng workflow

### Khởi tạo

Admin dùng `/config setup`.

### Quản lý dữ liệu

- Thêm/sửa/xóa ngày lễ qua `/holiday`.
- Thêm/sửa/xóa sinh nhật qua `/birthday`.

### Vận hành hàng ngày (7:00)

1. Kiểm tra ngày hiện tại (Dương + Âm).
2. Gửi lời chúc lễ và sinh nhật trùng khớp (tên sự kiện: "Sinh nhật [tên]" cho sinh nhật).
3. Gửi đếm ngược cố định 5 ngày trước sinh nhật và Tết.
4. Gửi báo cáo đếm ngược Tết theo tần suất cấu hình (Monthly ngày 1 hoặc Weekly thứ Hai).

### Tương tác người dùng

Thành viên bấm nút "🎉 Ăn mừng ngay!" → bot trả lời công khai mention người bấm (ngăn click trùng).

### Announcement

Admin dùng `/announcement` → modal → preview → gửi vào channel chỉ định/cấu hình.

### Backup/Restore

Admin dùng `/config export` và `/config import` (chỉ cấu hình server).

## Tính năng đã triển khai (phiên bản hiện tại)

- Toàn bộ lệnh slash groups như mô tả.
- Gửi lời chúc lễ và sinh nhật tự động.
- Đếm ngược 5 ngày cố định và đếm ngược Tết có cấu hình.
- Announcement với preview.
- Test commands đầy đủ.
- Persistent button celebrate.
- Sync commands trong setup_hook.

## Tính năng chưa triển khai

- [ ] Đặt comment phân luồng chức năng theo group và theo chức năng con để dễ theo dõi, bảo trì
- [ ] Bảng chọn test birthday nên cho chọn user trong danh sách dữ liệu để test thay vì nhập tên.
- [ ] Thông báo lỗi hoặc ping hàng tuần vào channel riêng.
- [ ] Chưa có hỗ trợ đa ngôn ngữ hoàn chỉnh và slash command đa ngôn ngữ.
- [ ] Web dashboard.
- [ ] Lệnh `/config update` và `/config list`.
- [ ] `/info update`.
- [ ] Một số placeholder nâng cao trong announcement (emoji custom ID hướng dẫn).
- [ ] Countdown linh hoạt hơn (ví dụ trước 10/7 ngày).
- [ ] Gửi thông báo sai giờ (Bot không gửi thông báo ngày lúc 6h sáng mà lại gửi vào khung giờ 15h34 chiều).
- [ ] Thêm tính năng thông báo ngày, thời tiết, nhiệt độ hằng ngày, có group lệnh `/weather` để config.
- [ ] Cập nhật lại `/help` cho đầy đủ, thêm các thông tin về các tính năng chưa triển khai, sửa đổi khi sử dụng `/help` sẽ hiện model tổng quan thay vì gửi thông báo.
- [ ] Thêm nhóm lệnh xóa tin nhắn người dùng, có thuộc tính tùy chọn số lượng tin nhắn, thời gian, và kênh để xóa tin nhắn, người bị xóa tin nhắn, gửi thông báo xóa thành công `/clear message [amount] [time] [channel] [user]`, hiển thị placeholder hướng dẫn cho từng thuộc tính, và có thể chọn user trong danh sách dữ liệu để xóa tin nhắn của người đó, mặc định dùng `/clear message` sẽ xóa 10 tin nhắn gần nhất của user dùng lệnh và gửi thông báo xóa thành công.
