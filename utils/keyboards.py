from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def phone_kb():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📞 Share Number", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def admin_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            ["📊 Dashboard", "👤 Users"],
            ["🛒 Add Product", "🔑 Add Keys"],
            ["📦 Buyers", "📢 Broadcast"],
            ["⚙ Bot Status"]
        ],
        resize_keyboard=True
    )

def product_buttons(products):
    kb = InlineKeyboardMarkup()
    for p in products:
        kb.add(InlineKeyboardButton(text=p, callback_data=f"prod:{p}"))
    return kb

def days_buttons(product, days):
    kb = InlineKeyboardMarkup()
    for d in days:
        kb.add(InlineKeyboardButton(text=f"{d} Days", callback_data=f"buy:{product}:{d}"))
    return kb
