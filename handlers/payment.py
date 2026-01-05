import aiohttp, asyncio, time
from config import PAYMENT_API, MERCHANT_ID, QR_EXPIRY_SECONDS
from database.firebase import db

async def check_payment(order_id, amount, user_id, bot):
    start = time.time()

    async with aiohttp.ClientSession() as session:
        while time.time() - start < QR_EXPIRY_SECONDS:
            async with session.get(
                f"{PAYMENT_API}?mid={MERCHANT_ID}&order_id={order_id}"
            ) as r:
                data = await r.json()

                if (
                    data.get("STATUS") == "TXN_SUCCESS"
                    and float(data.get("TXNAMOUNT", 0)) == amount
                ):
                    await deliver_key(order_id, user_id, bot)
                    return

            await asyncio.sleep(1)

    db.collection("orders").document(order_id).update({"status": "expired"})

async def deliver_key(order_id, user_id, bot):
    order = db.collection("orders").document(order_id).get().to_dict()

    keys_ref = (
        db.collection("keys")
        .document(order["product"])
        .collection(str(order["days"]))
    )

    keys = keys_ref.where("used", "==", False).limit(1).stream()

    for k in keys:
        key_data = k.to_dict()
        keys_ref.document(k.id).update({
            "used": True,
            "used_by": user_id
        })

        await bot.send_message(
            user_id,
            f"✅ Payment Successful\n\n🔑 Your Key:\n`{key_data['key']}`",
            parse_mode="Markdown"
        )

        db.collection("orders").document(order_id).update({"status": "success"})
        return

    await bot.send_message(user_id, "❌ No keys available. Contact admin.")
