from telegram import InlineKeyboardButton,InlineKeyboardMarkup

def get_follow_button():
    Keyboard=[[InlineKeyboardButton("✅ متابعة",callback_data="follow")]]
    return InlineKeyboardMarkup(Keyboard)


#بعد التحويل 

def get_conversion_keyboard():
    keyboard =[
    [InlineKeyboardButton("💰 القيمة في العملة الجديدة",callback_data="new_currency")],
     [InlineKeyboardButton("💰 القيمة في العملة القديمة",callback_data="old_currency")],
    [InlineKeyboardButton("💵 سعر الدولار اليوم ", callback_data="dolar_currency")],
    [InlineKeyboardButton("🥇 سعر الذهب اليوم ", callback_data="gold_currency")]
  ]
    return InlineKeyboardMarkup(keyboard)