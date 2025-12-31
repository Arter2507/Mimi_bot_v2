# Kế hoạch Test các Chức năng của Holiday Bot

## 1. Cấu hình Server (/config group)

- [x] `/config setup`: Test modal nhập role_id, channel_id, wish_type, template
- [x] `/config view`: Xem cấu hình hiện tại
- [x] `/config export`: Xuất cấu hình ra file JSON
- [x] `/config import`: Nhập cấu hình từ file JSON
- [x] `/config delete`: Xóa cấu hình server
- [x] `/config countdown`: Test modal cấu hình countdown (frequency, template_birthday, template_tet)

## 2. Quản lý Ngày lễ (/holiday group)

- [x] `/holiday add`: Thêm ngày lễ mới (date DD-MM, name, type Solar/Lunar)
- [x] `/holiday list`: Xem danh sách ngày lễ
- [x] `/holiday remove`: Xóa ngày lễ theo date
- [x] `/holiday update`: Cập nhật tên ngày lễ

## 3. Quản lý Sinh nhật (/birthday group)

- [ ] `/birthday add`: Thêm sinh nhật (date DD-MM-YYYY, user optional, type Solar/Lunar)
- [ ] `/birthday list`: Xem danh sách sinh nhật với mention
- [ ] `/birthday remove`: Xóa sinh nhật theo date
- [ ] `/birthday update`: Cập nhật user name cho sinh nhật

## 4. Thông tin Bot (/info group)

- [ ] `/info view`: Xem thông tin server cơ bản
- [ ] `/about`: Thông tin về bot
- [ ] `/help`: Hướng dẫn sử dụng bot

## 5. Lệnh Test (/test)

- [ ] `/test wish`: Test gửi lời chúc với select holiday hoặc ngày hiện tại
- [ ] `/test birthday`: Test sinh nhật với select user từ danh sách
- [ ] `/test countdown_birthday`: Test đếm ngược sinh nhật với select user
- [ ] `/test countdown_tet`: Test báo cáo đếm ngược Tết
- [ ] `/test weather`: Test thông báo thời tiết

## 6. Lệnh Admin

- [ ] `/ping`: Kiểm tra latency
- [ ] `/restart`: Khởi động lại bot
- [ ] `/stop`: Tắt bot
- [ ] `/sync`: Sync slash commands
- [ ] `/clear_cache`: Xóa cache và reset commands
- [ ] `/announcement`: Tạo thông báo với modal và preview

## 7. Quản lý Thời tiết (/weather group)

- [ ] `/weather setup`: Cấu hình channel nhận thông báo
- [ ] `/weather add`: Thêm vị trí thời tiết
- [ ] `/weather list`: Xem danh sách vị trí
- [ ] `/weather update`: Cập nhật vị trí với autocomplete
- [ ] `/weather delete`: Xóa vị trí với autocomplete
- [ ] `/weather view`: Xem cấu hình thời tiết hiện tại
- [ ] `/weather test`: Test gửi thông báo thời tiết
- [ ] `/weather enable/disable`: Bật/tắt thông báo thời tiết

## 8. Background Tasks

- [ ] Daily Check Task: Gửi wish tự động lúc 6:00 sáng
- [ ] Weather Notification Task: Gửi thông báo thời tiết lúc 6:00 sáng
- [ ] Countdown Notifications: Gửi countdown 5 ngày trước và theo frequency

## 9. Views và Interactions

- [ ] CelebrateView: Button "🎉 Ăn mừng ngay!" với anti-spam
- [ ] AnnouncementConfirmView: Confirm/Cancel announcement
- [ ] TestWishView: Select holiday để test
- [ ] TestBirthdayView: Select user để test birthday
- [ ] TestCountdownBirthdayView: Select user để test countdown
- [ ] TestWeatherView: Button test weather
- [ ] WeatherChannelView: Select channel cho weather

## 10. Modals

- [ ] ConfigSetupModal: Cấu hình ban đầu
- [ ] CountdownConfigModal: Cấu hình countdown
- [ ] AnnouncementModal: Tạo announcement với preview
- [ ] WeatherLocationModal: Thêm vị trí thời tiết
- [ ] WeatherUpdateModal: Cập nhật vị trí thời tiết

## 11. Core Functions

- [ ] date_utils.py: Xử lý ngày Solar/Lunar, tính days until, age
- [ ] json_store.py: Load/save JSON an toàn
- [ ] weather_service.py: Lấy thông tin thời tiết từ OpenWeatherMap
- [ ] constants.py: Đường dẫn và constants

## 12. Validation và Error Handling

- [ ] Validate date formats (DD-MM, DD-MM-YYYY)
- [ ] Check permissions (administrator cho admin commands)
- [ ] Handle missing config
- [ ] Handle API errors (weather)
- [ ] Handle channel/role not found
- [ ] Timeout handling cho views/modals

## 13. Edge Cases

- [ ] Test với dữ liệu rỗng
- [ ] Test với duplicate entries
- [ ] Test với invalid inputs
- [ ] Test permissions
- [ ] Test khi bot offline/restart
- [ ] Test multiple guilds
- [ ] Test timezone handling (VN timezone)

## 14. Integration Tests

- [ ] End-to-end flow: Setup -> Add data -> Test -> Background tasks
- [ ] Multi-user interactions
- [ ] Concurrent operations
- [ ] Large datasets performance

## 15. Bug Fixes Completed ✅

- [x] **Lỗi 1**: Xóa duplicate entries trong birthdays.json (annie1101.)
- [x] **Lỗi 2**: Thêm validation cho WEATHER_API_KEY và error handling
- [x] **Lỗi 3**: Cải thiện error handling trong weather_service.py với detailed logging
- [x] **Lỗi 5**: Thêm validate_date() và normalize_date() trong date_utils.py, cập nhật birthday_cog.py và holiday_cog.py để validate và normalize dates trước khi lưu.
- [x] **Lỗi 6**: Logic restart đã có error handling và cleanup cho restart_info.json, thêm logging chi tiết.
- [x] **Lỗi 7**: Thêm timeout 24 giờ cho CelebrateView và on_timeout để cleanup self.celebrated.
- [x] **Lỗi 8**: Thêm normalize_date để standardize date format, đảm bảo matching chính xác.
- [x] **Lỗi 9**: Thay đổi daily_check từ loop(time=DEFAULT_WISH_TIME) thành loop(hours=1) với kiểm tra giờ VN 6:00, đảm bảo chạy đúng timezone.
- [x] **Lỗi 10**: Thêm cache với TTL 10 phút cho weather data, fallback to cached data khi rate limited.
- [x] **Lỗi 11**: Thêm autocomplete cho date trong /birthday update, /birthday remove, /holiday update, /holiday remove để dễ select.
- [x] **Lỗi 12**: Sửa test weather để hỗ trợ nhiều locations và tag role_mention giống thông báo thực.
