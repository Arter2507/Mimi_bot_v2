# Localization Dictionary

LANG = {
    "vi": {
        "config_saved": "✅ Đã lưu cấu hình server.",
        "config_deleted": "✅ Đã xóa cấu hình server.",
        "config_not_found": "❌ Không tìm thấy cấu hình.",
        "config_error": "❌ Có lỗi xảy ra.",
        "only_admin": "❌ Chỉ admin mới có thể thực hiện lệnh này.",
        "invalid_file": "❌ File không hợp lệ.",
        "success": "✅ Thành công!",
        "error": "❌ Lỗi: {}",
        "language_set": "✅ Đã chuyển sang ngôn ngữ: Tiếng Việt 🇻🇳",
        "weather_notify_header": "☀️ **Thông báo thời tiết - {}, {}**",
        "weather_good_day": "Chúc một ngày tốt lành! {}",
    },
    "en": {
        "config_saved": "✅ Server configuration saved.",
        "config_deleted": "✅ Server configuration deleted.",
        "config_not_found": "❌ Configuration not found.",
        "config_error": "❌ An error occurred.",
        "only_admin": "❌ Only admins can execute this command.",
        "invalid_file": "❌ Invalid file.",
        "success": "✅ Success!",
        "error": "❌ Error: {}",
        "language_set": "✅ Language switched to: English 🇺🇸",
        "weather_notify_header": "☀️ **Weather Notification - {}, {}**",
        "weather_good_day": "Have a nice day! {}",
    }
}

def get_text(key: str, lang: str = "vi", **kwargs) -> str:
    """
    Get localized text.
    
    Args:
        key: Key in LANG dict.
        lang: Language code ("vi" or "en").
        **kwargs: Format arguments.
        
    Returns:
        Localized string.
    """
    # Fallback to 'vi' if lang not found
    lang_dict = LANG.get(lang, LANG["vi"])
    # Fallback to key if key not found
    text = lang_dict.get(key, key)
    
    if kwargs:
        try:
            return text.format(**kwargs)
        except Exception:
            return text
    return text
