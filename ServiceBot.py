from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from BaseBot import BaseBot


class ServiceBot(BaseBot):
    MAIN_CHECKLIST = [
        "Релиз установлен на Test",
        "Регресс командой QA ES",
        "Тестирование командой QA АБ",
        "Регресс командой QA АБ",
        "Релиз установлен на Test 2",
        "Релиз установлен на Dev",
        "Релиз установлен на Prod",
    ]

    STATUS_ICONS = {
        None: "⬜️",  # Не выбрано
        "in_progress": "⚙️",  # В процессе
        "passed": "✅",  # Успешно
        "failed": "❌"  # Не пройдено
    }

    def __init__(self, application):
        super().__init__(application)
        self.session = {
            "main_checklist": [None] * len(self.MAIN_CHECKLIST),
        }

    def generate_keyboard(self, checklist, statuses, prefix):
        keyboard = [
            [InlineKeyboardButton(f"{self.STATUS_ICONS[statuses[i]]} {item}", callback_data=f"{prefix}_{i}")]
            for i, item in enumerate(checklist)
        ]
        return InlineKeyboardMarkup(keyboard)

    async def start(self, update: Update, context: CallbackContext):
        commands = "Доступные команды:\n/check - Запросить чек-лист\n/restart - Сбросить состояние чек-листа"
        await self.send_message(update, f"👋 Привет! Начинаем процесс релиза.\n\n{commands}")

    async def deploy(self, update: Update, context: CallbackContext):
        await self.send_message(update, "📋 Чек-лист релиза: ",
                                self.generate_keyboard(self.MAIN_CHECKLIST, self.session["main_checklist"], "main"))

    async def restart(self, update: Update, context: CallbackContext):
        self.session = {
            "main_checklist": [None] * len(self.MAIN_CHECKLIST),
        }
        await self.send_message(update, "🔄 Чек-лист сброшен. Используйте /check для повторного запроса.")

    async def handle_button_click(self, update: Update, context: CallbackContext):
        query = update.callback_query
        data = query.data
        index = int(data.split("_")[1])
        self.session["main_checklist"][index] = self.cycle_status(self.session["main_checklist"][index])
        await self.edit_message(query, "📋 Чек-лист релиза:",
                                self.generate_keyboard(self.MAIN_CHECKLIST, self.session["main_checklist"], "main"))

    def cycle_status(self, current_status):
        statuses = [None, "in_progress", "passed", "failed"]
        return statuses[(statuses.index(current_status) + 1) % len(statuses)]
