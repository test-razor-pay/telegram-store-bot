import qrcode

def generate_qr(order_id, amount, upi, name, note):
    upi_url = (
        f"upi://pay?tr={order_id}&tid={order_id}"
        f"&pa={upi}&pn={name}&am={amount}&cu=INR&tn={note}"
    )

    img = qrcode.make(upi_url)
    path = f"/tmp/{order_id}.png"
    img.save(path)
    return path
