from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton  # pip install aiogram
from aiogram import Dispatcher, Bot, executor, types
import json
from selenium_to_txt import json_open
import asyncio
from DB import pandas
from DB import privyazka
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

API_TOKEN = "5662776987:AAFNQiftIFBgayordIizZxMeRDcZWCmq7Ao"

# инициализация ботика...
bot = Bot(token=API_TOKEN)
dispatcher = Dispatcher(bot, storage=MemoryStorage())

# Создание клавиатуры
btn_berta = KeyboardButton("♈ Берта")
btn_blyzenko = KeyboardButton('♿ Близенько')
btn_other = KeyboardButton("🔷 TEST")



btn_info = KeyboardButton('ℹ️ Інформація')
btn_main = KeyboardButton('🟡 Головне меню')
btn_back = KeyboardButton('🟡 Назад')

btn_berta_popovn = KeyboardButton('☮ Поповнення')
btn_berta_vidpravka = KeyboardButton('☯ Відправка')
btn_berta_perep = KeyboardButton('✡ Перепаковка')

btn_blyzenko_peremisch_in = KeyboardButton('ℹ️ Переміщення IN*')
btn_blyzenko_popovn = KeyboardButton('ℹ️ Поповнення')
btn_blyzenko_perep = KeyboardButton('ℹ️ Перепаковка')
btn_blyzenko_peremisch_st = KeyboardButton('ℹ️ Переміщення ST*')
btn_blyzenko_vidpravka = KeyboardButton('ℹ️ Відправка')




main_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_berta, btn_blyzenko, btn_other)
other_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_info, btn_main)
berta_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_berta_perep, btn_berta_popovn, btn_berta_vidpravka, btn_back)
blyzenko_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_blyzenko_popovn, btn_blyzenko_perep, btn_blyzenko_peremisch_in, btn_blyzenko_peremisch_st, btn_blyzenko_vidpravka, btn_back)

class Answer(StatesGroup):
    user_send_text = State()
    admin_answer = State()

@dispatcher.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(message.from_user.id, f"👋 Привіт, {message.from_user.first_name}!", reply_markup=main_menu)
chat_id=420995060

# @dispatcher.message_handler()
# async def messages(message: types.Message):
#     if message.text == "♈ Берта":
#         await bot.send_message(message.from_user.id, '🟡 Відкриваю меню Берта...', reply_markup=berta_menu)
    # elif message.text == '♿ Близенько':
    #     await bot.send_message(message.from_user.id, '🟡 Відкриваю меню Близенько...', reply_markup=blyzenko_menu)
    # elif message.text == '☮ Поповнення':
    #     await message.answer(json_open("popovn_berta.json"))
    # elif message.text == '☯ Відправка':
    #     await message.answer(json_open("vidpravka_berta.json"))
    # elif message.text == '✡ Перепаковка':
    #     await message.answer(json_open("perepakovka_berta.json"))
    # elif message.text == '🟡 Назад':
    #     await bot.send_message(message.from_user.id, '🟡 Відкриваю меню...', reply_markup=main_menu)
    # elif message.text == 'ℹ️ Переміщення IN*':
    #     await message.answer(json_open("peremischenya_na_in_blyzenko.json"))
    # elif message.text == 'ℹ️ Переміщення ST*':
    #     await message.answer(json_open("peremischenya_na_st_blyzenko.json"))
    # elif message.text == 'ℹ️ Перепаковка':
    #     await message.answer(json_open("perepakovka_blyzenko.json"))
    # elif message.text == 'ℹ️ Поповнення':
    #     await message.answer(json_open("popovn_blyzenko.json"))
    # elif message.text == 'ℹ️ Відправка':
    #     await message.answer(json_open("vidpravka_blyzenko.json"))
    # # elif message.text == '🔷 TEST':
    # #     test_mes = pandas()
    # #     await message.answer(message.text)
    #
    # else:
    #     await bot.send_message(message.from_user.id, f'😐 Ботик вас не зрозумів... :(')
@dispatcher.message_handler(text='🔷 TEST')
async def handler(message: types.Message):
    await message.answer('🙏 Пожалуйста, укажите ID заказа <b>(укажите только цифры)</b>:')
    print(Answer.user_send_text.set())
    await Answer.user_send_text.set()


# @dispatcher.message_handler(content_types=['text'])
# async def cmd_keyboard(message: types.Message):
#     if message.text == '🔷 TEST':
#         await message.answer('🙏 Пожалуйста, укажите ID заказа <b>(укажите только цифры)</b>:')
#         await Answer.user_send_text.set()

    # else:
    #     await bot.send_message(message.from_user.id, f'😐 Ботик вас не зрозумів... :(')

@dispatcher.message_handler(state=Answer.user_send_text)
async def state_sended(message: types.Message, state: FSMContext):
    # db.set_user_text(message.from_user.id, int(message.text))
    # await message.answer(message.text)
    text = "111"
    await bot.send_message(message.from_user.id, text)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    executor.start_polling(dispatcher)
