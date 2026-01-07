'''import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import (ApplicationBuilder,CommandHandler,CallbackQueryHandler,MessageHandler,filters)
from handlers.start import start, button_handler, message_handler
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.environ.get("BOT_TOKEN")
PORT = int(os.environ.get("PORT", 5000))
WEBHOOK_URL = os.environ.get("RENDER_EXTERNAL_URL")

flask_app = Flask(__name__)
telegram_app = ApplicationBuilder().token(TOKEN).build()

# Handlers
telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CallbackQueryHandler(button_handler))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

# Webhook endpoint (sync)
@flask_app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, telegram_app.bot)
    asyncio.get_event_loop().create_task(telegram_app.process_update(update))
    return "OK", 200

# إعداد Webhook وتشغيل البوت
async def run_bot():
    await telegram_app.initialize()
    if WEBHOOK_URL:
        full_url = f"{WEBHOOK_URL}/webhook"
        await telegram_app.bot.set_webhook(full_url)
        print(f"✅ Webhook set to: {full_url}")
    else:
        print("⚠️ RENDER_EXTERNAL_URL not found!")
    await telegram_app.start()
    print("🚀 Telegram bot started successfully!")


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.create_task(run_bot())

if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=PORT)'''




'''''
import os
import threading
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters
)
from handlers.start import start, button_handler, message_handler
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("RENDER_EXTERNAL_URL")
PORT = int(os.environ.get("PORT", 5000))

flask_app = Flask(__name__)

telegram_app = ApplicationBuilder().token(TOKEN).build()

# Handlers
telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CallbackQueryHandler(button_handler))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

# Webhook endpoint
@flask_app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, telegram_app.bot)
    #telegram_app.create_task(telegram_app.process_update(update))
    telegram_app.update_queue.put_nowait(update)   # ← هذا هو الصحيح

    return "OK", 200

# تشغيل PTB في Thread منفصل
def run_bot():
    telegram_app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path="webhook",
        webhook_url=f"{WEBHOOK_URL}/webhook"
    )

#threading.Thread(target=run_bot).start()
threading.Thread(target=lambda: telegram_app.start()).start()
if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=PORT)
'''



import asyncio
import logging
import os
from quart import Quart, request, Response
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    Application,
)
from handlers.start import start, button_handler, message_handler  # افترض أن هذا موجود
from dotenv import load_dotenv
from http import HTTPStatus

load_dotenv()
TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("RENDER_EXTERNAL_URL")  # https://your-app.onrender.com
PORT = int(os.environ.get("PORT", 10000))

# إعداد Logging للتصحيح
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# بناء الـ Application بدون updater (لـ webhook custom)
application = ApplicationBuilder().token(TOKEN).updater(None).build()

# إضافة الـ Handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(button_handler))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

# إعداد الـ Webhook مع تليجرام (يتم مرة واحدة عند التشغيل)
async def set_webhook():
    await application.bot.set_webhook(
        url=f"{WEBHOOK_URL}/webhook",
        allowed_updates=Update.ALL_TYPES
    )

# استدعاء set_webhook synchronously
asyncio.run(set_webhook())

# إعداد Quart app (async Flask)
quart_app = Quart(__name__)

@quart_app.post("/webhook")
async def webhook() -> Response:
    """معالجة تحديثات تليجرام بوضعها في update_queue"""
    data = await request.get_json()
    if data:
        update = Update.de_json(data, application.bot)
        await application.update_queue.put(update)
        return Response(status=HTTPStatus.OK)
    return Response(status=HTTPStatus.BAD_REQUEST)

# تشغيل الـ application قبل بدء السيرفر وبعد إيقافه
@quart_app.before_serving
async def before_serving():
    await application.start()

@quart_app.after_serving
async def after_serving():
    await application.stop()

# لا حاجة لـ if __name__ == "__main__"، لأن Uvicorn سيشغل الـ app مباشرة