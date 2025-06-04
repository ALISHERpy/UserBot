from aiogram.filters.state import StatesGroup, State


class Test(StatesGroup):
    Q1 = State()
    Q2 = State()


class AdminState(StatesGroup):
    are_you_sure = State()
    ask_ad_content = State()

class LoginState(StatesGroup):
    waiting_number = State()
    waiting_confirm_code = State()
    code_input = State()
    two_factor_password = State()

class ClientState(StatesGroup):
    waiting_delete_confirm = State()
