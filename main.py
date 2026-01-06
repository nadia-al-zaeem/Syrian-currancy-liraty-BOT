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

TOKEN = os.environ.get("BOT_TOKEN")
PORT = int(os.environ.get("PORT", 5000))
WEBHOOK_URL = os.environ.get("RENDER_EXTERNAL_URL")

flask_app = Flask(__name__)
telegram_app = ApplicationBuilder().token(TOKEN).build()

# Handlers
telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CallbackQueryHandler(button_handler))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

# Webhook endpoint (sync حتى لا يظهر خطأ Flask async)
@flask_app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, telegram_app.bot)
    asyncio.get_event_loop().create_task(telegram_app.process_update(update))
    return "OK", 200

# إعداد Webhook وتشغيل البوت
async def run_bot():
    await telegram_app.initialize()
    if WEBHOOK_URL:
        full_url = f"{WEBHOOK_URL}/{TOKEN}"
        await telegram_app.bot.set_webhook(full_url)
        print(f"✅ Webhook set to: {full_url}")
    else:
        print("⚠️ RENDER_EXTERNAL_URL not found!")
    await telegram_app.start()
    print("🚀 Telegram bot started successfully!")

loop = asyncio.get_event_loop()
loop.create_task(run_bot())

if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=PORT)