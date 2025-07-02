from aiogram.fsm.state import State, StatesGroup


class InstAccAdd(StatesGroup):
    username = State()
    password = State()
