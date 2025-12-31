holiday_notification_bot/
│
├─ reset_commands.py
│ └─ Reset lại các command của bot
│
├─ main.py
│ └─ Entry point khởi chạy bot (python main.py)
│
├─ bot.py
│ └─ Định nghĩa class HolidayBot, load cogs, sync slash commands
│
├─ .env
│ └─ Biến môi trường (DISCORD_TOKEN, DEBUG, …)
│
├─ README.md
│ └─ Mô tả dự án, cách cài đặt, cách chạy bot
│
├─ core/
│ ├─ **init**.py
│ │ └─ Đánh dấu package core
│ │
│ ├─ constants.py
│ │ └─ Hằng số dùng toàn hệ thống
│ │ (đường dẫn JSON, DEFAULT_WISH_TIME, …)
│ │
│ ├─ json_store.py
│ │ └─ Hàm load_json / save_json
│ │ (đọc ghi file JSON an toàn)
│ │
│ └─ date_utils.py
│ └─ Logic xử lý ngày tháng
│ (is_today, days_until, chuyển đổi ngày âm/dương)
│
├─ cogs/
│ ├─ **init**.py
│ │ └─ Đánh dấu package cogs
│ │
│ ├─ admin_cog.py
│ │ └─ Lệnh quản trị
│ │ (/announce, chức năng admin)
│ │
│ ├─ birthday_cog.py
│ │ └─ Lệnh liên quan sinh nhật
│ │ (/birthdays, quản lý dữ liệu sinh nhật)
│ │
│ ├─ config_cog.py
│ │ └─ Lệnh cấu hình server
│ │ (/setup, /countdown_config)
│ │
│ ├─ holiday_cog.py
│ │ └─ Lệnh xem / quản lý ngày lễ
│ │ (/holidays)
│ │
│ ├─ info_cog.py
│ │ └─ Lệnh thông tin bot
│ │ (/botinfo)
│ │
│ └─ test_cog.py
│ └─ Lệnh test, kiểm tra bot
│ (/ping)
│
├─ modals/
│ ├─ **init**.py
│ │ └─ Đánh dấu package modals
│ │
│ ├─ config_setup.py
│ │ └─ Modal cấu hình server ban đầu
│ │ (channel, role, template)
│ │
│ ├─ countdown_config.py
│ │ └─ Modal cấu hình countdown
│ │ (tần suất, template đếm ngược)
│ │
│ └─ announcement_modal.py
│ └─ Modal tạo thông báo embed
│ (title, content, image, footer)
│
├─ views/
│ ├─ **init**.py
│ │ └─ Đánh dấu package views
│ │
│ ├─ celebrate_view.py
│ │ └─ View (Button / UI) cho chúc mừng, xác nhận
│ │
│ └─ announcement_view.py
│ └─ View xác nhận gửi thông báo
│ (Confirm / Cancel)
│
├─ tasks/
│ ├─ **init**.py
│ │ └─ Đánh dấu package tasks
│ │
│ └─ daily_check.py
│ └─ Background task chạy định kỳ
│ (check ngày lễ, sinh nhật, gửi thông báo)
│
└─ json_config/
├─ holidays.json
│ └─ Dữ liệu ngày lễ (tĩnh, dùng chung)
│
├─ birthdays.json
│ └─ Dữ liệu sinh nhật người dùng
│
└─ server_config.json
└─ Cấu hình riêng cho từng server (guild)
