import logging
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext

from config import TOKEN
from keyboards import start_keyboard, user_keyboard, admin_keyboard, site_button
from database import (get_user_by_username, get_admin_by_credentials, get_orders_by_user,
                      get_order_details, get_all_orders, get_analytics_data, get_reports_data)


logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot, storage=storage)


class UserState(StatesGroup):
    verify = State()
    verified = State()


class AdminState(StatesGroup):
    username = State()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Выберите вашу роль:", reply_markup=start_keyboard())


@dp.message(Command('info'))
async def info(message: Message):
    caption = "Magic Tricks Shop"
    await message.answer(f"Добро пожаловать в {caption}!\n"
                         f"Погрузитесь в захватывающий мир иллюзий и волшебства вместе с нами!\n"
                         f"{caption} — это ваше уникальное пространство, где каждый, от начинающего "
                         f"до профессионального иллюзиониста, найдет всё необходимое для создания "
                         f"незабываемых магических шоу. Следите за нашими обновлениями, акциями "
                         f"и специальными предложениями. \nПодписывайтесь на нашу рассылку и соцсети, "
                         f"чтобы всегда быть в курсе новинок и событий мира магии."
                         f"\n{caption} — откройте для себя мир волшебства уже сегодня!",
                         reply_markup=site_button())


@dp.message(Command('help'))
async def help(message: Message):
    await message.answer(
        'Этот бот умеет выполнять команды: \n /start \n /help \n /info'
    )


@dp.message(F.text == 'Покупатель')
async def handle_user(message: Message, state: FSMContext):
    await message.answer("Введите ваше имя пользователя:")
    await state.set_state(UserState.verify)


@dp.message(F.text == 'Админ')
async def handle_admin(message: Message):
    await message.answer("Введите ваши учетные данные в формате username:password:")


@dp.message(UserState.verify)
async def verify_user(message: Message, state: FSMContext):
    user = get_user_by_username(message.text)
    if user:
        await state.update_data(username=user[1], user_id=user[0])  # Сохраняем данные пользователя в состоянии
        await state.set_state(UserState.verified)  # Устанавливаем состояние как "верифицированный"
        await message.answer(f"Добро пожаловать, {user[1]}!", reply_markup=user_keyboard())
    else:
        await message.answer("Пользователь не найден. Попробуйте снова.")


@dp.message(lambda message: ':' in message.text)
async def verify_admin(message: Message, state: FSMContext):
    username, password = message.text.split(':', 1)
    admin = get_admin_by_credentials(username, password)
    if admin:
        await state.update_data(username=admin[4])  # Сохраняем имя администратора в состояние
        await message.answer(f"Добро пожаловать, {admin[4]}!", reply_markup=admin_keyboard())
    else:
        await message.answer("Неверные учетные данные. Попробуйте снова.")


@dp.message(F.text == 'Мои заказы', StateFilter(UserState.verified))
async def show_user_orders(message: Message, state: FSMContext):
    data = await state.get_data()
    user_id = data.get("user_id")
    logging.info(f"User ID from state: {user_id}")
    if user_id:
        orders = get_orders_by_user(user_id)
        if orders:
            for order in orders:
                order_details = get_order_details(order[0])
                details = "\n".join([f"{item[1]} x{item[0]} - {item[2]} руб." for item in order_details])
                await message.answer(f"Заказ #{order[0]}:\n{details}\nСтатус: {order[1]}")
        else:
            await message.answer("У вас нет заказов.")
    else:
        await message.answer("Пользователь не найден. Попробуйте снова.")


@dp.message(F.text == 'Все заказы')
async def show_all_orders(message: Message):
    orders = get_all_orders()
    if orders:
        for order in orders:
            order_details = get_order_details(order[0])
            details = "\n".join([f"{item[1]} x{item[0]} - {item[2]} руб." for item in order_details])
            await message.answer(f"Заказ #{order[0]}:\n{details}\nСтатус: {order[1]}")
    else:
        await message.answer("Заказов не найдено.")

@dp.message(F.text == 'Аналитика')
async def show_analytics(message: Message):
    total_sales, total_profit = get_analytics_data()
    summary_message = (
        f"Общее количество завершенных заказов: {total_sales}\n"
        f"Общая прибыль: {total_profit} руб."
    )
    await message.answer(summary_message)


@dp.message(F.text == 'Отчеты')
async def show_reports(message: Message):
    reports = get_reports_data()
    if reports:
        for report in reports:
            report_message = (
                f"Дата: {report[0]}\n"
                f"Данные продаж: {report[1]}\n"
                f"Прибыль: {report[2]} руб.\n"
                f"Расходы: {report[3]} руб."
            )
            await message.answer(report_message)
    else:
        await message.answer("Отчетов не найдено.")


@dp.message(F.text == 'Назад')
async def go_back(message: Message, state: FSMContext):
    await state.clear()  # Завершаем состояние
    await start(message)


@dp.message()
async def echo(message: Message):
    if message.text:
        await message.send_copy(chat_id=message.chat.id)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
