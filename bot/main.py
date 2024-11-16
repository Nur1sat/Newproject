from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
import asyncio

from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.database import save_user, get_user, get_all_users

TOKEN = "7968153954:AAFDw9rDiDrbGH0CM8RsM6aOi-H33O-jOxM"
bot_properties = DefaultBotProperties(parse_mode="HTML")
bot = Bot(token=TOKEN, default=bot_properties)

dp = Dispatcher(storage=MemoryStorage())


class MyStateGroup(StatesGroup):
    state1 = State()
    state2 = State()
    state3 = State()


@dp.message(Command("start"))
async def start(message: Message):
    kb = InlineKeyboardBuilder()
    kb.add(types.InlineKeyboardButton(callback_data="yes", text="yes"))
    kb.add(types.InlineKeyboardButton(callback_data="no", text="no"))
    await bot.send_message(message.from_user.id, "Hello!\nAre you student in <b>JIHC</b>?", reply_markup=kb.as_markup())


@dp.callback_query(F.data == "yes")
async def yes(message: Message, state: FSMContext):
    await bot.send_message(message.from_user.id,"Welcome! Let's start the conversation. What's your name?")
    await state.set_state(MyStateGroup.state1)


@dp.message(MyStateGroup.state1)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(f"Nice to meet you, {message.text}! How old are you?")
    await state.set_state(MyStateGroup.state2)


@dp.message(MyStateGroup.state2)
async def get_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("Got it! Where are you from?")
    await state.set_state(MyStateGroup.state3)


@dp.message(MyStateGroup.state3)
async def get_location(message: Message, state: FSMContext):
    user_data = await state.get_data()
    name = user_data['name']
    age = user_data['age']
    location = message.text
    await message.answer(f"Thanks, {name}! You're {age} years old and from {location}.")
    await save_user(message.from_user.id, name, age, location)
    await state.clear()

@dp.message(Command("users"))
async def users(message: Message):
    user = await get_all_users()
    user_data = user
    await bot.send_message(
        message.from_user.id,
        f"All data:"
        f"{user_data}"

    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
