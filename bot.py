from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from functools import partial

from ServiceBot import ServiceBot
from config import TOKEN

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    bot = ServiceBot(app)

    app.add_handler(CommandHandler("start", partial(bot.start)))
    app.add_handler(CommandHandler("check", partial(bot.deploy)))
    app.add_handler(CommandHandler("restart", partial(bot.restart)))
    app.add_handler(CallbackQueryHandler(bot.handle_button_click))

    print("Бот запущен...")
    app.run_polling()

if __name__ == '__main__':
    main()