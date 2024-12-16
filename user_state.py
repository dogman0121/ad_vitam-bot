from aiogram.fsm.state import State, StatesGroup


class UserState(StatesGroup):
    team = State()
    task1 = State()
    task2 = State()
    task3 = State()
    finished = State()