'''''
from telegram import Update
from telegram.ext import ContextTypes
#from keyboards.inline_keyboard import get_follow_button,get_conversion_keyboard
from handlers.converting import handler_new_numbers,handler_old_numbers
from handlers.prices import get_gold_price_damascus
from keyboards.inline_keyboard import get_conversion_keyboard,get_follow_button
#تخزين مستخدمين قاموا ي استخدام بوت 

followed_users=set()
#تحقق ان مستخدم مفعل ام لا
def is_user_followed(user_id: int):
    return user_id in followed_users
#اضافة مستخدم الى set على انه مفعل
def set_user_followed(user_id:int):
    followed_users.add(user_id)





async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id=update.effective_user.id
    if is_user_followed(user_id):

        await update.message.reply_text( "مرحباً! البوت مفعل الآن ✅\n"
            "أدخل مبلغاً بالليرة السورية القديمة لتحويله إلى الجديدة.\n"
            "او لمعرفة قيمة المبلغ بالدولار او قيمته بالذهب \n"

)
        
        await update.message.reply_text(
        "اختر نوع تحويل آخر:",
        reply_markup=get_conversion_keyboard()
           )   

    else: 
        await update.message.reply_text(
        "👋 أهلاً بك!\n\n"
        "تم تطوير هذا البوت بواسطة:\n"
        "👩‍💻 المهندسة فرح حلواني\n"
        "👩‍💻 المهندسة ناديا الزعيم\n\n"
        "لكي تستفيد من البوت، يرجى متابعة حساب:\n"
        "📸 https://www.instagram.com/binary_team_10\n\n"
        "بعد المتابعة اضغط على الزر بالأسفل لتفعيل البوت."
        ,reply_markup=get_follow_button()
        )

async def button_handler(update:Update,context:ContextTypes.DEFAULT_TYPE):
    query=update.callback_query
    user_id=query.from_user.id
    await query.answer()

    if query.data == "follow":
        set_user_followed(user_id)
        await query.edit_message_text(
             "تم التفعيل 🎉\nاختر نوع التحويل:",
         reply_markup=get_conversion_keyboard()
        )

    elif query.data == "new_currency":
        context.user_data["mode"]="old_to_new"
        await query.edit_message_text("💰 أدخل المبلغ بالليرة القديمة للتحويل إلى الجديدة:")

      
    elif query.data == "old_currency":
        context.user_data["mode"] = "new_to_old"
        await query.edit_message_text("💰 أدخل المبلغ بالليرة الجديدة للتحويل إلى القديمة:")
         
    elif query.data == "gold_currency":
        await query.message.edit_text("⏳ جاري جلب سعر الذهب...")
        
        # استدعاء دالة جلب سعر الذهب من الـ API
        gold_price_message = await get_gold_price_damascus()
        
        # إرسال الرسالة للمستخدم مع سعر الذهب ولوحة المفاتيح
        await query.message.reply_text(
            f"🥇 **سعر الذهب اليوم في دمشق:**\n\n{gold_price_message}",
            reply_markup=get_conversion_keyboard()
        )

    elif query.data == "dolar_currency":
        await query.message.edit_text("⏳ جاري جلب سعر الدولار...")

        # هنا تكتب الدالة مباشرة داخل الشرط
        async def get_usd_price():
         return "لكي تتمكن من معرفة سعر صرف الدولار\nاضغط هنا : https://sp-today.com/"

        # استدعاء الدالة فقط عند الضغط على زر الدولار
        dolar_price_message = await get_usd_price()

        await query.message.reply_text(
            f"{dolar_price_message}",
            reply_markup=get_conversion_keyboard()
        )    
      
  

async def message_handler(update, context):
    text = update.message.text.strip()
    mode = context.user_data.get("mode")

    # إذا لم يحدد نوع التحويل
    if not mode:
        return

    # إذا كتب المستخدم رقم → نفذ التحويل مباشرة
    #if text.replace('.', '', 1).isdigit():

        # تنفيذ التحويل
    if mode == "old_to_new":
            await handler_new_numbers(update, context)
            await update.message.reply_text(
        "اختر نوع تحويل آخر:",
        reply_markup=get_conversion_keyboard()
    )


    elif mode == "new_to_old":
            await handler_old_numbers(update, context)
        # بعد التحويل أظهر الأزرار مباشرة
            await update.message.reply_text(
            "اختر نوع تحويل آخر:",
            reply_markup=get_conversion_keyboard()
        )

            context.user_data.pop("mode", None)
            return
            '''


#testing
from telegram import Update
from telegram.ext import ContextTypes
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # لا تستخدم لوحة مفاتيح أو منطق 'followed_users' مؤقتاً
   
    # للتأكد من أن الكود لا ينهار عند أول سطر
    print("START HANDLER CALLED SUCCESSFULLY.") 
    await update.message.reply_text("البوت يعمل بنجاح!")