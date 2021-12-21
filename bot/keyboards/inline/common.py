from typing import Any

from aiogram.dispatcher.filters.callback_data import CallbackData


class OptionCallback(CallbackData, prefix="option"):
    option: str


class PayloadCallback(CallbackData, prefix="payload"):
    option: str
    payload: Any
