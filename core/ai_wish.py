import random

# Mock database of wishes
WISH_DATABASE = {
    "vi": {
        "tet": [
            "Chúc mừng năm mới! Chúc bạn và gia đình an khang thịnh vượng, vạn sự như ý! 🌸",
            "Năm mới tết đến, chúc mọi người sức khỏe dồi dào, tiền vào như nước! 🧧",
            "Xuân sang rộn ràng, chúc bạn gặt hái được nhiều thành công trong năm mới nhé! 🥂",
            "Chúc mừng năm mới! Mong một năm tràn đầy niềm vui và may mắn. ✨"
        ],
        "birthday": [
            "Chúc mừng sinh nhật {user}! Chúc bạn tuổi mới thật nhiều niềm vui và thành công! 🎂",
            "Happy Birthday {user}! Chúc bạn hay ăn chóng lớn, tiền đầy túi, tình đầy tim! 🎉",
            "Sinh nhật vui vẻ nhé {user}! Chúc mọi điều ước của bạn đều thành hiện thực. 🎁",
            "Chúc mừng sinh nhật {mention_user}! Thêm tuổi mới, thêm nhiều thành công mới nha! 🥳"
        ],
        "default": [
            "Chúc mừng {date_name}! Chúc một ngày thật tuyệt vời! ✨",
            "Hôm nay là {date_name}, chúc mọi người có những giây phút vui vẻ! 🎈"
        ]
    },
    "en": {
        "tet": [
            "Happy New Year! Wishing you and your family prosperity and good health! 🌸",
            "Happy New Year! May this year bring you luck and success! 🧧"
        ],
        "birthday": [
            "Happy Birthday {user}! Wishing you a year filled with joy and success! 🎂",
            "Happy Birthday {user}! Hope your day is as special as you are! 🎉"
        ],
        "default": [
            "Happy {date_name}! Have a wonderful day! ✨"
        ]
    }
}

def generate_wish(event_name: str, event_type: str = "default", language: str = "vi", user_name: str = "", mention: str = "") -> str:
    """
    Generate a wish based on event type and language (Mock AI).
    
    Args:
        event_name: Name of the event (e.g., "Tết Nguyên Đán", "Sinh nhật")
        event_type: "tet", "birthday", or "default"
        language: "vi" or "en"
        user_name: Name of the user (for birthday)
        mention: Mention string (e.g. <@123>)
        
    Returns:
        A wish string.
    """
    lang_db = WISH_DATABASE.get(language, WISH_DATABASE["vi"])
    
    # Determine category
    category = "default"
    name_lower = event_name.lower()
    if "tết" in name_lower or "new year" in name_lower:
        category = "tet"
    elif "sinh nhật" in name_lower or "birthday" in name_lower:
        category = "birthday"
    
    templates = lang_db.get(category, lang_db['default'])
    template = random.choice(templates)
    
    # Replace placeholders
    wish = template.replace("{date_name}", event_name) \
                   .replace("{user}", user_name) \
                   .replace("{mention_user}", mention)
    
    return wish
