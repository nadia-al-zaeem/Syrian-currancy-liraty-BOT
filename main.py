# bot running with Webhook (Render ready)

import os
from flask import Flask, request
from telegram import Update
from telegram.ext import (ApplicationBuilder,CommandHandler,ContextTypes,MessageHandler,
    CallbackQueryHandler,filters)

from handlers.start import start, button_handler, message_handler

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
# Webhook endpoint
# ==============================

@flask_app.route("/", methods=["POST"])
def webhook():
    update = Update.de_json(
        request.get_json(force=True),
        telegram_app.bot
    )
    telegram_app.update_queue.put_nowait(update)
    return "OK"

# ==============================
# تشغيل التطبيق
# ==============================

if __name__ == "__main__":
    telegram_app.initialize()
    telegram_app.start()

    telegram_app.bot.set_webhook(
        url="https://اسم-خدمتك.onrender.com/"
    )

    print("✅ BOT IS RUNNING WITH WEBHOOK")

    flask_app.run(host="0.0.0.0", port=PORT)


























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