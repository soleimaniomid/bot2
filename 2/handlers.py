import re
import logging
from telegram import Update
from telegram.ext import CallbackContext
from database import save_transaction, get_transaction, delete_transaction
from utils import format_message

# تنظیمات لاگینگ
logger = logging.getLogger(__name__)

async def process_message(update: Update, context: CallbackContext) -> None:
    message_text = update.message.text.strip()
    logger.info(f"پیام دریافتی: {message_text}")

    # جلوگیری از پردازش پیام "ب"
    if message_text.lower() == 'ب':
        logger.warning(f"پیام 'ب' به عنوان یک پیام عادی دریافت شده است، نادیده گرفته شد.")
        return

    # بررسی فرمت پیام و استخراج اطلاعات
    match = re.match(r"(\d+)\s*(ف|خ)\s*(\d+)", message_text)
    if match:
        price = int(match.group(1))  # قیمت هر بسته
        operation = match.group(2)   # نوع عملیات (فروش یا خرید)
        quantity = int(match.group(3))  # تعداد بسته‌ها

        # ذخیره پیام و جزئیات آن برای استفاده در ثبت معامله
        save_transaction(update.message.message_id, {
            'price': price,
            'operation': operation,
            'quantity': quantity,
            'initiator': update.message.from_user.username,
            'chat_id': update.message.chat_id
        })
        logger.info(f"معامله ذخیره شد: {price} {operation} {quantity}")
    else:
        logger.warning(f"فرمت پیام نادرست است: {message_text}")

async def handle_reply(update: Update, context: CallbackContext) -> None:
    logger.info(f"پیام ریپلای دریافتی: {update.message.text}")

    if update.message.reply_to_message:
        replied_message_id = update.message.reply_to_message.message_id
        transaction = get_transaction(replied_message_id)
        logger.info(f"شناسه پیام ریپلای شده: {replied_message_id}, معامله: {transaction}")

        if transaction:
            reply_text = update.message.text.strip().lower()
            logger.info(f"متن ریپلای: {reply_text}")

            if reply_text == 'ب':
                action = "فروش" if transaction['operation'] == 'ف' else "خرید"
                opposite_action = "خرید" if action == "فروش" else "فروش"
                
                # ثبت معامله
                if transaction['operation'] == 'ف':
                    buyer = update.message.from_user.username
                    seller = transaction['initiator']
                else:
                    seller = update.message.from_user.username
                    buyer = transaction['initiator']
                
                # پاک کردن معامله از لیست انتظار
                delete_transaction(replied_message_id)

                # ارسال نتایج به گروه
                result_message = format_message(
                    price=transaction['price'],
                    operation=transaction['operation'],
                    quantity=transaction['quantity'],
                    initiator=seller,
                    buyer=buyer
                )
                await context.bot.send_message(chat_id=transaction['chat_id'], text=result_message, parse_mode='Markdown')
                logger.info(f"معامله ثبت شد و ارسال شد: {result_message}")
            else:
                logger.warning(f"متن ریپلای نادرست است: {reply_text}")
        else:
            logger.warning(f"معامله‌ای برای شناسه پیام پیدا نشد: {replied_message_id}")
    else:
        logger.warning("پیام ریپلای شده نامعتبر است یا معامله‌ای ندارد.")
