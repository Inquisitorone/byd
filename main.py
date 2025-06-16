
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

API_TOKEN = "YOUR_API_TOKEN"

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class Form(StatesGroup):
    language = State()
    city = State()
    order_number = State()
    manager_name = State()
    manager_phone = State()
    vin = State()
    multimedia = State()
    car_model = State()
    install_lang = State()
    confirm = State()

language_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("Русский", "Українська", "English")
city_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(
    "Днепр", "Киев", "Кропивницкий", "Львов", "Одесса", "Ужгород", "Харьков", "Винница"
)
multimedia_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("Dlink 3", "Dlink 4", "Dlink 5")
install_lang_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("UA", "RUS")

models = {
    "Dlink 3": ["Qin Plus DM-i, EV", "Song Pro", "Yuan Plus", "Song Max", "Destroyer 05", "Dolphins", "Tang Dm-i"],
    "Dlink 4": ["Han 22", "Tang 22", "Song Plus", "Song Champ", "Frigate 07", "Seal EV"],
    "Dlink 5": ["Song Plus", "Song L DMI", "Seal", "Sealion 07"]
}

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await Form.language.set()
    await message.answer("Выберите язык / Оберіть мову / Choose language:", reply_markup=language_kb)

@dp.message_handler(state=Form.language)
async def set_language(message: types.Message, state: FSMContext):
    await state.update_data(language=message.text)
    await Form.city.set()
    await message.answer("Выберите город:", reply_markup=city_kb)

@dp.message_handler(state=Form.city)
async def set_city(message: types.Message, state: FSMContext):
    await state.update_data(city=message.text)
    await Form.order_number.set()
    await message.answer("Введите номер заказ-наряда:")

@dp.message_handler(state=Form.order_number)
async def set_order_number(message: types.Message, state: FSMContext):
    await state.update_data(order_number=message.text)
    await Form.manager_name.set()
    await message.answer("Введите ФИО менеджера:")

@dp.message_handler(state=Form.manager_name)
async def set_manager_name(message: types.Message, state: FSMContext):
    await state.update_data(manager_name=message.text)
    await Form.manager_phone.set()
    await message.answer("Введите номер телефона менеджера:")

@dp.message_handler(state=Form.manager_phone)
async def set_manager_phone(message: types.Message, state: FSMContext):
    await state.update_data(manager_phone=message.text)
    await Form.vin.set()
    await message.answer("Введите VIN автомобиля:")

@dp.message_handler(state=Form.vin)
async def set_vin(message: types.Message, state: FSMContext):
    await state.update_data(vin=message.text)
    await Form.multimedia.set()
    await message.answer("Выберите мультимедию:", reply_markup=multimedia_kb)

@dp.message_handler(state=Form.multimedia)
async def set_multimedia(message: types.Message, state: FSMContext):
    await state.update_data(multimedia=message.text)
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for model in models.get(message.text, []):
        kb.add(model)
    await Form.car_model.set()
    await message.answer("Выберите модель авто:", reply_markup=kb)

@dp.message_handler(state=Form.car_model)
async def set_car_model(message: types.Message, state: FSMContext):
    await state.update_data(car_model=message.text)
    await Form.install_lang.set()
    await message.answer("Выберите язык установки мультимедии:", reply_markup=install_lang_kb)

@dp.message_handler(state=Form.install_lang)
async def set_install_lang(message: types.Message, state: FSMContext):
    await state.update_data(install_lang=message.text)
    data = await state.get_data()
    summary = (
        f"Проверьте введенные данные:

"
        f"Язык интерфейса: {data['language']}
"
        f"Город: {data['city']}
"
        f"Заказ-наряд: {data['order_number']}
"
        f"Менеджер: {data['manager_name']}
"
        f"Телефон: {data['manager_phone']}
"
        f"VIN: {data['vin']}
"
        f"Мультимедиа: {data['multimedia']}
"
        f"Модель: {data['car_model']}
"
        f"Язык установки: {data['install_lang']}"
    )
    kb = ReplyKeyboardMarkup(resize_keyboard=True).add("✅ Подтвердить", "🔁 Отменить")
    await Form.confirm.set()
    await message.answer(summary, reply_markup=kb)

@dp.message_handler(state=Form.confirm)
async def confirm_data(message: types.Message, state: FSMContext):
    if message.text == "✅ Подтвердить":
        await message.answer("Данные сохранены. Спасибо!")
        await state.finish()
    else:
        await message.answer("Операция отменена. Запустите /start для начала.")
        await state.finish()

if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
