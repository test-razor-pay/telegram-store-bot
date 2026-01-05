import random
import time

def generate_order_id():
    return f"BB{random.randint(100,999)}{int(time.time())}{random.randint(100,999)}"
