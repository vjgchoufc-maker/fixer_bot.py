import ast  
import io  
import sys  
from telegram import Update  
from telegram.ext import (  
    Application,  
    CommandHandler,  
    ContextTypes,  
    MessageHandler,  
    filters,  
)  
import traceback  
  
# استبدل هذا بـ API Token الخاص بروبوتك  
TOKEN =  "8293785720:AAGZCRwR3_r93E-yd8S04Q0PmowCX-OPe0k"  
  
def fix_python_code(code_string):  
    """  
    يقوم بتحليل كود بايثون لتحديد وتصحيح الأخطاء الشائعة.  
    """  
    errors = []  
      
    # المرحلة 1: فحص الأخطاء النحوية (SyntaxError)  
    try:  
        ast.parse(code_string)  
    except SyntaxError as e:  
        # إضافة رسالة خطأ واضحة  
        errors.append(f"❌ خطأ نحوي في السطر {e.lineno}: {e.msg}")  
      
    # المرحلة 2: فحص أخطاء المسافات البادئة (IndentationError)  
    # لا يمكن الاعتماد على compile لتحديد المسافات البادئة بشكل دقيق دائماً  
    # لذا سنكتفي بالأخطاء النحوية التي يلتقطها ast  
    # هذه الطريقة أكثر أماناً وتجنباً للمشاكل  
      
    if not errors:  
        return "✅ **تم الفحص بنجاح.** لم يتم العثور على أخطاء نحوية."  
    else:  
        error_message = "⚠️ **تم العثور على الأخطاء التالية:**\n\n"  
        for error in errors:  
            error_message += f"{error}\n"  
          
        # إضافة إرشادات بسيطة لمساعدة المستخدم  
        error_message += "\n💡 **نصيحة:** تأكد من الأقواس، علامات الاقتباس، والنقاط الرأسية."  
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
    # التحقق من وجود رسالة مقتبس منها  
    if not update.message.reply_to_message:  
        await update.message.reply_text("يرجى الرد على رسالة تحتوي على الكود بالأمر /fix.")  
        return  
  
    # استخراج الكود من الرسالة المقتبس منها  
    code_text = update.message.reply_to_message.text  
    if not code_text:  
        await update.message.reply_text("الرسالة المقتبس منها لا تحتوي على كود.")  
        return  
  
    # استخدام try-except لضمان عدم توقف البوت في حال حدوث أي خطأ غير متوقع  
    try:  
        result_message = fix_python_code(code_text)  
        await update.message.reply_text(result_message, parse_mode="Markdown")  
    except Exception as e:  
        # إرسال رسالة خطأ عامة للمستخدم  
        await update.message.reply_text(  
            f"❌ حدث خطأ غير متوقع: {e}\n\n"  
            "يرجى التأكد من أن الكود بتنسيق صحيح.",  
            parse_mode="Markdown"  
        )  
        # طباعة الخطأ في وحدة التحكم للمطور  
        print(f"An unexpected error occurred: {traceback.format_exc()}")  
  
  
def main() -> None:  
    """تشغيل الروبوت."""  
    application = Application.builder().token(TOKEN).build()  
  
    application.add_handler(CommandHandler("start", start))  
    application.add_handler(CommandHandler("fix", fix_code_handler))  
      
    # تشغيل الروبوت  
    application.run_polling(allowed_updates=Update.ALL_TYPES)  
  
  
if __name__ == "__main__":  
    main()  
