import os
import ast
import traceback
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# التوكن من المتغير البيئي
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# التحقق من التوكن
if not TOKEN:
    raise ValueError("❌ لم يتم العثور على TELEGRAM_BOT_TOKEN. تأكد من إضافته في إعدادات Render.")

def fix_python_code(code_string):
    errors = []
    try:
        ast.parse(code_string)
    except SyntaxError as e:
        errors.append(f"❌ خطأ نحوي في السطر {e.lineno}: {e.msg}")

    if not errors:
        return "✅ **تم الفحص بنجاح.** لم يتم العثور على أخطاء نحوية."
    else:
        error_message = "⚠️ **تم العثور على الأخطاء التالية:**\n\n"
        for error in errors:
            error_message += f"{error}\n"
        error_message += "\n💡 **نصيحة:** تأكد من الأقواس، علامات الاقتباس، والنقاط الرأسية."
        return error_message

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "👋 أهلاً بك!\nأرسل كود بايثون ثم استخدم /fix للعثور على الأخطاء النحوية."
    )

async def fix_code_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message.reply_to_message:
        await update.message.reply_text("📌 يرجى الرد على رسالة تحتوي على كود بالأمر /fix.")
        return

    code_text = update.message.reply_to_message.text
    if not code_text:
        await update.message.reply_text("🚫 الرسالة لا تحتوي على كود.")
        return

    try:
        result_message = fix_python_code(code_text)
        await update.message.reply_text(result_message, parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(
            f"❌ حدث خطأ: {e}\n\nيرجى التحقق من الكود.",
            parse_mode="Markdown"
        )
        print(f"Unexpected error: {traceback.format_exc()}")

def main() -> None:
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("fix", fix_code_handler))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
