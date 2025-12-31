# HolidayWisherBot Specifications

## Project Info

| Field        | Value            |
| ------------ | ---------------- |
| Project Name | HolidayWisherBot |
| Version      | 1.0.0            |

---

## Core Features

### Configuration

| Field            | Description              |
| ---------------- | ------------------------ |
| Method           | Discord UI Modal         |
| role_id          | ID của role được mention |
| channel_id       | ID của kênh gửi lời chúc |
| wish_type        | static / ai              |
| content_template | Mẫu nội dung lời chúc    |

### Scheduler

| Field    | Value            |
| -------- | ---------------- |
| Interval | Daily            |
| Timezone | Asia/Ho_Chi_Minh |

### Holiday Database

| Supported Types | Examples       |
| --------------- | -------------- |
| International   | Christmas      |
| Vietnam_Solar   | Quốc Khánh     |
| Vietnam_Lunar   | Tết Nguyên Đán |

---

## Data Structure

### Guild Config Schema

| Field             | Type    | Description                          |
| ----------------- | ------- | ------------------------------------ |
| guild_id          | string  | Unique key cho mỗi server            |
| target_channel_id | integer | ID kênh gửi lời chúc                 |
| mention_role_id   | integer | ID role được mention                 |
| use_ai            | boolean | Có dùng AI để tạo lời chúc hay không |
| custom_prompt     | string  | Prompt tùy chỉnh cho AI              |
