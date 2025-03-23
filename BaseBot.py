from telegram import Update
from telegram.constants import ParseMode


class BaseBot:
    def __init__(self, application):
        self.app = application

    def add_handlers(self, handlers):
        for handler in handlers:
            self.app.add_handler(handler)

    async def send_message(self, update: Update, text: str, reply_markup=None):
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

    async def edit_message(self, query, text=None, reply_markup=None):
        await query.edit_message_text(text=text, reply_markup=reply_markup)
