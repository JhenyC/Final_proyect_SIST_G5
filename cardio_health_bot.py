import logging
import telegram
import asyncio
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler
from config import TOKEN, contact_list

logging.basicConfig(format ='%(asctime)s - %(name)s - %(levelname)s - %(message)s' ,
                     level=logging.DEBUG)

async def send_emergency_message(message: str, bot):
    for chat_id in contact_list:
        await bot.send_message(chat_id = chat_id, text = message)

async def emergency(bot):
    message = "Emergency! Please help!"
    await send_emergency_message(message, bot)

async def main():
    bot = telegram.Bot(TOKEN)
    await emergency(bot)

if __name__ == '__main__':
    bot = telegram.Bot(TOKEN)
    asyncio.run(main())
    


