
import httpx
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import (ContextTypes,CommandHandler,CallbackQueryHandler,MessageHandler,filters,)
#gold
async def get_gold_price_damascus():
    url = "https://www.zahabprice.com/ar-sy"
    try:
        async with httpx.AsyncClient(timeout=20, follow_redirects=True) as client:
            response = await client.get(url)
            response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        rows = soup.select("table tbody tr")
        prices = {}
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 2:
                name = cols[0].get_text(strip=True)
                price = cols[1].get_text(strip=True)

                # تنظيف النص من الفراغات وتكرار "ل.س"
                price = price.replace("\n", "").replace("\r", "").strip()
                if price.endswith("ل.س ل.س"):
                    price = price.replace("ل.س ل.س", "ل.س")

                prices[name] = price

        # الرسالة النهائية
        message = (
            "🥇 **سعر الذهب اليوم في دمشق**\n"
            "📍 الأسعار بحسب موقع **ZahabPrice**\n\n"
            f"🥇 عيار 24: {prices.get('عيار 24', 'غير متوفر')}\n"
            f"🥇 عيار 22: {prices.get('عيار 22', 'غير متوفر')}\n"
            f"🥇 عيار 21: {prices.get('عيار 21', 'غير متوفر')}\n"
            f"🥇 عيار 18: {prices.get('عيار 18', 'غير متوفر')}\n"
            f"عزيزي المستخدم هذه بيانات تقديرية نظرا لعدم وجود سعر ثابت  لكل المحلات ,وجب التنويه ❤️"
        )

        return message

    except Exception as e:
        return f"❗️ خطأ داخلي: {e}"
    



#dolar


'''''
import httpx
from bs4 import BeautifulSoup

async def get_usd_price_sp_today():
    url = "https://sp-today.com/currency/us_dollar/city/damascus"
    try:
        async with httpx.AsyncClient(timeout=20, follow_redirects=True) as client:
            response = await client.get(url)
            response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # البحث عن عناصر السعر
        buy_element = soup.select_one(".buy")   # عنصر سعر الشراء
        sell_element = soup.select_one(".sell") # عنصر سعر المبيع

        usd_buy = buy_element.get_text(strip=True) if buy_element else "غير متوفر"
        usd_sell = sell_element.get_text(strip=True) if sell_element else "غير متوفر"

        message = (
            "💵 **سعر الدولار اليوم في دمشق**\n"
            "📍 بحسب موقع **SP‑Today**\n\n"
            f"💵 شراء: {usd_buy}\n"
            f"💵 مبيع: {usd_sell}"
        )

        return message

    except Exception as e:
        return f"❗ خطأ داخلي: {e}"
        '''



