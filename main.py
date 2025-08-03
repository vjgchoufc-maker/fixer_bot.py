import ast
import io
import os
import sys
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)
from dotenv import load_dotenv

# قم بتحميل متغيرات البيئة من ملف .env
load_dotenv()

# استبدل هذا بـ API Token الخاص بروبوتك
TOKEN = os.getenv("TOKEN")
# عنوان URL الخاص بك على Render، يجب أن يتطابق مع الدومين الخاص بخدمتك
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

def fix_python_code(code_string):
    """
    يقوم بتحليل كود بايثون لتحديد وتصحيح الأخطاء الشائعة.
    """
    errors = []
    output_buffer = io.StringIO()

    # المرحلة 1: فحص الأخطاء النحوية (SyntaxError)
    try:
        ast.parse(code_string)
    except SyntaxError as e:
        errors.append(f"❌ خطأ نحوي في السطر {e.lineno}: {e.msg}")

    # المرحلة 2: فحص أخطاء المسافات البادئة (IndentationError)
    try:
        # توجيه مخرجات الأخطاء إلى متغير
        sys.stderr = output_buffer
        compile(code_string, '<string>', 'exec')
    except IndentationError as e:
        errors.append(f"❌ خطأ في المسافات البادئة في السطر {e.lineno}: {e.msg}")
    finally:
        # إعادة مخرجات الأخطاء إلى وضعها الطبيعي
        sys.stderr = sys.__stderr__

    if not errors:
        return "✅ **تم الفحص بنجاح.** لم يتم العثور على أخطاء نحوية أو في المسافات البادئة."
    else:
        error_message = "⚠️ **تم العثور على الأخطاء التالية:**\n\n"
        for error in errors:
            error_message += f"{error}\n"
        return error_message


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """إرسال رسالة ترحيب عند استخدام أمر /start."""
    await update.message.reply_text(
        "أنا روبوت تصحيح أكواد بايثون! أرسل لي كودك، ثم أجب على الرسالة بالأمر /fix."
    )


async def fix_code_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    يقوم بمعالجة الأمر /fix ويصحح الكود المرفق.
    """
    if not update.message.reply_to_message:
        await update.message.reply_text("يرجى الرد على رسالة تحتوي على الكود بالأمر /fix.")
        return

    code_text = update.message.reply_to_message.text
    if not code_text:
        await update.message.reply_text("الرسالة المقتبس منها لا تحتوي على كود.")
        return

    result_message = fix_python_code(code_text)

    await update.message.reply_text(result_message, parse_mode="Markdown")


def main() -> None:
    """تشغيل الروبوت."""
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("fix", fix_code_handler))

    # تعيين Webhook
    application.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", "8443")),
        url_path=TOKEN,
        webhook_url=WEBHOOK_URL,
    )


if __name__ == "__main__":
    main()

