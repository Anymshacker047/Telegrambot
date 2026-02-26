import sys
import types
sys.modules['imghdr'] = types.ModuleType('imghdr')
import os
import requests
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Environment variables load karein
load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
API_KEY = os.getenv("ABSTRACT_API_KEY")

def start(update, context):
    update.message.reply_text("👋 Bhai, number bhejo (with country code, e.g., +91...) aur main uski kundli nikaal dunga!")

def get_phone_info(update, context):
    phone_number = update.message.text
    url = f"https://phonevalidation.abstractapi.com/v1/?api_key={API_KEY}&phone={phone_number}"
    
    update.message.reply_text("🔍 Checking... Thoda sabar karo.")

    try:
        response = requests.get(url)
        data = response.json()

        if data.get("valid") is False:
            update.message.reply_text("❌ Ye number sahi nahi lag raha. Check karke firse bhejo.")
            return

        # Formatting Output for Telegram
        msg = (
            f"📞 *Phone Info Found:*\n\n"
            f"📍 *Location:* {data.get('location', 'N/A')}\n"
            f"🏢 *Carrier:* {data.get('carrier', 'N/A')}\n"
            f"🌍 *Country:* {data.get('country', {}).get('name', 'N/A')}\n"
            f"📱 *Line Type:* {data.get('type', 'N/A')}\n"
            f"✅ *Valid:* {data.get('valid')}"
        )
        update.message.reply_markdown(msg)

    except Exception as e:
        update.message.reply_text(f"⚠️ Error aa gaya bhai: {str(e)}")

def main():
    # Aapka version 12.8 hai, isliye use_context=True zaroori hai
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, get_phone_info))

    print("🚀 Bot start ho gaya hai...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()