import os
import requests
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# .env file se details uthayega
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
API_KEY = os.getenv("ABSTRACT_API_KEY")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔥 *NUMINFO Bot Ready!*\nNumber bhejo (+91...) details nikaalne ke liye.", parse_mode='Markdown')

async def handle_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    number = update.message.text
    sent_msg = await update.message.reply_text("⏳ *Searching...*", parse_mode='Markdown')

    url = f"https://phonevalidation.abstractapi.com/v1/?api_key={API_KEY}&phone={number}"
    
    try:
        response = requests.get(url)
        data = response.json()

        if data.get("valid") is False:
            await sent_msg.edit_text("❌ Galat number hai bhai, sahi format mein dalo.")
            return

        result = (
            f"📞 *PHONE DETAILS FOUND*\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"📍 *Location:* {data.get('location', 'N/A')}\n"
            f"🏢 *Carrier:* {data.get('carrier', 'N/A')}\n"
            f"🌍 *Country:* {data.get('country', {}).get('name', 'N/A')}\n"
            f"📱 *Type:* {data.get('type', 'N/A')}\n"
            f"✅ *Valid:* {data.get('valid')}\n"
            f"━━━━━━━━━━━━━━━━━━━"
        )
        await sent_msg.edit_text(result, parse_mode='Markdown')

    except Exception as e:
        await sent_msg.edit_text(f"⚠️ Error: {str(e)}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_number))
    
    print("🚀 Termux Bot is Running...")
    app.run_polling()
