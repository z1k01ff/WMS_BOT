from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from DB import privyazka_DB, soderzimoe_DB, vidpravka_DB, \
    transport_DB, transport_perep_DB, transport_peremish_st, \
    transport_peremish_in, transport_vidpravka_bl, soderzimoe_full_DB
import json
bot = Bot(token="5662776987:AAFNQiftIFBgayordIizZxMeRDcZWCmq7Ao")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# Создание клавиатуры
btn_berta = KeyboardButton("♈ Берта")
btn_blyzenko = KeyboardButton('♿ Близенько')
btn_other = KeyboardButton("🔷 TEST")



btn_info = KeyboardButton('ℹ️ Інформація')
btn_main = KeyboardButton('🟡 Головне меню')
btn_back = KeyboardButton('🟡 Назад')

btn_berta_popovn = KeyboardButton('☮ Поповнення')
btn_berta_vidpravka = KeyboardButton('☯ Відправка')
# btn_berta_perep = KeyboardButton('✡ Перепаковка')
btn_berta_privyazka = KeyboardButton("Прив'язка")
btn_berta_vmist = KeyboardButton("Вміст складу")





btn_blyzenko_peremisch = KeyboardButton('ℹ️ Переміщення')
# btn_blyzenko_popovn = KeyboardButton('ℹ️ Поповнення')
# btn_blyzenko_perep = KeyboardButton('ℹ️ Перепаковка')
# btn_blyzenko_peremisch_st = KeyboardButton('ℹ️ Переміщення ST*')
btn_blyzenko_vidpravka = KeyboardButton('ℹ️ Відправка')

btn_soder_nisiy = KeyboardButton('Носій')
btn_artikul = KeyboardButton('Номер артикула')
btn_nazva_artikulf = KeyboardButton('Назва артикула')
btn_soder_test = KeyboardButton('Тест')




main_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_berta, btn_blyzenko, btn_other)
other_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_info, btn_main)
berta_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_berta_popovn, btn_berta_vidpravka, btn_back, btn_berta_privyazka, btn_berta_vmist)
blyzenko_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_blyzenko_peremisch, btn_blyzenko_vidpravka, btn_back)
vmist_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_soder_nisiy, btn_artikul, btn_nazva_artikulf, btn_soder_test, btn_back)
# vmist_menu.add(btn_back)

def load_whitelist(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
        return data.get("admin_user_ids", [])




@dp.message_handler(commands=['start'])
async def whitelist(message: types.Message):
    whitelistt = load_whitelist('whitelist.json')
    if message.from_user.id not in whitelistt:
        await message.answer("Ви не в WHITELIST")
    else:
        await bot.send_message(message.from_user.id, f"👋 Привіт, {message.from_user.first_name}!",
                               reply_markup=main_menu)


# Кнопки МЕНЮ
@dp.message_handler(lambda message: message.text == "♈ Берта")
async def berta_menu_btn(message: types.Message):
    await bot.send_message(message.from_user.id, '🟡 Відкриваю меню Берта...', reply_markup=berta_menu)

@dp.message_handler(lambda message: message.text == "♿ Близенько")
async def berta_menu_btn(message: types.Message):
    await bot.send_message(message.from_user.id, '🟡 Відкриваю меню Близенько...', reply_markup=blyzenko_menu)

@dp.message_handler(lambda message: message.text == "🟡 Назад")
async def back_menu_btn(message: types.Message):
    await bot.send_message(message.from_user.id, '🟡 Відкриваю меню...', reply_markup=main_menu)

# БЕРТА
@dp.message_handler(lambda message: message.text == "☮ Поповнення")
async def back_menu_btn(message: types.Message):
    await bot.send_message(message.from_user.id, 'Завантажую інформацію... ⏳')

    transport_DB('RP')
    transport_perep_DB("CP")

    with open("cache/PNG/transport.png", 'rb') as photo:
        await bot.send_photo(message.chat.id, photo)
    await bot.send_message(message.from_user.id, 'Поповнення ⤴️')

    with open("cache/PNG/transport_perep.png", 'rb') as photo:
        await bot.send_photo(message.chat.id, photo)
    await bot.send_message(message.from_user.id, 'Переупаковки ⤴️')


@dp.message_handler(lambda message: message.text == "☯ Відправка")
async def popovnenya(message: types.Message):
    await bot.send_message(message.from_user.id, 'Завантажую інформацію... ⏳')
    vidpravka_DB()

    with open("cache/PNG/vidpravka_pack.png", 'rb') as photo:
        await bot.send_photo(message.chat.id, photo)
    await bot.send_message(message.from_user.id, 'Ящична зона ⤴️')
    with open("cache/PNG/vidpravka_piec.png", 'rb') as photo:
        await bot.send_photo(message.chat.id, photo)
    await bot.send_message(message.from_user.id, 'Штучна зона ⤴️')

# Привязка функція
@dp.message_handler(lambda message: message.text == "Прив'язка")
async def privyazka(message: types.Message):
    await message.reply("Введіть артикул:")

    # Зберігаємо ID користувача та текст повідомлення в контексті
    await bot.get_chat_member(message.chat.id, message.from_user.id)
    context = dp.current_state(user=message.from_user.id)
    await context.set_state('privyazka_state')


@dp.message_handler(state='privyazka_state')
async def privyazka_state(message: types.Message, state: State):
    # Викликаємо функцію для обробки поповнення з текстом
    print(type(message.text))
    privyazka_DB(message.text)

    # Скидаємо стан
    await state.finish()

    with open("cache/PNG/privyazka.png", 'rb') as photo:
        await bot.send_photo(message.chat.id, photo)

# Залишок на складі функція
@dp.message_handler(lambda message: message.text == "Залишок")
async def handle_topup(message: types.Message):
    await message.reply("Введіть артикул товару:")

    # Зберігаємо ID користувача та текст повідомлення в контексті
    await bot.get_chat_member(message.chat.id, message.from_user.id)
    context = dp.current_state(user=message.from_user.id)
    await context.set_state('waiting_for_text_sklad')


@dp.message_handler(state='waiting_for_text_sklad')
async def process_topup_text(message: types.Message, state: State):
    # Отримуємо текст з повідомлення
    soderzimoe_DB(message.text)

    # Скидаємо стан
    await state.finish()

    with open("cache/PNG/soderzimoe.png", 'rb') as photo:
        await bot.send_photo(message.chat.id, photo)

# БЛИЗЕНЬКО

@dp.message_handler(lambda message: message.text == "ℹ️ Переміщення")
async def back_menu_btn(message: types.Message):
    await bot.send_message(message.from_user.id, 'Завантажую інформацію... ⏳')
    transport_peremish_st()
    transport_peremish_in()

    with open("cache/PNG/transport_perem_IN.png", 'rb') as photo:
        await bot.send_photo(message.chat.id, photo)
    await bot.send_message(message.from_user.id, 'Переміщення IN-* ⤴️')

    with open("cache/PNG/transport_perem_ST.png", 'rb') as photo:
        await bot.send_photo(message.chat.id, photo)
    await bot.send_message(message.from_user.id, 'Переміщення ST-* ⤴️')

@dp.message_handler(lambda message: message.text == "ℹ️ Відправка")
async def back_menu_btn(message: types.Message):
    await bot.send_message(message.from_user.id, 'Завантажую інформацію... ⏳')
    transport_vidpravka_bl()

    with open("cache/PNG/transport_vidpravka_bl.png", 'rb') as photo:
        await bot.send_photo(message.chat.id, photo)
    await bot.send_message(message.from_user.id, 'Відправка ⤴️')

@dp.message_handler(lambda message: message.text == "Вміст складу")
async def berta_menu_btn(message: types.Message):
    await bot.send_message(message.from_user.id, '🟡 Відкриваю меню Вміст...', reply_markup=vmist_menu)

@dp.message_handler(lambda message: message.text == "Тест")
async def search_by_nosiy_test(message: types.Message):
    await message.reply("шукаємо по носію тест:")

    # Зберігаємо ID користувача та текст повідомлення в контексті
    await bot.get_chat_member(message.chat.id, message.from_user.id)
    context = dp.current_state(user=message.from_user.id)
    await context.set_state('vmist_state_test')

@dp.message_handler(state='vmist_state_test')
async def state_search_by_nosiy_test(message: types.Message, state: State):

    df = soderzimoe_full_DB(message.text, "LOADUNIT_ID")

    vmist_menu_test = ReplyKeyboardMarkup(resize_keyboard=True)

    for PRODUCT_NAME in df["PRODUCT_NAME"]:
        vmist_menu_test.add(KeyboardButton(PRODUCT_NAME))

    await bot.send_message(message.from_user.id, '🟡 Відкриваю меню TEST...', reply_markup=vmist_menu_test)
    # Скидаємо стан
    await state.finish()

    # Зберігаємо ID користувача та текст повідомлення в контексті
    await bot.get_chat_member(message.chat.id, message.from_user.id)
    context = dp.current_state(user=message.from_user.id)
    await context.set_state('vmist_state_test_no2')

@dp.message_handler(state='vmist_state_test_no2')
async def state_search_by_nosiy_test(message: types.Message, state: State):
    # await bot.send_message(message.from_user.id, 'ON STATE')
    # Отримуємо текст з повідомлення
    soderzimoe_full_DB(message.text, "PRODUCT_NAME")

    # Скидаємо стан
    await state.finish()

    with open("cache/PNG/soderzimoe_full.png", 'rb') as photo:
        await bot.send_photo(message.chat.id, photo)
    await bot.send_message(message.from_user.id, '🟡 Відкриваю меню Вміст...', reply_markup=vmist_menu)

@dp.message_handler(lambda message: message.text == "Носій")
async def handle_topup(message: types.Message):
    await message.reply("шукаємо по носію:")

    # Зберігаємо ID користувача та текст повідомлення в контексті
    await bot.get_chat_member(message.chat.id, message.from_user.id)
    context = dp.current_state(user=message.from_user.id)
    await context.set_state('vmist_state')

@dp.message_handler(state='vmist_state')
async def process_topup_text(message: types.Message, state: State):
    # Отримуємо текст з повідомлення
    soderzimoe_full_DB(message.text, "LOADUNIT_ID")

    # Скидаємо стан
    await state.finish()

    with open("cache/PNG/soderzimoe_full.png", 'rb') as photo:
        await bot.send_photo(message.chat.id, photo)




if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp)





