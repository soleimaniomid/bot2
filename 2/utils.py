# توابع کمکی برای پردازش متن و کارهای دیگر

def format_message(price, operation, quantity, initiator, buyer):
    action = "فروش" if operation == 'ف' else "خرید"
    opposite_action = "خرید" if action == "فروش" else "فروش"
    return (
        f"🔔 **فاکتور معامله**\n"
        f"💸 نوع معامله: {action}\n"
        f"💰 قیمت هر بسته: {price} تومان\n"
        f"📦 تعداد بسته‌ها: {quantity} عدد\n"
        f"👤 نام {opposite_action}: {initiator}\n"
        f"👤 نام {action}: {buyer}\n"
        f"📝 معامله با موفقیت ثبت شد!"
    )
