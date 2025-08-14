from fastapi import FastAPI, Request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ===== إعدادات البوت =====
TOKEN = "6217434623:AAGZqBjmVz-VZ6W0y0MXeN0pAtXyRjSZTNk"
ADMIN_ID = 5581457665
WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = f"https://boteleinsta.onrender.com{WEBHOOK_PATH}"

# ===== FastAPI =====
app = FastAPI()

# ===== تطبيق البوت =====
bot_app = Application.builder().token(TOKEN).build()

# ===== حسابات المالك =====
instagram_accounts = ["insta1", "insta2", "insta3"]
telegram_accounts = ["tg1", "tg2", "tg3"]

# ===== لوحة المالك =====
def main_menu():
    keyboard = []
    for acc in instagram_accounts:
        keyboard.append([InlineKeyboardButton(f"📸 {acc}", callback_data=f"insta_{acc}")])
    for acc in telegram_accounts:
        keyboard.append([InlineKeyboardButton(f"💬 {acc}", callback_data=f"tg_{acc}")])
    keyboard.append([InlineKeyboardButton("⚙️ الإعدادات", callback_data="settings")])
    keyboard.append([InlineKeyboardButton("ℹ️ المساعدة", callback_data="help")])
    return InlineKeyboardMarkup(keyboard)

# ===== رسالة توقف البوت للمستخدمين =====
def stopped_message():
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("👤 تواصل مع المالك", url="https://t.me/e2E12")]
    ])
    return "⛔ البوت متوقف💎", keyboard

# ===== أمر /start =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id == ADMIN_ID:
        await update.message.reply_text("👋 أهلاً بك يا Batman! اختر ماتشاء 🦾.:", reply_markup=main_menu())
    else:
        text, keyboard = stopped_message()
        await update.message.reply_text(text, reply_markup=keyboard)

# ===== الرد على أزرار المالك =====
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if user_id != ADMIN_ID:
        text, keyboard = stopped_message()
        await query.edit_message_text(text, reply_markup=keyboard)
        return

    data = query.data
    if data.startswith("insta_"):
        account = data.replace("insta_", "")
        await query.edit_message_text(f"📸 إدارة حساب باتمنگرام: {account}", reply_markup=main_menu())
    elif data.startswith("tg_"):
        account = data.replace("tg_", "")
        await query.edit_message_text(f"💬 إدارة حساب باتمنگرام: {account}", reply_markup=main_menu())
    elif data == "settings":
        await query.edit_message_text("⚙️ إعدادات البوت:\n- اللغة: العربية\n- الإشعارات: مفعلة", reply_markup=main_menu())
    elif data == "help":
        await query.edit_message_text("ℹ️ المساعدة:\n- استخدم الأزرار للتحكم في حساباتك.", reply_markup=main_menu())

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

# ===== إضافة Handlers =====
bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(CallbackQueryHandler(button_handler))
