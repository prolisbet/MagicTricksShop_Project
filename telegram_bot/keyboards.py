from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def start_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Покупатель')],
            [KeyboardButton(text='Админ')]
        ],
        resize_keyboard=True
    )


def user_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Мои заказы')],
            [KeyboardButton(text='Назад')]
        ],
        resize_keyboard=True
    )


def admin_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Все заказы')],
            [KeyboardButton(text='Аналитика')],
            [KeyboardButton(text='Отчеты')],
            [KeyboardButton(text='Назад')],
        ],
        resize_keyboard=True
    )


def site_button():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Наш сайт", url='https://magictricks.shop')]
        ],
        resize_keyboard=True
    )
