from aiogram.dispatcher.fsm.state import StatesGroup, State


class Auth(StatesGroup):
    full_name = State()
