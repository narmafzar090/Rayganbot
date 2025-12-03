import telebot
import requests
import random

# ============================
# تنظیمات ربات
# ============================
TOKEN = "8025043146:AAG6AYsJ8eTEa2IcZVA7BYfFxnTYvpWzPos"
bot = telebot.TeleBot(TOKEN)

# لینک گیت‌هاب کانفیگ‌ها
VLESS_URL = "https://raw.githubusercontent.com/F0rc3Run/F0rc3Run/refs/heads/main/splitted-by-protocol/vless.txt"


# ============================
# تابع دریافت کانفیگ رندوم
# ============================
def get_random_vless():
    try:
        response = requests.get(VLESS_URL, timeout=10)
        raw = response.text.strip().split("\n")

        # فقط کانفیگ‌هایی که با vless:// شروع می‌شن
        configs = [c for c in raw if c.startswith("vless://")]

        if not configs:
            return "❌ کانفیگی یافت نشد!"

        selected = random.choice(configs)

        # اضافه کردن نام نمایشی و ``` در اول و آخر
        final_cfg = f"```RAYGAN\n{selected}\n```"
        return final_cfg

    except Exception as e:
        return f"❌ مشکل در دریافت کانفیگ: {e}"


# ============================
# دکمه‌ شیشه‌ای
# ============================
def inline_button():
    kb = telebot.types.InlineKeyboardMarkup()
    btn = telebot.types.InlineKeyboardButton("📡 دریافت کانفیگ", callback_data="get_cfg")
    kb.add(btn)
    return kb


# ============================
# /start
# ============================
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "سلام دوست عزیز 😊\nبرای دریافت کانفیگ رایگان روی دکمه زیر بزن:",
        reply_markup=inline_button()
    )


# ============================
# دریافت دکمه شیشه‌ای
# ============================
@bot.callback_query_handler(func=lambda c: True)
def callback_query(call):
    if call.data == "get_cfg":
        cfg = get_random_vless()
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, cfg)


# ============================
# اجرای ربات
# ============================
print("Bot is running...")
bot.infinity_polling()