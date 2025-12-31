import os
import requests
from typing import Optional, Dict
from dotenv import load_dotenv

load_dotenv()

# OpenWeatherMap API key (có thể lấy miễn phí tại https://openweathermap.org/api)
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"

# Mapping thời tiết tiếng Việt
WEATHER_DESCRIPTIONS = {
    "clear sky": "trời quang đãng",
    "few clouds": "ít mây",
    "scattered clouds": "mây rải rác",
    "broken clouds": "mây cụm",
    "shower rain": "mưa rào",
    "rain": "mưa",
    "thunderstorm": "dông bão",
    "snow": "tuyết",
    "mist": "sương mù",
    "fog": "sương mù",
    "haze": "mù mịt",
    "dust": "bụi",
    "sand": "cát",
    "ash": "tro",
    "squall": "gió giật",
    "tornado": "lốc xoáy",
    "overcast clouds": "mây đen",
    "light rain": "mưa nhẹ",
    "moderate rain": "mưa vừa",
    "heavy intensity rain": "mưa to",
    "very heavy rain": "mưa rất to",
    "extreme rain": "mưa cực to",
    "freezing rain": "mưa đá",
    "light intensity drizzle": "mưa phùn nhẹ",
    "drizzle": "mưa phùn",
    "heavy intensity drizzle": "mưa phùn to",
    "light intensity shower rain": "mưa rào nhẹ",
    "heavy intensity shower rain": "mưa rào to",
    "ragged shower rain": "mưa rào dữ dội",
    "light snow": "tuyết nhẹ",
    "heavy snow": "tuyết dày",
    "sleet": "mưa tuyết",
    "light shower sleet": "mưa tuyết nhẹ",
    "shower sleet": "mưa tuyết",
    "light rain and snow": "mưa và tuyết nhẹ",
    "rain and snow": "mưa và tuyết",
    "light shower snow": "mưa tuyết nhẹ",
    "shower snow": "mưa tuyết",
    "heavy shower snow": "mưa tuyết dày",
    "smoke": "khói",
    "volcanic ash": "tro núi lửa",
}


def get_weather_description(weather_main: str, weather_description: str) -> str:
    """Chuyển đổi mô tả thời tiết sang tiếng Việt."""
    desc_lower = weather_description.lower()
    for key, value in WEATHER_DESCRIPTIONS.items():
        if key in desc_lower:
            return value
    # Fallback về mô tả chính
    main_lower = weather_main.lower()
    for key, value in WEATHER_DESCRIPTIONS.items():
        if key.startswith(main_lower):
            return value
    return weather_description


def get_weather(location: str) -> Optional[Dict]:
    """
    Lấy thông tin thời tiết từ OpenWeatherMap API.
    
    Args:
        location: Tên thành phố hoặc tọa độ (ví dụ: "Hanoi", "Ho Chi Minh City")
    
    Returns:
        Dict chứa thông tin thời tiết hoặc None nếu lỗi
    """
    if not WEATHER_API_KEY:
        return None
    
    try:
        params = {
            "q": location,
            "appid": WEATHER_API_KEY,
            "units": "metric",  # Nhiệt độ Celsius
            "lang": "vi"  # Ngôn ngữ tiếng Việt
        }
        
        response = requests.get(WEATHER_API_URL, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            weather_main = data["weather"][0]["main"]
            weather_desc = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            city_name = data["name"]
            country = data["sys"].get("country", "")
            
            return {
                "location": f"{city_name}, {country}",
                "temperature": round(temp),
                "feels_like": round(feels_like),
                "description": get_weather_description(weather_main, weather_desc),
                "humidity": humidity,
                "main": weather_main
            }
        else:
            return None
    except Exception as e:
        print(f"Lỗi khi lấy thời tiết: {e}")
        return None


def get_weather_message(location: str) -> str:
    """
    Tạo thông báo thời tiết đầy đủ.
    
    Args:
        location: Tên thành phố
    
    Returns:
        Chuỗi thông báo thời tiết
    """
    weather_data = get_weather(location)
    
    if not weather_data:
        return f"Không thể lấy thông tin thời tiết cho {location}. Vui lòng kiểm tra lại cấu hình."
    
    return (
        f"Thời tiết {weather_data['description']}, "
        f"nhiệt độ {weather_data['temperature']}°C "
        f"(cảm giác như {weather_data['feels_like']}°C)"
    )

