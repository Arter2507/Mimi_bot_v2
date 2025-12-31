import discord
from discord.ext import commands
from core.json_store import load_json
from core.constants import BIRTHDAYS_JSON, HOLIDAYS_JSON
from core.date_utils import get_days_until_solar, get_days_until_lunar, get_age


class HolidaySelect(discord.ui.Select):
    """Select menu cho holidays."""
    
    def __init__(self, bot, guild, channel):
        holidays = load_json(HOLIDAYS_JSON)
        
        options = [
            discord.SelectOption(
                label="📅 Ngày hiện tại",
                value="today",
                description="Test với các sự kiện của ngày hôm nay"
            )
        ]
        
        # Thêm options từ danh sách holidays
        for holiday in holidays:
            holiday_name = holiday.get('name', 'Unknown')
            holiday_date = holiday.get('date', 'N/A')
            holiday_type = holiday.get('type', 'Solar')
            label = f"{holiday_name} ({holiday_date} - {holiday_type})"
            # Giới hạn label length
            if len(label) > 100:
                label = label[:97] + "..."
            options.append(
                discord.SelectOption(
                    label=label,
                    value=holiday_name,
                    description=f"Test wish cho {holiday_name}"
                )
            )
        
        super().__init__(
            placeholder="Chọn ngày lễ hoặc 'Ngày hiện tại'...",
            min_values=1,
            max_values=1,
            options=options
        )
        
        self.bot = bot
        self.guild = guild
        self.channel = channel
    
    async def callback(self, interaction: discord.Interaction):
        """Xử lý khi chọn holiday."""
        selected_value = self.values[0]
        
        if selected_value == "today":
            # Test với ngày hiện tại
            await interaction.response.defer(ephemeral=True)
            await self.bot.check_events_for_guild(
                self.guild,
                manual_trigger=True,
                interaction_ctx=None  # Không gửi thông báo test
            )
            await interaction.followup.send("✅ Đã gửi test wish cho ngày hiện tại!", ephemeral=True)
        else:
            # Test với holiday cụ thể
            holiday_name = selected_value
            await interaction.response.defer(ephemeral=True)
            await self.bot.send_wish(self.guild, holiday_name, "Test", None)  # Không gửi thông báo test
            await interaction.followup.send(f"✅ Đã gửi test wish cho: {holiday_name}!", ephemeral=True)


class TestWishView(discord.ui.View):
    """View để test wish với menu chọn holiday."""
    
    def __init__(self, bot, guild, channel):
        super().__init__(timeout=300)
        self.add_item(HolidaySelect(bot, guild, channel))
    
    async def on_timeout(self):
        """Xử lý khi timeout."""
        pass
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """Kiểm tra interaction."""
        return True


class BirthdaySelect(discord.ui.Select):
    """Select menu cho birthdays."""
    
    def __init__(self, bot, guild, channel):
        birthdays = load_json(BIRTHDAYS_JSON)
        
        options = []
        # Thêm options từ danh sách birthdays
        for bd in birthdays:
            user_id = bd.get('user_id')
            user_name = bd.get('user_name', 'Unknown')
            date = bd.get('date', 'N/A')
            label = f"{user_name} ({date})"
            # Giới hạn label length
            if len(label) > 100:
                label = label[:97] + "..."
            options.append(
                discord.SelectOption(
                    label=label,
                    value=str(user_id),
                    description=f"Test birthday cho {user_name}"
                )
            )
        
        if not options:
            options.append(
                discord.SelectOption(
                    label="Không có birthday nào",
                    value="none",
                    description="Vui lòng thêm birthday trước"
                )
            )
        
        super().__init__(
            placeholder="Chọn user để test birthday...",
            min_values=1,
            max_values=1,
            options=options
        )
        
        self.bot = bot
        self.guild = guild
        self.channel = channel
    
    async def callback(self, interaction: discord.Interaction):
        """Xử lý khi chọn user."""
        selected_value = self.values[0]
        
        if selected_value == "none":
            await interaction.response.send_message(
                "❌ Không có birthday nào để test. Vui lòng thêm birthday trước.",
                ephemeral=True
            )
            return
        
        birthdays = load_json(BIRTHDAYS_JSON)
        user_bd = None
        for bd in birthdays:
            if str(bd.get('user_id')) == selected_value:
                user_bd = bd
                break
        
        if not user_bd:
            await interaction.response.send_message(
                "❌ Không tìm thấy birthday cho user này.",
                ephemeral=True
            )
            return
        
        user_name = user_bd.get('user_name', 'Unknown')
        user_id = user_bd.get('user_id')
        name = f"Sinh nhật {user_name}"
        
        await interaction.response.defer(ephemeral=True)
        await self.bot.send_wish(self.guild, name, "Birthday", None, user_id=user_id)  # Không gửi thông báo test
        await interaction.followup.send(f"✅ Đã gửi test birthday cho {user_name}!", ephemeral=True)


class TestBirthdayView(discord.ui.View):
    """View để test birthday với menu chọn user."""
    
    def __init__(self, bot, guild, channel):
        super().__init__(timeout=300)
        self.add_item(BirthdaySelect(bot, guild, channel))


class CountdownBirthdaySelect(discord.ui.Select):
    """Select menu cho countdown birthday."""
    
    def __init__(self, bot, guild, channel):
        birthdays = load_json(BIRTHDAYS_JSON)
        
        options = []
        # Thêm options từ danh sách birthdays
        for bd in birthdays:
            user_id = bd.get('user_id')
            user_name = bd.get('user_name', 'Unknown')
            date = bd.get('date', 'N/A')
            label = f"{user_name} ({date})"
            # Giới hạn label length
            if len(label) > 100:
                label = label[:97] + "..."
            options.append(
                discord.SelectOption(
                    label=label,
                    value=str(user_id),
                    description=f"Test countdown cho {user_name}"
                )
            )
        
        if not options:
            options.append(
                discord.SelectOption(
                    label="Không có birthday nào",
                    value="none",
                    description="Vui lòng thêm birthday trước"
                )
            )
        
        super().__init__(
            placeholder="Chọn user để test countdown birthday...",
            min_values=1,
            max_values=1,
            options=options
        )
        
        self.bot = bot
        self.guild = guild
        self.channel = channel
    
    async def callback(self, interaction: discord.Interaction):
        """Xử lý khi chọn user."""
        selected_value = self.values[0]
        
        if selected_value == "none":
            await interaction.response.send_message(
                "❌ Không có birthday nào để test. Vui lòng thêm birthday trước.",
                ephemeral=True
            )
            return
        
        birthdays = load_json(BIRTHDAYS_JSON)
        user_bd = None
        for bd in birthdays:
            if str(bd.get('user_id')) == selected_value:
                user_bd = bd
                break
        
        if not user_bd:
            await interaction.response.send_message(
                "❌ Không tìm thấy birthday cho user này.",
                ephemeral=True
            )
            return
        
        user_name = user_bd.get('user_name', 'Unknown')
        
        await interaction.response.defer(ephemeral=True)
        
        # Tính toán days và age
        if user_bd['type'] == 'Solar':
            days = get_days_until_solar(user_bd['date'])
        else:
            days = get_days_until_lunar(user_bd['date'])
        
        age = get_age(user_bd['date'], user_bd['type'])
        if isinstance(age, int):
            age += 1
        
        await self.bot.send_countdown(
            self.guild,
            None,
            days,
            user_name=user_name,
            age=age,
            template_type="birthday"
        )
        await interaction.followup.send(f"✅ Đã gửi test countdown birthday cho {user_name}!", ephemeral=True)


class TestCountdownBirthdayView(discord.ui.View):
    """View để test countdown birthday với menu chọn user."""
    
    def __init__(self, bot, guild, channel):
        super().__init__(timeout=300)
        self.add_item(CountdownBirthdaySelect(bot, guild, channel))


class TestWeatherView(discord.ui.View):
    """View để test weather."""
    
    def __init__(self, bot, guild, channel):
        super().__init__(timeout=300)
        self.bot = bot
        self.guild = guild
        self.channel = channel
    
    @discord.ui.button(label="Test Thông Báo Thời Tiết", style=discord.ButtonStyle.primary)
    async def test_weather_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        """Test gửi thông báo thời tiết."""
        from core.json_store import load_json
        from core.constants import JSON_CONFIG
        from core.weather_service import get_weather
        from datetime import datetime
        import pytz
        
        config = load_json(JSON_CONFIG).get(str(self.guild.id), {})
        weather_config = config.get("weather")
        
        if not weather_config:
            await interaction.response.send_message(
                "❌ Chưa cấu hình thông báo thời tiết. Vui lòng dùng `/weather setup`.",
                ephemeral=True
            )
            return
        
        locations = weather_config.get("locations", [])
        if not locations:
            await interaction.response.send_message(
                "❌ Chưa cấu hình vị trí thời tiết.",
                ephemeral=True
            )
            return
        
        await interaction.response.send_message(
            "🔄 Đang gửi test thông báo thời tiết...",
            ephemeral=True
        )
        
        # Lấy role_mention từ config chính
        role_id = config.get('role_id')
        role_mention = f"<@&{role_id}>" if role_id else "@everyone"
        
        # Tạo thông báo giống thông báo thật
        vn_tz = pytz.timezone("Asia/Ho_Chi_Minh")
        now = datetime.now(vn_tz)
        weekday_names = [
            "Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", 
            "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"
        ]
        weekday = weekday_names[now.weekday()]
        date_str = now.strftime("%d/%m/%Y")
        
        # Lấy thông tin thời tiết cho tất cả vị trí
        weather_messages = []
        for location in locations:
            weather_data = get_weather(location)
            if weather_data:
                weather_messages.append(
                    f"thời tiết {weather_data['description']}, "
                    f"nhiệt độ tại {location} là {weather_data['temperature']}°C"
                )
            else:
                weather_messages.append(
                    f"không thể lấy thông tin thời tiết cho {location}"
                )
        
        # Tạo message với tất cả vị trí, sau đó mới tag role_mention
        message = (
            f"Hôm nay là {weekday}, ngày {date_str}, "
            + ", ".join(weather_messages) + ". "
            + f"Chúc một ngày tốt lành! {role_mention}"
        )
        
        # Gửi thông báo test
        await self.channel.send(message)
        await interaction.followup.send(
            f"✅ Đã gửi test thông báo thời tiết đến {self.channel.mention}!",
            ephemeral=True
        )

