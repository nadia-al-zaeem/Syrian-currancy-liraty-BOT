# bot running with Webhook (Render ready)

import os
from flask import Flask, request
from telegram import Update
from telegram.ext import (ApplicationBuilder,CommandHandler,ContextTypes,MessageHandler,
    CallbackQueryHandler,filters)

from handlers.start import start, button_handler, message_handler
import asyncio

# ==============================
# إعداد المتغيرات
# ==============================

TOKEN = os.environ.get("BOT_TOKEN")
PORT = int(os.environ.get("PORT", 5000))

# ==============================
# إنشاء Flask و Telegram App
# ==============================

flask_app = Flask(__name__)
telegram_app = ApplicationBuilder().token(TOKEN).build()

# ==============================
# Handlers (كما هي عندك)
# ==============================

telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CallbackQueryHandler(button_handler))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))



# ==============================
# تشغيل التطبيق
# ==============================

# ... (الجزء العلوي من الكود و Handlers يبقى كما هو)

# ==============================
# Webhook endpoint
# ==============================

# نستخدم التوكن كمسار سري
@flask_app.route("/{}".format(TOKEN), methods=["POST"])
def webhook():
    # ... (بقية الدالة كما هي)
    update = Update.de_json(
        request.get_json(force=True),
        telegram_app.bot
    )
    telegram_app.update_queue.put_nowait(update)
    return "OK"

# ==============================
# دالة إعداد البوت (نضيفها)
# ==============================

async def setup_webhook():
    # التأكد من تهيئة التطبيق قبل تعيين Webhook
    await telegram_app.initialize() 

    # تعيين Webhook إلى الرابط الصحيح (URL)
    # ملاحظة: نستخدم متغير البيئة الذي يوفره Render وهو RENDER_EXTERNAL_URL
    WEBHOOK_URL = os.environ.get("RENDER_EXTERNAL_URL")
    
    if WEBHOOK_URL:
        full_webhook_url = f"{WEBHOOK_URL}/{TOKEN}"
        await telegram_app.bot.set_webhook(url=full_webhook_url)
        print(f"✅ Webhook set to: {full_webhook_url}")
    else:
        print("⚠️ RENDER_EXTERNAL_URL not found. Webhook not set.")


# نفذ إعداد Webhook مرة واحدة عند بدء تشغيل الخادم
asyncio.run(setup_webhook())


























#bot running  by polling:
'''''
from telegram import Update
from telegram.ext import ApplicationBuilder,CommandHandler,ContextTypes ,MessageHandler,filters,CallbackQueryHandler
import os
from dotenv import load_dotenv
from handlers.start import start,button_handler,message_handler
import asyncio

# 1. تحميل المتغيرات من ملف .env
load_dotenv()

# 2. استرجاع التوكن
TOKEN = os.getenv('BOT_TOKEN')




def main():
   
    app=ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start",start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT, message_handler))


    print("✅ BOT IS RUNNING")
    
    app.run_polling()

if __name__ == "__main__":
    main()   
'''