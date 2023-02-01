#!/usr/bin/env python3
import logging
import os
import openai
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler


openai.api_key = os.environ.get("API_KEY")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

memory = ""

def clear_memory(update, context):
    global memory
    memory = ""
    context.bot.send_message(chat_id=update.effective_chat.id, text="Memory cleared.")

def chat(update, context):
    global memory
    query = memory+" "+update.message.text
    memory = query
    print(memory)
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=query,
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.7,
    )
    
    result = response["choices"][0]["text"]
    keyboard = [[telegram.InlineKeyboardButton("Clear Memory", callback_data="clear_memory")]]
    reply_markup = telegram.InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text=result, reply_markup=reply_markup)

def main():
    TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text, chat))
    dp.add_handler(CallbackQueryHandler(clear_memory, pattern='clear_memory'))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

