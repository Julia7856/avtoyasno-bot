
import telebot
from telebot import types

BOT_TOKEN = '8842420512:AAG5ctJuJTh_XknmFNnB26uJC9p4kIpF5Vw'
bot = telebot.TeleBot(BOT_TOKEN)

ERROR_CODES = {
    'P0420': '🔴 P0420 - Катализатор\n⚠️ Причины: износ, лямбда-зонд\n🔧 Решение: замена',
    'P0300': '🔴 P0300 - Пропуски зажигания\n⚠️ Причины: свечи, катушки\n🔧 Решение: замена свечей',
    'P0171': '🟡 P0171 - Бедная смесь\n⚠️ Причины: подсос воздуха, ДМРВ\n🔧 Решение: проверка впуска',
    'P0172': '🟡 P0172 - Богатая смесь\n⚠️ Причины: фильтр, ДМРВ\n🔧 Решение: замена фильтра',
    'P0135': '🟡 P0135 - Лямбда-зонд\n⚠️ Причины: обрыв цепи\n🔧 Решение: замена датчика',
    'P0442': '🟡 P0442 - Утечка EVAP\n⚠️ Причины: крышка бензобака\n🔧 Решение: проверить крышку'
}

CAR_BRANDS = {
    'Chery': '🚗 Chery\nМодели: Tiggo 7/8, Omoda\n⚠️ Стук гидрокомпенсаторов, вариатор\n Масло каждые 7 тыс. км',
    'Haval': '🚗 Haval\nМодели: F7, Jolion, Dargo\n⚠️ Мультимедиа, подвеска\n💡 Обновляйте прошивку',
    'Geely': '🚗 Geely\nМодели: Coolray, Atlas, Monjaro\n⚠️ Турбина, рулевая рейка\n💡 Масло 5W-30',
    'Changan': '🚗 Changan\nМодели: CS35, UNI-T\n⚠️ Шум вариатора, электроника\n💡 Масло в вариаторе каждые 40 тыс.',
    'BAIC': '🚗 BAIC\nМодели: X35, X55\n⚠️ Шумоизоляция, кондиционер\n💡 Доп. шумоизоляция'
}

def get_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add('🔍 Ошибки', '🚗 Марки')
    markup.add('📍 Запчасти', '📅 Калькуляторы')
    markup.add(' Б/у Авто', 'ℹ️ О нас')
    return markup

def get_brands_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add('Chery', 'Haval', 'Geely')
    markup.add('Changan', 'BAIC')
    markup.add('⬅️ Главное меню')
    return markup

def get_calc_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(' Расчет ТО', '⛽ Расход топлива')
    markup.add('🌨️ Сезонные советы')
    markup.add('️ Главное меню')
    return markup

@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.send_message(message.chat.id, '🚗 Добро пожаловать в АвтоЯсно!\nВыберите раздел:', reply_markup=get_main_menu())

@bot.message_handler(func=lambda m: m.text == '⬅️ Главное меню')
def back(message):
    bot.send_message(message.chat.id, '🚗 Главное меню', reply_markup=get_main_menu())

@bot.message_handler(func=lambda m: m.text == '🔍 Ошибки')
def search(message):
    bot.send_message(message.chat.id, '🔍 Напишите код ошибки (P0420) или проблему (стук, не заводится).\n\nИли выберите из меню:', reply_markup=get_main_menu())

@bot.message_handler(func=lambda m: m.text == '🚗 Марки')
def brands(message):
    bot.send_message(message.chat.id, '🚗 Выберите марку:', reply_markup=get_brands_menu())

@bot.message_handler(func=lambda m: m.text in CAR_BRANDS)
def show_brand(message):
    bot.send_message(message.chat.id, CAR_BRANDS[message.text] + '\n\n Чтобы выбрать другую марку, нажмите " Марки" или "⬅️ Главное меню"', reply_markup=get_brands_menu())

@bot.message_handler(func=lambda m: m.text == '📍 Запчасти')
def parts(message):
    bot.send_message(message.chat.id, '📍 Напишите: Марка + Запчасть + Год\nПример: Haval, колодки, 2023', reply_markup=get_main_menu())

@bot.message_handler(func=lambda m: m.text == '🛒 Б/у Авто')
def used_car(message):
    text = '🛒 ЧЕК-ЛИСТ ПРОВЕРКИ Б/У КИТАЙЦА\n\n1️⃣ Кузов: зазоры, окрас (толщиномер)\n2️⃣ Двигатель: течи, звук, дым\n3️ Вариатор/АКПП: пинки, масло\n4️⃣ Электрика: все кнопки, экран\n5️⃣ История: проверка по VIN (Автокод)\n\n💡 Совет: всегда берите автоподборщика!'
    bot.send_message(message.chat.id, text, reply_markup=get_main_menu())

@bot.message_handler(func=lambda m: m.text == 'ℹ️ О нас')
def about(message):
    text = '️ АвтоЯсно — ваш карманный эксперт!\n\n📞 Связь: @ваш_ник\n💬 Чат владельцев: @ссылка_на_чат\n Наш канал: @ссылка_на_канал'
    bot.send_message(message.chat.id, text, reply_markup=get_main_menu())

@bot.message_handler(func=lambda m: m.text == ' Калькуляторы')
def calc_menu(message):
    bot.send_message(message.chat.id, ' Выберите калькулятор:', reply_markup=get_calc_menu())

@bot.message_handler(func=lambda m: m.text == '🌨️ Сезонные советы')
def seasonal(message):
    text = '🌨️ СЕЗОННЫЕ СОВЕТЫ\n\n❄️ ЗИМА:\n• Проверьте аккумулятор\n• Залейте незамерзайку\n• Смажьте уплотнители\n\n☀️ ЛЕТО:\n• Проверьте кондиционер\n• Смените резину\n• Проверьте антифриз'
    bot.send_message(message.chat.id, text, reply_markup=get_main_menu())

@bot.message_handler(func=lambda m: m.text == '📊 Расчет ТО')
def calc_to_start(message):
    msg = bot.send_message(message.chat.id, '📊 Напишите ваш пробег (только цифры, например: 85000):')
    bot.register_next_step_handler(msg, calc_to_process)

def calc_to_process(message):
    try:
        mileage = int(message.text)
        if mileage < 0:
            raise ValueError
        recs = []
        if mileage % 10000 == 0 or mileage % 15000 == 0:
            recs.append('• Замена масла ДВС и фильтров')
        if mileage % 30000 == 0:
            recs.append('• Замена свечей зажигания')
        if mileage % 40000 == 0:
            recs.append('• Замена масла в вариаторе/АКПП')
        if mileage % 60000 == 0:
            recs.append('• Замена тормозной жидкости и антифриза')
        if mileage % 90000 == 0:
            recs.append('• Замена ремня/цепи ГРМ')
        if not recs:
            text = f'📊 Пробег {mileage} км.\nСрочных работ нет. Следите за маслом!'
        else:
            text = f' Пробег {mileage} км.\n\n РЕКОМЕНДУЕТСЯ:\n' + '\n'.join(recs)
        bot.send_message(message.chat.id, text, reply_markup=get_main_menu())
    except ValueError:
        bot.send_message(message.chat.id, '❌ Ошибка. Напишите только цифры (например: 85000)', reply_markup=get_main_menu())

@bot.message_handler(func=lambda m: m.text == '⛽ Расход топлива')
def calc_fuel_start(message):
    msg = bot.send_message(message.chat.id, '⛽ Напишите через запятую: Пробег, Литры, Цена за литр.\nПример: 500, 40, 55')
    bot.register_next_step_handler(msg, calc_fuel_process)

def calc_fuel_process(message):
    try:
        parts = [x.strip() for x in message.text.split(',')]
        if len(parts) != 3:
            raise ValueError
        km, liters, price = float(parts[0]), float(parts[1]), float(parts[2])
        consumption = (liters / km) * 100
        cost_per_km = (liters * price) / km
        text = f'📉 РЕЗУЛЬТАТ:\n\nРеальный расход: {consumption:.1f} л/100км\n Стоимость 1 км: {cost_per_km:.2f} руб.'
        bot.send_message(message.chat.id, text, reply_markup=get_main_menu())
    except (ValueError, IndexError):
        bot.send_message(message.chat.id, '❌ Ошибка формата. Пример: 500, 40, 55', reply_markup=get_main_menu())

@bot.message_handler(func=lambda m: m.text.upper().startswith('P') and len(m.text) == 5)
def check_error(message):
    code = message.text.upper()
    if code in ERROR_CODES:
        bot.send_message(message.chat.id, ERROR_CODES[code] + '\n\n💡 Чтобы проверить другую ошибку, напишите её код или выберите из меню:', reply_markup=get_main_menu())
    else:
        bot.send_message(message.chat.id, f'❓ Код {code} не найден. Доступные коды: {", ".join(ERROR_CODES.keys())}', reply_markup=get_main_menu())

@bot.message_handler(content_types=['text'])
def text_handler(message):
    text = message.text.lower()
    
    # Проверяем, не марка ли это
    for brand in CAR_BRANDS:
        if brand.lower() in text:
            bot.send_message(message.chat.id, CAR_BRANDS[brand] + '\n\n💡 Чтобы выбрать другую марку, нажмите "🚗 Марки"', reply_markup=get_brands_menu())
            return
    
    # Проверяем проблемы
    if 'стук' in text or 'стучит' in text:
        bot.send_message(message.chat.id, '🔍 Стук: гидрокомпенсаторы, ГРМ, подшипники. Нужна диагностика!', reply_markup=get_main_menu())
    elif 'не заводится' in text or 'не запускается' in text:
        bot.send_message(message.chat.id, '🔍 Не заводится: АКБ, стартер, свечи, бензонасос.', reply_markup=get_main_menu())
    elif 'check' in text or 'чек' in text or 'ошибка' in text:
        bot.send_message(message.chat.id, '🔍 Check Engine: считайте код сканером OBD2 и напишите мне (например: P0420)', reply_markup=get_main_menu())
    else:
        bot.send_message(message.chat.id, '🤔 Не понял запрос.\n\nПопробуйте:\n• Код ошибки (P0420)\n• Название марки (Chery, Haval)\n• Опишите проблему (стук, не заводится)\n\nИли выберите из меню:', reply_markup=get_main_menu())

if __name__ == '__main__':
    print('🚗 АвтоЯсно запущен...')
    bot.infinity_polling()
