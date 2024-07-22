# -*- coding: utf-8 -*-
import logging
from telegram.ext import Application, MessageHandler, filters
from handlers import process_message, handle_reply

# تنظیمات لاگینگ
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# توکن ربات
TOKEN = '6892549491:AAFz2rluse5nKyYB63wJ1Q4qLM8UQnkesNw'

def main() -> None:
    logger.info("شروع به کار ربات...")
    # ایجاد Application و dispatcher
    application = Application.builder().token(TOKEN).build()

    # افزودن هندلر برای پیام‌های متنی
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & ~filters.REPLY, process_message))
    application.add_handler(MessageHandler(filters.REPLY & filters.TEXT, handle_reply))

    # شروع polling
    application.run_polling()

if __name__ == '__main__':
    main()
