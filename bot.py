import json
import logging
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# Setup runtime logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Config options (Fill these out during setup)
BOT_TOKEN = "8832726944:AAHIEt7_YPu2DdNSHBLEdjdKh4d26bKpbmg"
WEB_APP_URL = "https://dannynewg.github.io/alfaruk-support/"  # URL where your index.html is hosted
ADMIN_CHAT_ID = "YOUR_ADMIN_CHAT_OR_GROUP_ID"  # Optional: Pass tickets straight to your operations team

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a welcome message and a keyboard option targeting the Mini App."""
    keyboard = [
        [
            KeyboardButton(
                text="📱 Open Support / ድጋፍ ማዕከል",
                web_app=WebAppInfo(url=WEB_APP_URL)
            )
        ]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    welcome_text = (
        "✨ **Welcome to Al-faruk Super App Support Bot!** ✨\n\n"
        "We are dedicated to helping you. Click the button below to open our interactive Support Mini App, "
        "where you can easily submit technical issues, general inquiries, or feedback in either English or Amharic.\n\n"
        "--- \n\n"
        "✨ **እንኳን ወደ አል-ፋሩቅ ሱፐር አፕ ድጋፍ ሰጪ ቦት በሰላም መጡ!** ✨\n\n"
        "እርስዎን ለመርዳት ሁልጊዜ ዝግጁ ነን። ቴክኒካዊ ችግሮችን ለመጠቆም፣ አጠቃላይ ጥያቄዎችን ለመጠየቅ ወይም አስተያየት ለመስጠት ከታች ያለውን ቁልፍ በመጫን የድጋፍ ሚኒ አፑን ይክፈቱ።"
    )
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

async def handle_web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Catches payload submitted by tg.sendData() from front-end."""
    raw_data = update.message.web_app_data.data
    parsed_data = json.loads(raw_data)
    
    user = update.effective_user
    username = f"@{user.username}" if user.username else "No Username Available"
    
    lang = parsed_data.get("language", "en")
    issue_type = parsed_data.get("issue_type", "N/A")
    description = parsed_data.get("description", "N/A")
    contact = parsed_data.get("contact", "N/A")
    
    # Formulate a structured internal support notification log
    ticket_payload = (
        "🎫 **[New Support Ticket Received]**\n\n"
        f"👤 **Customer Name:** {user.full_name}\n"
        f"🆔 **Telegram ID:** `{user.id}`\n"
        f"📱 **Handle:** {username}\n"
        f"🌐 **Preferred Interface Language:** {'English 🇬🇧' if lang == 'en' else 'Amharic 🇪🇹'}\n"
        f"📂 **Category:** {issue_type}\n"
        f"📞 **Phone Provided:** {contact}\n\n"
        f"📝 **Description:**\n{description}"
    )
    
    # Send user confirmation message based on their localized form submission choice
    if lang == 'en':
        reply_message = (
            "✅ **Thank you! Your ticket has been recorded.**\n\n"
            "Our technical support team will evaluate your request and reply to you directly through this chat profile shortly."
        )
    else:
        reply_message = (
            "✅ **እናመሰግናለን! የድጋፍ ጥያቄዎ በተሳካ ሁኔታ ተመዝግቧል።**\n\n"
            "የቴክኒክ ቡድናችን ያቀረቡትን መረጃ ገምግሞ በዚህ ቦት በኩል በቅርቡ ምላሽ ይሰጥዎታል።"
        )
        
    await update.message.reply_text(reply_message, parse_mode="Markdown")
    
    # Optional: Forward ticket text directly to an Admin or Operations Group Channel
    if ADMIN_CHAT_ID != "YOUR_ADMIN_CHAT_OR_GROUP_ID":
        try:
            await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=ticket_payload, parse_mode="Markdown")
        except Exception as e:
            logging.error(f"Failed to forward ticket payload to admin channel: {e}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Handler Mappings
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_web_app_data))
    
    print("Al-faruk Support Bot Engine has started tracking...")
    app.run_polling()

if __name__ == '__main__':
    main()