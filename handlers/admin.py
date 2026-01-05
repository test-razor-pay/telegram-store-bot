from aiogram import Router, F
from aiogram.types import Message
from config import ADMINS
from database.firebase import db
from utils.keyboards import admin_kb

router = Router()

def is_admin(uid):
    return uid in ADMINS

@router.message(F.text == "/admin")
async def admin_panel(message: Message):
    if not is_admin(message.from_user.id):
        return
    await message.answer("⚙ Admin Panel", reply_markup=admin_kb())

@router.message(F.text == "🛒 Add Product")
async def add_product(message: Message):
    if not is_admin(message.from_user.id):
        return
    await message.answer(
        "Send product like:\n\nBr Mods\n7-80\n15-150\n30-250"
    )

@router.message(F.text.contains("-"))
async def save_product(message: Message):
    if not is_admin(message.from_user.id):
        return

    lines = message.text.splitlines()
    name = lines[0]
    data = {}

    for l in lines[1:]:
        d, p = l.split("-")
        data[d.strip()] = int(p.strip())

    db.collection("products").document(name).set(data)
    await message.answer("✅ Product Added")
