# -*- coding: utf-8 -*-
import logging

# تنظیمات لاگینگ
logger = logging.getLogger(__name__)

# دیکشنری برای ذخیره‌سازی موقتی اطلاعات
pending_transactions = {}

def save_transaction(message_id, transaction):
    pending_transactions[message_id] = transaction
    logger.info(f"معامله در دیتابیس ذخیره شد: {message_id}")

def get_transaction(message_id):
    transaction = pending_transactions.get(message_id)
    logger.info(f"دریافت معامله برای شناسه پیام: {message_id}, نتیجه: {transaction}")
    return transaction

def delete_transaction(message_id):
    if message_id in pending_transactions:
        del pending_transactions[message_id]
        logger.info(f"معامله از دیتابیس حذف شد: {message_id}")
