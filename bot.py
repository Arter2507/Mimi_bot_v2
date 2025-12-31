import discord
from discord.ext import commands, tasks
from discord import app_commands
from dotenv import load_dotenv
import os
from datetime import datetime, time
import pytz
import json
import asyncio

from core.constants import DEFAULT_WISH_TIME, JSON_CONFIG, HOLIDAYS_JSON, BIRTHDAYS_JSON
from core.json_store import load_json
from core.date_utils import get_solar_date, get_lunar_date, get_days_until_solar, get_days_until_lunar, get_age
from core.weather_service import get_weather
from core.ai_wish import generate_wish
from views.celebrate_view import CelebrateView

from cogs.config_cog import ConfigCog
from cogs.info_cog import InfoCog
from cogs.holiday_cog import HolidayCog
from cogs.birthday_cog import BirthdayCog
from cogs.admin_cog import AdminCog
from cogs.test_cog import TestCog
from cogs.weather_cog import WeatherCog

load_dotenv()
GUILD_ID = os.getenv("GUILD_ID")


class HolidayBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.add_cog(ConfigCog(self))
        await self.add_cog(InfoCog(self))
        await self.add_cog(HolidayCog(self))
        await self.add_cog(BirthdayCog(self))
        await self.add_cog(AdminCog(self))
        await self.add_cog(TestCog(self))
        await self.add_cog(WeatherCog(self))
        self.add_view(CelebrateView())

        # Sync to specific guild for instant updates
        if GUILD_ID:
            try:
                guild = discord.Object(id=int(GUILD_ID))
                self.tree.copy_global_to(guild=guild)
                synced = await self.tree.sync(guild=guild)
                print(f"Synced {len(synced)} commands to Guild {GUILD_ID}")
            except Exception as e:
                print(f"Guild Sync Error: {e}")
        else:
            synced = await self.tree.sync()
            print(f"Synced {len(synced)} global commands")

        # Start background tasks
        self.daily_check.start()
        self.weather_notification_task.start()

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")
        
        # Gửi thông báo khởi động vào log channel
        await self.send_startup_notification()
        
        # Kiểm tra và gửi thông báo restart thành công nếu có
        await self.check_restart_status()

    # ========== Helper Methods ==========

    async def send_log_message(self, guild, message: str, file_path: str = None):
        """Gửi thông báo vào log channel được config, có thể kèm file."""
        config = load_json(JSON_CONFIG).get(str(guild.id))
        if not config:
            return
        
        log_channel_id = config.get('log_channel_id')
        if not log_channel_id:
            return
        
        try:
            channel = guild.get_channel(int(log_channel_id))
            if channel:
                if file_path and os.path.exists(file_path):
                    with open(file_path, 'rb') as f:
                        file = discord.File(f, filename=os.path.basename(file_path))
                        await channel.send(message, file=file)
                else:
                    await channel.send(message)
        except Exception as e:
            print(f"Lỗi khi gửi log message (Guild: {guild.id}): {e}")

    def get_restart_count(self):
        """Lấy số lần restart hiện tại và tăng lên 1."""
        restart_count_file = "restart_count.json"
        count = 1
        
        if os.path.exists(restart_count_file):
            try:
                with open(restart_count_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    count = data.get('count', 1) + 1
            except:
                count = 1
        
        # Lưu số lần mới
        try:
            with open(restart_count_file, 'w', encoding='utf-8') as f:
                json.dump({'count': count}, f, indent=2)
        except:
            pass
        
        return count

    async def send_startup_notification(self):
        """Gửi thông báo khởi động bot vào log channel của tất cả guilds."""
        restart_count = self.get_restart_count()
        
        for guild in self.guilds:
            try:
                latency = round(self.latency * 1000)
                message = (
                    f"✅ **Bot đã khởi động thành công!**\n"
                    f"🏓 Latency: {latency}ms\n"
                    f"⏰ Thời gian: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
                    f"📊 Lần khởi động thứ: {restart_count}"
                )
                
                # Tạo file restart info nếu có restart_info.json
                restart_info_file = "restart_info.json"
                file_to_send = None
                
                if os.path.exists(restart_info_file):
                    # Đọc và tạo file mới với tên có số lần
                    try:
                        with open(restart_info_file, 'r', encoding='utf-8') as f:
                            restart_info = json.load(f)
                        
                        # Tạo file mới với tên có số lần
                        new_filename = f"restart_info_file_{restart_count}.json"
                        with open(new_filename, 'w', encoding='utf-8') as f:
                            json.dump(restart_info, f, indent=2, ensure_ascii=False)
                        
                        file_to_send = new_filename
                    except Exception as e:
                        print(f"Lỗi khi tạo restart info file: {e}")
                
                await self.send_log_message(guild, message, file_to_send)
                
                # Xóa file tạm sau khi gửi
                if file_to_send and os.path.exists(file_to_send):
                    try:
                        os.remove(file_to_send)
                    except:
                        pass
                        
            except Exception as e:
                print(f"Lỗi khi gửi startup notification (Guild: {guild.id}): {e}")

    async def send_wish(self, guild, name, type_info, interaction_ctx=None, user_id=None):
        """Send a wish message to the configured channel."""
        config = load_json(JSON_CONFIG).get(str(guild.id))
        if not config:
            if interaction_ctx:
                if interaction_ctx.response.is_done():
                    await interaction_ctx.followup.send("Server chưa cấu hình.", ephemeral=True)
                else:
                    await interaction_ctx.response.send_message("Server chưa cấu hình.", ephemeral=True)
            return

        channel_id = config.get('channel_id')
        role_id = config.get('role_id')
        template = config.get('content_template', "Chúc mừng {date_name}!")

        channel = guild.get_channel(int(channel_id))
        if not channel:
            if interaction_ctx:
                if interaction_ctx.response.is_done():
                    await interaction_ctx.followup.send("Không tìm thấy channel.", ephemeral=True)
                else:
                    await interaction_ctx.response.send_message("Không tìm thấy channel.", ephemeral=True)
            return

        role_mention = f"<@&{role_id}>" if role_id else "@everyone"
        
        # Xử lý mention_user cho birthday
        mention_user = ""
        user_name_for_template = name.replace("Sinh nhật ", "") if "Sinh nhật " in name else "Members"
        
        if user_id and type_info == "Birthday":
            mention_user = f"<@{user_id}>"
            # Sử dụng template mặc định cho birthday với tag user
            if "{mention_user}" not in template:
                template = f"🎂 Chúc mừng Sinh nhật {{user}} {mention_user}! @everyone"
        
        # AI Wish Generation
        wish_type = config.get('wish_type', 'Static')
        if wish_type == 'AI':
            # Language config will be added in next task, default to 'vi'
            lang = config.get('language', 'vi') 
            content = generate_wish(name, type_info, lang, user_name_for_template, mention_user)
            # Append role_mention if not in content (AI might not include it)
            if role_mention and role_mention not in content:
                content += f"\n\n{role_mention}"
        else:
            # Static Template
            replacements = {
                "{date_name}": name,
                "{date}": datetime.now().strftime("%d/%m/%Y"),
                "{time}": datetime.now().strftime("%H:%M"),
                "{role_mention}": role_mention,
                "{everyone}": "@everyone",
                "{here}": "@here",
                "{guild}": guild.name,
                "{user}": user_name_for_template,
                "{mention_user}": mention_user,
            }

            content = template
            for k, v in replacements.items():
                content = content.replace(k, str(v))

        view = CelebrateView()

        # Gửi tin nhắn (không gửi thông báo test nữa để giống thực tế)
        await channel.send(content, view=view)

    async def send_countdown(self, guild, name, days, interaction_ctx=None, user_name=None, age=None, template_type="tet"):
        """Send countdown message."""
        config = load_json(JSON_CONFIG).get(str(guild.id))
        if not config:
            return

        cd_config = config.get("countdown", {})
        if template_type == "birthday":
            template = cd_config.get("template_birthday", "{role_mention} Còn {days} ngày nữa tới sinh nhật {user}, năm nay đã tròn {age} tuổi!")
        else:
            template = cd_config.get("template_tet", "{role_mention} Còn {days} ngày nữa là đến {date_name}!")

        channel_id = config.get('channel_id')
        role_id = config.get('role_id')

        channel = guild.get_channel(int(channel_id))
        if not channel:
            return

        role_mention = f"<@&{role_id}>" if role_id else "@everyone"
        replacements = {
            "{date_name}": name or "",
            "{days}": str(days),
            "{role_mention}": role_mention,
            "{user}": user_name or "Unknown",
            "{age}": str(age) if age else "?",
            "{everyone}": "@everyone"
        }

        content = template
        for k, v in replacements.items():
            content = content.replace(str(k), str(v))

        await channel.send(content)

    async def send_tet_countdown_report(self, guild):
        """Send Tet countdown report."""
        config = load_json(JSON_CONFIG).get(str(guild.id))
        if not config:
            return
        channel_id = config.get('channel_id')
        role_id = config.get('role_id')
        channel = guild.get_channel(int(channel_id))
        if not channel:
            return

        role_mention = f"<@&{role_id}>" if role_id else "@everyone"

        tet_solar = get_days_until_solar("01-01")
        tet_lunar = get_days_until_lunar("01-01")

        msg = f"**{role_mention} Countdown Tết**:\n"
        msg += f"- 🎆 Tết Dương Lịch (01-01): còn **{tet_solar}** ngày\n"
        msg += f"- 🏮 Tết Nguyên Đán (01-01 Âm): còn **{tet_lunar}** ngày"

        await channel.send(msg)
    
    async def send_weather_notification(self, guild):
        """Gửi thông báo thời tiết hằng ngày."""
        config = load_json(JSON_CONFIG).get(str(guild.id), {})
        if not config:
            return
        
        weather_config = config.get("weather")
        
        if not weather_config or not weather_config.get("enabled", False):
            return
        
        locations = weather_config.get("locations", [])
        channel_id = weather_config.get("channel_id")
        
        if not locations:
            return
        
        if not channel_id:
            return
        
        channel = guild.get_channel(channel_id)
        if not channel:
            return
        
        # Lấy role_mention từ config chính
        role_id = config.get('role_id')
        role_mention = f"<@&{role_id}>" if role_id else "@everyone"
        
        # Tạo thông báo
        vn_tz = pytz.timezone("Asia/Ho_Chi_Minh")
        now = datetime.now(vn_tz)
        weekday_names = [
            "Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", 
            "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"
        ]
        weekday = weekday_names[now.weekday()]
        date_str = now.strftime("%d/%m/%Y")
        
        # Lấy thông tin thời tiết cho tất cả vị trí
        weather_lines = []
        for location in locations:
            weather_data = get_weather(location)
            if weather_data:
                weather_lines.append(
                    f"📍 **{location}**: {weather_data['description']}, {weather_data['temperature']}°C"
                )
            else:
                print(f"Không thể lấy thông tin thời tiết cho {location} (Guild: {guild.id})")
                weather_lines.append(
                    f"📍 **{location}**: không thể lấy thông tin"
                )
        
        # Tạo message với format nhiều dòng dễ đọc
        weather_content = "\n".join(weather_lines)
        message = (
            f"☀️ **Thông báo thời tiết - {weekday}, {date_str}**\n\n"
            f"{weather_content}\n\n"
            f"Chúc một ngày tốt lành! {role_mention}"
        )
        
        try:
            await channel.send(message)
        except Exception as e:
            print(f"Lỗi khi gửi thông báo thời tiết (Guild: {guild.id}): {e}")

    async def check_events_for_guild(self, guild, holidays=None, birthdays=None, solar=None, lunar=None, manual_trigger=False, interaction_ctx=None):
        """Check and send wishes for matching events."""
        if holidays is None:
            holidays = []
        if birthdays is None:
            birthdays = []
        if not solar:
            solar = get_solar_date()
        if not lunar:
            lunar = get_lunar_date()

        # If manual trigger with no holidays passed, reload them
        if manual_trigger and not holidays:
            all_h = load_json(HOLIDAYS_JSON)
            for h in all_h:
                if (h['type'] == 'Solar' and h['date'] == solar) or \
                   (h['type'] == 'Lunar' and h['date'] == lunar):
                    holidays.append(h)

        # Send holiday wishes
        for h in holidays:
            await self.send_wish(guild, h['name'], h['type'], interaction_ctx)

        # Send birthday wishes
        if manual_trigger and not birthdays:
            birthdays = load_json(BIRTHDAYS_JSON)

        todays_bd = [b for b in birthdays if (b['type'] == 'Solar' and b['date'].startswith(solar)) or (b['type'] == 'Lunar' and b['date'].startswith(lunar))]

        for bd in todays_bd:
            name = f"Sinh nhật {bd['user_name']}"
            user_id = bd.get('user_id')
            await self.send_wish(guild, name, "Birthday", interaction_ctx, user_id=user_id)

    async def check_countdowns(self, guild, holidays, birthdays):
        """Check and send countdown notifications."""
        today = datetime.now()
        config = load_json(JSON_CONFIG).get(str(guild.id), {})
        cd_config = config.get("countdown", {})

        # Tet Countdown Logic - Check if today matches frequency
        freq = cd_config.get("frequency", "Monthly")
        should_alert_tet = False
        if freq == "Monthly" and today.day == 1:
            should_alert_tet = True
        if freq == "Weekly" and today.weekday() == 0:  # Monday
            should_alert_tet = True

        if should_alert_tet:
            await self.send_tet_countdown_report(guild)

        # Custom countdown days (default: 5)
        days_before = cd_config.get("days_before", [5])
        # Allow single int for backward compatibility or direct edit
        if isinstance(days_before, int):
            days_before = [days_before]

        # Check Tet dates for countdown
        tet_dates = [h for h in holidays if h['name'] in ["Tết Dương Lịch", "Tết Nguyên Đán"]]
        for t in tet_dates:
            if t['type'] == 'Solar':
                days = get_days_until_solar(t['date'])
            else:
                days = get_days_until_lunar(t['date'])

            if days in days_before:
                await self.send_countdown(guild, t['name'], days, template_type="tet")

        # Birthday Countdown Logic
        for bd in birthdays:
            if bd['type'] == 'Solar':
                days = get_days_until_solar(bd['date'])
            else:
                days = get_days_until_lunar(bd['date'])

            if days in days_before:
                age = get_age(bd['date'], bd['type'])
                if isinstance(age, int):
                    age += 1
                await self.send_countdown(guild, None, days, user_name=bd['user_name'], age=age, template_type="birthday")

    # ========== Background Task ==========

    @tasks.loop(minutes=1)
    async def daily_check(self):
        """Daily background task to check holidays and birthdays."""
        vn_tz = pytz.timezone("Asia/Ho_Chi_Minh")
        now_vn = datetime.now(vn_tz)
        
        today_solar = get_solar_date()
        today_lunar = get_lunar_date()
        holidays = load_json(HOLIDAYS_JSON)
        birthdays = load_json(BIRTHDAYS_JSON)
        
        # Kiểm tra từng guild theo thời gian cấu hình riêng
        for guild in self.guilds:
            config = load_json(JSON_CONFIG).get(str(guild.id), {})
            notif_time = config.get('notification_time', {})
            target_hour = notif_time.get('hour', 6)
            target_minute = notif_time.get('minute', 0)
            
            # Chỉ chạy khi đúng giờ đã cấu hình
            if now_vn.hour != target_hour or now_vn.minute != target_minute:
                continue
            
            # Lọc holidays phù hợp
            matched_events = []
            for h in holidays:
                if (h['type'] == 'Solar' and h['date'] == today_solar) or \
                   (h['type'] == 'Lunar' and h['date'] == today_lunar):
                    matched_events.append(h)
            
            await self.check_events_for_guild(guild, matched_events, birthdays, today_solar, today_lunar)
            await self.check_countdowns(guild, holidays, birthdays)

    @daily_check.before_loop
    async def before_daily_check(self):
        await self.wait_until_ready()
    
    @tasks.loop(minutes=1)
    async def weather_notification_task(self):
        """Task gửi thông báo thời tiết theo giờ cấu hình."""
        vn_tz = pytz.timezone("Asia/Ho_Chi_Minh")
        now_vn = datetime.now(vn_tz)
        
        for guild in self.guilds:
            config = load_json(JSON_CONFIG).get(str(guild.id), {})
            notif_time = config.get('notification_time', {})
            target_hour = notif_time.get('hour', 6)
            target_minute = notif_time.get('minute', 0)
            
            # Chỉ gửi khi đúng giờ đã cấu hình
            if now_vn.hour == target_hour and now_vn.minute == target_minute:
                await self.send_weather_notification(guild)
    
    @weather_notification_task.before_loop
    async def before_weather_notification(self):
        await self.wait_until_ready()
    
    async def check_restart_status(self):
        """Kiểm tra và gửi thông báo restart thành công vào log channel."""
        restart_info_file = "restart_info.json"
        
        if not os.path.exists(restart_info_file):
            return
        
        try:
            with open(restart_info_file, 'r', encoding='utf-8') as f:
                restart_info = json.load(f)
            
            guild_id = int(restart_info.get('guild_id'))
            user_name = restart_info.get('user_name', 'Unknown')
            
            guild = self.get_guild(guild_id)
            if not guild:
                # Xóa file nếu không tìm thấy guild
                os.remove(restart_info_file)
                return
            
            # Đợi một chút để đảm bảo bot đã sẵn sàng
            await asyncio.sleep(2)
            
            # Thử ping để kiểm tra bot hoạt động
            try:
                latency = round(self.latency * 1000)
                ping_success = latency > 0
            except:
                ping_success = False
            
            restart_count = self.get_restart_count()
            
            if ping_success:
                # Ping thành công - bot đã khởi động xong
                message = (
                    f"✅ **Bot đã khởi động lại thành công!**\n"
                    f"🏓 Latency: {latency}ms\n"
                    f"👤 Khởi động bởi: {user_name}\n"
                    f"⏰ Thời gian: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
                    f"📊 Lần khởi động thứ: {restart_count}"
                )
            else:
                # Ping không thành công - có thể có lỗi
                message = (
                    f"⚠️ **Bot đã khởi động lại nhưng có thể có vấn đề!**\n"
                    f"👤 Khởi động bởi: {user_name}\n"
                    f"⏰ Thời gian: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
                    f"📊 Lần khởi động thứ: {restart_count}\n"
                    f"❌ Không thể ping bot, vui lòng kiểm tra lại."
                )
            
            # Tạo file restart info với số lần
            file_to_send = None
            try:
                new_filename = f"restart_info_file_{restart_count}.json"
                with open(new_filename, 'w', encoding='utf-8') as f:
                    json.dump(restart_info, f, indent=2, ensure_ascii=False)
                file_to_send = new_filename
            except Exception as e:
                print(f"Lỗi khi tạo restart info file: {e}")
            
            # Gửi vào log channel kèm file
            await self.send_log_message(guild, message, file_to_send)
            
            # Xóa file sau khi đã xử lý
            if os.path.exists(restart_info_file):
                try:
                    os.remove(restart_info_file)
                except:
                    pass
            
            if file_to_send and os.path.exists(file_to_send):
                try:
                    os.remove(file_to_send)
                except:
                    pass
            
        except Exception as e:
            print(f"Lỗi khi kiểm tra restart status: {e}")
            # Xóa file nếu có lỗi
            if os.path.exists(restart_info_file):
                try:
                    os.remove(restart_info_file)
                except:
                    pass
