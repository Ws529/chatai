import logging
from telegram import Update
# from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler,  MessageHandler, filters
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from chat_history_utils import save_chat_to_history
from dotenv import load_dotenv
import os
from app import chai
load_dotenv()
TOKEN = os.getenv('apitele')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # user_message = update.message.text
    # logging.info(f"Pesan dari pengguna: {user_message}")
    response = chai(update.message.text)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)
    user_id = update.effective_user.id
    save_chat_to_history(update.message.text, response)
    logging.info(f"Pesan dari pengguna dengan ID {user_id}: {update.message.text}")

# async def log_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # user_message = 

if __name__ == '__main__':
    application = Application.builder().token(TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    # message_handler = MessageHandler()
    application.add_handler(start_handler)
    # Uncomment the line below to add the MessageHandler for handling messages
    application.add_handler(MessageHandler(filters.TEXT, handle_message))
    # MessageHandler(filters.TEXT, handle_message)
    
    application.run_polling()