from num2words import num2words
from pyarabic.number import text2number


# old to new:
async def handler_new_numbers(update, context):
    text = update.message.text.strip()
    # 1. محاولة تحويل النص العربي إلى رقم
    # سواء كان النص رقمًا (مثل '1500000') أو نصًا عدديًا (مثل 'مليون وخمسمائة')
    # أولاً، التحقق مما إذا كان المدخل رقمًا عشريًا أو رقمًا عادياً لنتجنب مشاكل المعالجة النصية إذا كان رقمًا
    if text.replace('.', '', 1).isdigit():
        new_number = int(float(text))
    else:
        try:
            # استخدام دالة pyarabic لتحويل النص إلى رقم
            new_number = text2number(text)
        except Exception:
            update.message.reply_text("حدث خطأ في الادخال حاول مجددا ❌")

            new_number = 0
            
    # 2. التحقق من الرقم الجديد
    if new_number is None or new_number <= 0:
        await update.message.reply_text(
            "عذراً، لم أستطع فهم النص المدخل كرقم صحيح. يرجى إدخال رقم (مثلاً: 10000) أو نص عددي واضح (مثلاً: عشرة آلاف).❗️❗️"
        )
        return
    
    
    result = new_number / 100
    
    # 4. تحويل النتيجة الجديدة إلى نص عربي مكتوب
    # نستخدم int() إذا كانت النتيجة لا تحتوي على كسور لتجنب أخطاء num2words
    words_input = int(result) if result == int(result) else result
    words = num2words(words_input, lang="ar")

    # 5. الرد على المستخدم
    # أضفت تنسيقًا للأرقام لتسهيل قراءتها
    await update.message.reply_text(
        f"القيمة الأصلية  ✨\n{new_number:,.0f}\n\n"
        f"القيمة بالعملة الجديدة ✨ \n{result:,.2f}\n\n"
        f"✍️ كتابة:\n{words} ليرة"
    )



#new to old:
async def handler_old_numbers(update, context):
    text = update.message.text.strip()
    # 1. محاولة تحويل النص العربي إلى رقم
    # سواء كان النص رقمًا (مثل '1500000') أو نصًا عدديًا (مثل 'مليون وخمسمائة')
    
    # أولاً، التحقق مما إذا كان المدخل رقمًا عشريًا أو رقمًا عادياً لنتجنب مشاكل المعالجة النصية إذا كان رقمًا
    if text.replace('.', '', 1).isdigit():
        new_number = int(float(text))
    else:
        try:
            # استخدام دالة pyarabic لتحويل النص إلى رقم
            new_number = text2number(text)
        except Exception:
            update.message.reply_text("حدث خطأ في الادخال حاول مجددا ❌")

            new_number = 0
            
    # 2. التحقق من الرقم الجديد
    if new_number is None or new_number <= 0:
        await update.message.reply_text(
            "عذراً، لم أستطع فهم النص المدخل كرقم صحيح. يرجى إدخال رقم (مثلاً: 100) أو نص عددي واضح .❗️❗️"
        )
        return
    
    
    result = new_number *100
    
    # 4. تحويل النتيجة الجديدة إلى نص عربي مكتوب
    # نستخدم int() إذا كانت النتيجة لا تحتوي على كسور لتجنب أخطاء num2words
    words_input = int(result) if result == int(result) else result
    words = num2words(words_input, lang="ar")

    # 5. الرد على المستخدم
    # أضفت تنسيقًا للأرقام لتسهيل قراءتها
    await update.message.reply_text(
        f"القيمة الأصلية  ✨\n{new_number:,.0f}\n\n"
        f"القيمة بالعملة القديمة ⭕️ \n{result:,.2f}\n\n"
        f"✍️ كتابة:\n{words} ليرة"
    )