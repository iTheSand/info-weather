from django.conf import settings
from django.core.management.base import BaseCommand
from requests import request
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
)
from telegram.utils.request import Request

from apps.core.utils import convert_json_to_str

INTERNAL_API_PATH = "http://django-app:8080/core/weather-forecast"


class Command(BaseCommand):
    help = "Telegram bot"

    @staticmethod
    def show_button(update: Update, context: CallbackContext):
        text = "Привет! Я помогу тебе узнать прогноз погоды на сегодня!"

        keyboard = [[InlineKeyboardButton("Узнать погоду", callback_data="clicking")]]
        update.message.reply_text(
            text=text, reply_markup=InlineKeyboardMarkup(keyboard)
        )

    @staticmethod
    def response_from_button(update: Update, context: CallbackContext):
        update.callback_query.answer()
        update.callback_query.message.reply_text("Введите название города РФ:")

    @staticmethod
    def give_forecast(update: Update, context: CallbackContext):
        city = update.message.text
        response = request("GET", INTERNAL_API_PATH, params={"city": city})

        if response.status_code == 200:
            update.message.reply_text(convert_json_to_str(response.json()))
        else:
            update.message.reply_text(response.json())

    def handle(self, *args, **kwargs):
        telegram_request = Request(connect_timeout=0.5, read_timeout=1.0)

        bot = Bot(request=telegram_request, token=settings.TELEGRAM_TOKEN)
        self.stdout.write(f"Bot started - {bot.get_me()}")

        updater = Updater(bot=bot, use_context=True)

        updater.dispatcher.add_handler(CommandHandler("start", self.show_button))

        updater.dispatcher.add_handler(
            CallbackQueryHandler(self.response_from_button, pattern="^clicking")
        )

        updater.dispatcher.add_handler(MessageHandler(Filters.text, self.give_forecast))

        updater.start_polling()
        updater.idle()
