from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
import shutil

from BaseBot import BaseBot


class ServiceBot(BaseBot):
    MAIN_CHECKLIST = [
        "Релиз установлен на Test",
        "Регресс командой QA ES",
        "Тестирование доработок командой QA АБ",
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

    async def help(self, update: Update, context: CallbackContext):
        commands = (f"""Доступные команды:
            /help - Список доступных команд
            /check - Запросить чек-лист
            /restart - Сбросить состояние чек-листа
            /FAQ - Возможные состояния чек-листа""")
        await self.send_message(update,
        f"""👋 Привет! Начинаем процесс релиза.

        {commands}""")

    async def deploy(self, update: Update, context: CallbackContext):
        await self.send_message(update, "📋 Чек-лист релиза: ",
                                self.generate_keyboard(self.MAIN_CHECKLIST, self.session["main_checklist"], "main"))

    async def restart(self, update: Update, context: CallbackContext):
        self.session = {
            "main_checklist": [None] * len(self.MAIN_CHECKLIST),
        }
        await self.send_message(update, "🔄 Чек-лист сброшен. Используйте /check для повторного запроса.")

    async def FAQ(self, update: Update, context: CallbackContext):
        terminal_width = shutil.get_terminal_size().columns
        separator = "-" * terminal_width
        await self.send_message(update,
        f"""ℹ️ *Чек-лист создан для обеспечения прозрачности текущего статуса релиза платформы IPN.*
        {separator} 
        *Полезные ссылки:*
            🔗[Процесс тестирования проекта Импортозамещение телефонии](https://confluence.moscow.alfaintra.net/pages/viewpage.action?pageId=1763449160)
            🔗[Отчеты тестирования релизов IPN](https://confluence.moscow.alfaintra.net/pages/viewpage.action?pageId=2128949560)
            🔗[Инструкции для QA](https://confluence.moscow.alfaintra.net/pages/viewpage.action?pageId=1865411686)
            🔗[Баги проекта Импортозамещение телефони](https://jira.moscow.alfaintra.net/secure/Dashboard.jspa?selectPageId=109712)
            🔗[Баги проекта по корневым причинам](https://jira.moscow.alfaintra.net/secure/Dashboard.jspa?selectPageId=112914)
            🔗[Тестовая модель](https://testops.moscow.alfaintra.net/project/42/test-cases?treeId=118)
                                        
        {separator}
        *Состояния отмеченных пунктов в соответствии с количеством нажатий на них:*
                                        
            1. ⚙️ - in progress (в работе)
            2. ✅ - passed (пройден успешно)
            3. ❌ -  failed (пройден с ошибками)""")

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
