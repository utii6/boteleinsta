import os
from fastapi import FastAPI, Request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ===== إعدادات البوت =====
TOKEN = "6217434623:AAGZqBjmVz-VZ6W0y0MXeN0pAtXyRjSZTNk"
ADMIN_ID = 5581457665  # معرف المدير
WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = f"https://teestrbot.onrender.com{WEBHOOK_PATH}"

# ===== إنشاء تطبيق FastAPI =====
app = FastAPI()

# ===== إنشاء تطبيق البوت =====
bot_app = Application.builder().token(TOKEN).build()

# ===== لوحة الأزرار الرئيسية =====
def main_menu():
    keyboard = [
        [InlineKeyboardButton("📊 إحصائيات الحساب", callback_data="stats")],
        [InlineKeyboardButton("🔄 تحديث البيانات", callback_data="refresh")],
        [InlineKeyboardButton("📥 تسجيل الدخول", callback_data="login")],
        [InlineKeyboardButton("📤 تسجيل الخروج", callback_data="logout")],
        [InlineKeyboardButton("⚙️ الإعدادات", callback_data="settings")],
        [InlineKeyboardButton("ℹ️ المساعدة", callback_data="help")]
    ]
    return InlineKeyboardMarkup(keyboard)

# ===== أمر /start =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "أهلاً بك قاسم !الأدمن والوحيد بغرفة BatMan😎🦾.\n"
        "اختر لتنقذ المدينـه:",
        reply_markup=main_menu()
    )

# ===== ردود الأزرار =====
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "stats":
        await query.edit_message_text("📊 إحصائيات الحساب:\n- المتابعين: 1234\n- المنشورات: 56", reply_markup=main_menu())
    elif query.data == "refresh":
        await query.edit_message_text("🔄 تم تحديث البيانات بنجاح ✅", reply_markup=main_menu())
    elif query.data == "login":
        await query.edit_message_text("📥 أرسل بيانات الدخول الآن:", reply_markup=main_menu())
    elif query.data == "logout":
        await query.edit_message_text("📤 تم تسجيل الخروج من الحساب.", reply_markup=main_menu())
    elif query.data == "settings":
        await query.edit_message_text("⚙️ الإعدادات:\n- اللغة: العربية\n- الإشعارات: مفعلة", reply_markup=main_menu())
    elif query.data == "help":
        await query.edit_message_text("ℹ️ المساعدة:\n- استخدم الأزرار للتحكم في حسابك بسهولة.", reply_markup=main_menu())

# ===== استقبال Webhook =====
@app.post(WEBHOOK_PATH)
async def webhook_handler(request: Request):
    data = await request.json()
    update = Update.de_json(data, bot_app.bot)
    await bot_app.process_update(update)
    return {"status": "ok"}

# ===== ضبط Webhook عند التشغيل =====
@app.on_event("startup")
async def set_webhook():
    await bot_app.bot.set_webhook(url=WEBHOOK_URL)
    print(f"✅ Webhook set to {WEBHOOK_URL}")

# ===== إضافة الأوامر =====
bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(CallbackQueryHandler(button_handler))
