from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import asyncio, os

class TelegramClient:

    def __init__(self):
        self.chat_id = os.getenv('TELEGRAM_CHATID')
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')

    async def send_message(self, message):
        await Bot(self.bot_token).send_message(chat_id=self.chat_id, text=message)

    def start_listening(self, chat_engine_handler):

        print('[+] Telegram bot listening to responses...')

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            if (int(update.message.chat_id) != int(self.chat_id)):
                await update.message.reply_text("Lo siento. Soy un bot privado.")
                return
            response = chat_engine_handler(update.message.text)
            await update.message.reply_text(response)

        application = Application.builder().token(self.bot_token).build()

        #application.add_handler(CommandHandler("start", start))
        #application.add_handler(CommandHandler("help", help_command))

        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

        # Run the bot until the user presses Ctrl-C
        application.run_polling()