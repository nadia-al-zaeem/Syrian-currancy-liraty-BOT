#this is main code
''''
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
#test

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

#just webhook
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

# تحميل المتغيرات من .env
load_dotenv()

TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("RENDER_EXTERNAL_URL")   # رابط التطبيق على Render
PORT = int(os.environ.get("PORT", 10000))             # Render يحدد المنفذ

flask_app = Flask(__name__)

telegram_app = ApplicationBuilder().token(TOKEN).build()

# Handlers
telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CallbackQueryHandler(button_handler))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

# Route للتأكد أن السيرفر شغال
@flask_app.route("/")
def home():
    return "Bot is running!", 200

# Route للـ webhook
@flask_app.route("/webhook", methods=["POST"])


@flask_app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    print("📩 Received update:", data)   # يظهر في الـ logs
    update = Update.de_json(data, telegram_app.bot)
    # معالجة التحديث مباشرة
    asyncio.get_event_loop().create_task(telegram_app.process_update(update))
    return "OK", 200

if __name__ == "__main__":
    # تشغيل البوت بالـ webhook
    telegram_app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path="webhook",
        webhook_url=f"{WEBHOOK_URL}/webhook"
    )
    '''''
#right code:

import os
from telegram.ext import (
ApplicationBuilder,CommandHandler,CallbackQueryHandler,MessageHandler, filters
)
from handlers.start import start, button_handler, message_handler
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("RENDER_EXTERNAL_URL")
PORT = int(os.environ.get("PORT", 10000))

telegram_app = ApplicationBuilder().token(TOKEN).build()

# Handlers
telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CallbackQueryHandler(button_handler))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))




if __name__ == "__main__":
    
    telegram_app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path="webhook",
        webhook_url=f"{WEBHOOK_URL}/webhook"
    )