import json
import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from user_state import UserState
from keyboard import teams
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv('BOT_TOKEN')

with open("resources/messages.json", "r", encoding="utf-8") as f:
    messages = json.load(f)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


@dp.message(UserState.finished)
def finish(message: types.Message, state: FSMContext):
    return


@dp.message(Command('start'))
async def send_welcome(message: types.Message, state: FSMContext):
    await state.set_state(UserState.team)
    await message.answer(messages["welcome_1"])
    await message.answer(messages["welcome_2"], reply_markup=teams)


@dp.callback_query(F.data.startswith("team"))
async def set_team(callback: types.CallbackQuery, state: FSMContext):
    team = int(callback.data[-1])
    await state.update_data(team=team)
    await state.set_state(UserState.task1)
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await bot.send_message(callback.message.chat.id, messages[f"task_1_{team}_1"])
    await bot.send_message(callback.message.chat.id, messages[f"task_1_{team}_2"])
    # await bot.send_message(callback.message.chat.id, f"Вы выбрали {team} команду")
    # await bot.delete_message(callback.message.chat.id, callback.message.message_id)


@dp.message(UserState.task1)
async def solve_task1(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if message.text == messages[f"task_1_{data['team']}_answer"]:
        await bot.send_message(message.chat.id, messages[f"task_2_{data['team']}"])
        await bot.send_message(message.chat.id, messages["task_2"])
        await bot.send_photo(message.chat.id,
                             photo=types.FSInputFile(f"resources/images/task2/{data['team']}.jpg"))
        await state.set_state(UserState.task2)
    else:
        await message.answer(messages["task_1_wrong"])


@dp.message(UserState.task2)
async def solve_task2(message: types.Message, state: FSMContext):
    data = await state.get_data()
    media = list()
    media.append(types.InputMediaPhoto(
        type="photo",
        media=types.FSInputFile(f"resources/images/task3/team{data['team']}/1.jpg")))
    media.append(types.InputMediaPhoto(
        type="photo",
        media=types.FSInputFile(f"resources/images/task3/team{data['team']}/2.jpg")))
    media.append(types.InputMediaPhoto(
        type="photo",
        media=types.FSInputFile(f"resources/images/task3/team{data['team']}/3.jpg")))
    if message.text == messages[f"task_2_{data['team']}_answer"]:
        await bot.send_message(message.chat.id, messages[f"task_3_{data['team']}"])
        await bot.send_message(message.chat.id, messages["task_3"])
        await bot.send_media_group(message.chat.id, media=media)
        await state.set_state(UserState.task3)
    else:
        await message.answer(messages["task_3_wrong"])


@dp.message(UserState.task3)
async def solve_task3(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if message.text.lower() == messages[f"task_3_{data['team']}_answer"].lower():
        await bot.send_message(message.chat.id, messages[f"task_4_{data['team']}"])
        await bot.send_message(message.chat.id, messages["task_4"])
        await state.set_state(UserState.finished)
    else:
        await message.answer(messages["task_3_wrong"])


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
