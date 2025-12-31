# Ghi chú Lỗi cần Sửa trong Holiday Bot

## Lỗi Hiện tại trong Codebase

### ✅ 1. Duplicate Entries trong birthdays.json - ĐÃ SỬA

- **Đã sửa**: Xóa duplicate entry cho user annie1101.

### ✅ 2. WEATHER_API_KEY trong .env - ĐÃ SỬA

- **Đã sửa**: Thêm validation cho API key format và detailed error handling.

### ✅ 3. Thiếu Error Handling trong weather_service.py - ĐÃ SỬA

- **Đã sửa**: Thêm logging chi tiết cho tất cả loại lỗi API (timeout, connection, auth, rate limit, parsing).

### 4. Bot có thể gửi thông báo sai giờ

### 4. Bot có thể gửi thông báo sai giờ

- **Vấn đề**: Theo documentation, bot gửi lúc 6h sáng nhưng code có DEFAULT_WISH_TIME = time(hour=6, minute=0)
- **Tác động**: Có thể gửi sai timezone hoặc timing
- **Giải pháp**: Đảm bảo timezone VN, test timing chính xác

### ✅ 5. Thiếu Validation trong date_utils.py - ĐÃ SỬA

- **Đã sửa**: Thêm validate_date() và normalize_date() trong date_utils.py, cập nhật birthday_cog.py và holiday_cog.py để validate và normalize dates trước khi lưu.

### ✅ 6. Restart Logic có thể fail - ĐÃ SỬA

- **Đã sửa**: Logic đã có error handling và cleanup cho restart_info.json, thêm logging chi tiết.

### ✅ 7. Thiếu Cleanup cho Persistent Views - ĐÃ SỬA

- **Đã sửa**: Thêm timeout 24 giờ cho CelebrateView và on_timeout để cleanup self.celebrated.

### ✅ 8. Holiday Matching Logic - ĐÃ SỬA

- **Đã sửa**: Thêm normalize_date để standardize date format, đảm bảo matching chính xác.

### ✅ 9. Weather Task chạy mỗi giờ, Các thông báo cài đặt giờ chưa chạy đúng timezone - ĐÃ SỬA

- **Đã sửa**: Thay đổi daily_check từ loop(time=DEFAULT_WISH_TIME) thành loop(hours=1) với kiểm tra giờ VN 6:00, đảm bảo chạy đúng timezone.

### ✅ 10. Thiếu Rate Limiting cho API calls - ĐÃ SỬA

- **Đã sửa**: Thêm cache với TTL 10 phút cho weather data, fallback to cached data khi rate limited.

### ✅ 11. Các vấn đề về thuộc tính của add, update, delete và các thuộc tính chung - ĐÃ SỬA

- **Đã sửa**: Thêm autocomplete cho date trong /birthday update, /birthday remove, /holiday update, /holiday remove để dễ select.

### ✅ 12. Đồng bộ các test, và thông báo weather - ĐÃ SỬA

- **Đã sửa**: Sửa test weather để hỗ trợ nhiều locations và tag role_mention giống thông báo thực.

## Tính năng Chưa Triển khai (Theo documentation)

### 1. Web Dashboard

- **Trạng thái**: Not implemented
- **Ưu tiên**: Low

### 2. Đa Ngôn ngữ

- **Trạng thái**: Not implemented
- **Ưu tiên**: Medium

### 3. Countdown Linh hoạt

- **Trạng thái**: Chỉ fixed 5 ngày
- **Ưu tiên**: Medium

### 4. Clear Message Command

- **Trạng thái**: Not implemented
- **Ưu tiên**: High (requested in docs)

### 5. Thông báo Ping hàng tuần

- **Trạng thái**: Not implemented
- **Ưu tiên**: Low

### 6. Update /config update và /config list

- **Trạng thái**: Not implemented
- **Ưu tiên**: Medium

### 7. /info update

- **Trạng thái**: Not implemented
- **Ưu tiên**: Low

### 8. Placeholder nâng cao trong announcement

- **Trạng thái**: Not implemented
- **Ưu tiên**: Low

### 9. Emoji custom ID trong announcement

- **Trạng thái**: Not implemented
- **Ưu tiên**: Low

## Performance Issues

### 1. Load JSON mỗi lần

- **Vấn đề**: load_json() được gọi nhiều lần trong loops
- **Giải pháp**: Cache data hoặc optimize loading

### 2. Large Guild Handling

- **Vấn đề**: Không test với large guilds
- **Giải pháp**: Thêm pagination cho lists

### 3. Memory Usage

- **Vấn đề**: Persistent views và data storage
- **Giải pháp**: Monitor và optimize memory

## Security Issues

### 1. Admin Permissions

- **Vấn đề**: Chỉ check has_permissions(administrator), có thể bypass
- **Giải pháp**: Thêm role-based access control

### 2. Input Validation

- **Vấn đề**: Thiếu sanitize cho user inputs trong templates
- **Giải pháp**: Sanitize inputs để tránh injection

### 3. API Key Exposure

- **Vấn đề**: WEATHER_API_KEY trong .env, có thể leak
- **Giải pháp**: Use environment variables properly

## Testing Gaps

### 1. Unit Tests

- **Trạng thái**: Không có unit tests
- **Giải pháp**: Thêm pytest cho core functions

### 2. Integration Tests

- **Trạng thái**: Manual testing only
- **Giải pháp**: Thêm automated integration tests

### 3. Load Testing

- **Trạng thái**: Not tested
- **Giải pháp**: Test với multiple concurrent users

## Documentation Issues

### 1. README.md

- **Vấn đề**: Có thể outdated
- **Giải pháp**: Update với current features

### 2. Code Comments

- **Vấn đề**: Thiếu comments trong một số functions
- **Giải pháp**: Add docstrings và comments

### 3. API Documentation

- **Vấn đề**: Không có API docs cho developers
- **Giải pháp**: Thêm swagger hoặc similar
