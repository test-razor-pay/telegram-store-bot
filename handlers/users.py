from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from database.firebase import db
from utils.keyboards import phone_kb, product_buttons, days_buttons
from utils.order_id import generate_order_id
from utils.qr import generate_qr
from handlers.payment import check_payment
from config import UPI_ID, UPI_NAME
import asyncio

router = Router()

@router.message(F.text == "/start")
async def start(message: Message):
    await message.answer("📞 Please share your number", reply_markup=phone_kb())

@router.message(F.contact)
async def save_user(message: Message):
    u = message.from_user
    db.collection("users").document(str(u.id)).set({
        "name": u.full_name,
        "username": u.username,
        "phone": message.contact.phone_number
    }, merge=True)

    products = [p.id for p in db.collection("products").stream()]
    await message.answer("🛒 Select Product", reply_markup=product_buttons(products))

@router.callback_query(F.data.startswith("prod:"))
async def product_selected(call: CallbackQuery):
    product = call.data.split(":")[1]
    product_data = db.collection("products").document(product).get().to_dict()

    text = f"🛒 {product}\n\n"
    for d, p in product_data.items():
        text += f"{d} Days – ₹{p}\n"

    await call.message.answer(
        text,
        reply_markup=days_buttons(product, product_data.keys())
    )

@router.callback_query(F.data.startswith("buy:"))
async def buy(call: CallbackQuery):
    _, product, days = call.data.split(":")
    price = db.collection("products").document(product).get().to_dict()[days]

    order_id = generate_order_id()
    qr_path = generate_qr(order_id, price, UPI_ID, UPI_NAME, f"{product}-{days}Days")

    db.collection("orders").document(order_id).set({
        "user_id": call.from_user.id,
        "product": product,
        "days": int(days),
        "amount": price,
        "status": "pending"
    })

    await call.message.answer_photo(
        open(qr_path, "rb"),
        caption=f"💳 Pay ₹{price}\n⏳ QR valid for 3 minutes"
    )

    asyncio.create_task(
        check_payment(order_id, price, call.from_user.id, call.bot)
    )
