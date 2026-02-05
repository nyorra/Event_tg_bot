from aiogram.fsm.state import State, StatesGroup


class RegistrationStates(StatesGroup):
    waiting_for_username = State()
    waiting_for_phone = State()


class ScreenshotStates(StatesGroup):
    waiting_for_screenshot = State()


class CoffeeStates(StatesGroup):
    waiting_for_code = State()


class AdminCodeStates(StatesGroup):
    waiting_for_delete_code = State()
    waiting_for_code_amount = State()


class AdminBanStates(StatesGroup):
    waiting_for_user_id = State()
    waiting_for_ban_date = State()


class AdminUnbanStates(StatesGroup):
    waiting_for_user_id = State()


class AdminAddPointsStates(StatesGroup):
    waiting_for_user_id = State()
    waiting_for_amount = State()


class AdminRemovePointsStates(StatesGroup):
    waiting_for_user_id = State()
    waiting_for_amount = State()


class AdminSetPointsStates(StatesGroup):
    waiting_for_amount_set = State()
    waiting_for_user_id = State()
    waiting_for_amount = State()


class AdminManagerPointsStates(StatesGroup):
    waiting_for_user_id = State()
