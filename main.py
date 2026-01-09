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


#this is main code

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
PORT = int(os.environ.get("PORT", 10000))  # Render يحدد المنفذ

flask_app = Flask(__name__)

telegram_app = ApplicationBuilder().token(TOKEN).build()

# Handlers
telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CallbackQueryHandler(button_handler))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

@flask_app.route("/")
def home():
    return "Bot is running!", 200
# Webhook endpoint
@flask_app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    print("📩 Received update:", data)   # مهم للتشخيص
    update = Update.de_json(data, telegram_app.bot)
    telegram_app.update_queue.put_nowait(update)
    return "OK", 200

# تشغيل PTB في Thread منفصل
def run_ptb():
    print("🔥 PTB thread started")

    telegram_app.run_polling()  # هذا هو المفتاح: يستهلك الـ queue

print("🚀 Starting PTB thread...")
threading.Thread(target=run_ptb, daemon=True).start()

if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=PORT)
    




'''''
import os
import asyncio
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
PORT = int(os.environ.get("PORT", 10000))

flask_app = Flask(__name__)
telegram_app = ApplicationBuilder().token(TOKEN).build()

# Handlers
telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CallbackQueryHandler(button_handler))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

@flask_app.route("/")
def home():
    return "Bot is running!", 200

@flask_app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    print("📩 Received update:", data)
    update = Update.de_json(data, telegram_app.bot)
    asyncio.get_event_loop().create_task(telegram_app.process_update(update))
    return "OK", 200

async def init_bot():
    await telegram_app.initialize()
    await telegram_app.start()
    full_url = f"{WEBHOOK_URL}/webhook"
    await telegram_app.bot.set_webhook(full_url)
    print(f"✅ Webhook set to: {full_url}")

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(init_bot())

    flask_app.run(host="0.0.0.0", port=PORT)
    '''

import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from handlers.start import start, button_handler, message_handler  # افترضي أن هذا موجود
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("RENDER_EXTERNAL_URL") + "/webhook"  # أضيفي /webhook
PORT = int(os.environ.get("PORT", 10000))

flask_app = Flask(__name__)

telegram_app = ApplicationBuilder().token(TOKEN).build()

# إضافة handlers
telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CallbackQueryHandler(button_handler))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

# إعداد webhook مع Telegram (مهم!)
async def set_webhook():
    await telegram_app.bot.set_webhook(WEBHOOK_URL)

# شغل set_webhook عند البداية
import asyncio
asyncio.run(set_webhook())  # أو استخدمي telegram_app.initialize() ثم set_webhook

@flask_app.route("/")
def home():
    return "Bot is running!", 200

@flask_app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    print("📩 Received update:", data)  # للتشخيص
    update = Update.de_json(data, telegram_app.bot)
    telegram_app.process_update(update)  # استخدمي process_update مباشرة (بدون queue)
    return "OK", 200

if __name__ == "__main__":
    print("🚀 Starting bot with webhook...")
    flask_app.run(host="0.0.0.0", port=PORT)