import telebot
from telebot import types
import random

BOT_TOKEN = '8842420512:AAG5ctJuJTh_XknmFNnB26uJC9p4kIpF5Vw'
bot = telebot.TeleBot(BOT_TOKEN)

# 1. БАЗЫ ДАННЫХ
ERROR_CODES = {
    'P0420': '🔴 P0420 - Катализатор\n⚠️ Причины: износ, лямбда-зонд\n🔧 Самому: проверить лямбда-зонд\n Сервис: замена\n💰 15 000 - 80 000 руб.',
    'P0300': ' P0300 - Пропуски зажигания\n⚠️ Причины: свечи, катушки\n🔧 Самому: заменить свечи\n Сервис: диагностика\n💰 2 000 - 15 000 руб.',
    'P0171': ' P0171 - Бедная смесь\n⚠️ Причины: подсос воздуха\n Самому: проверить шланги\n Сервис: замена ДМРВ\n💰 3 000 - 20 000 руб.',
    'P0172': '🟡 P0172 - Богатая смесь\n⚠️ Причины: забит фильтр\n🔧 Самому: заменить фильтр\n Сервис: диагностика\n💰 2 000 - 15 000 руб.',
    'P0135': ' P0135 - Лямбда-зонд\n⚠️ Причины: обрыв нагревателя\n🔧 Самому: проверить проводку\n🏪 Сервис: замена\n💰 5 000 - 25 000 руб.',
    'P0442': '🟡 P0442 - Утечка EVAP\n⚠️ Причины: крышка бензобака\n🔧 Самому: закрыть крышку\n🏪 Сервис: проверка\n💰 500 - 5 000 руб.'
}

CAR_BRANDS = {
    'Chery': '🚗 CHERY\n📱 Модели: Tiggo 4/7/8, Omoda C5\n️ Проблемы: стук гидрокомпенсаторов, вариатор\n🔧 Масло ДВС: 7-10 тыс. км\n Совет: только оригинальное масло',
    'Haval': '🚗 HAVAL\n📱 Модели: Jolion, F7, Dargo\n⚠️ Проблемы: мультимедиа, подвеска\n🔧 Масло ДВС: 10 тыс. км\n💡 Совет: обновляйте прошивку',
    'Geely': '🚗 GEELY\n Модели: Coolray, Atlas, Monjaro\n⚠️ Проблемы: турбина, рулевая рейка\n🔧 Масло ДВС: 5W-30\n💡 Совет: следите за турбиной',
    'Changan': '🚗 CHANGAN\n📱 Модели: CS35 Plus, UNI-T\n️ Проблемы: шум вариатора, электроника\n🔧 Масло в вариаторе: 40 тыс. км\n💡 Совет: избегайте резких стартов',
    'BAIC': '🚗 BAIC\n📱 Модели: X35, X55\n⚠️ Проблемы: шумоизоляция, кондиционер\n Масло ДВС: 10 тыс. км\n💡 Совет: доп. шумоизоляция'
}

RARE_PROBLEMS = {
    'свист ремня': '🔊 СВИСТ РЕМНЯ\n⚠️ Причины: износ ремня\n🔧 Самому: подтянуть или заменить\n🏪 Сервис: 3 000 - 8 000 руб.',
    'масляные пятна': '️ МАСЛЯНЫЕ ПЯТНА\n⚠️ Причины: прокладки, сальники\n🔧 Самому: проверить уровень масла\n Сервис: замена прокладок',
    'вибрация': '📳 ВИБРАЦИЯ НА СКОРОСТИ\n⚠️ Причины: дисбаланс колес, ШРУСы\n🔧 Самому: балансировка\n Сервис: диагностика ходовой',
    'скрип тормозов': '🔇 СКРИП ТОРМОЗОВ\n⚠️ Причины: износ колодок\n🔧 Самому: заменить колодки\n🏪 Сервис: 3 000 - 15 000 руб.'
}

EMERGENCY_HELP = {
    'перегрев': '🔥 ПЕРЕГРЕВ\n⚠️ НЕМЕДЛЕННО:\n1. Остановитесь!\n2. Выключите двигатель\n3. Откройте капот\n4. Дождитесь остывания\n🏪 Сервис: эвакуатор',
    'не заводится': '🔑 НЕ ЗАВОДИТСЯ\n⚠️ Проверьте:\n1. АКБ (горят фары?)\n2. Стартер (крутит?)\n3. Бензонасос (звук?)\n Самому: прикурить',
    'прокол': '🛞 ПРОКОЛ\n️ Действия:\n1. Аварийка\n2. Знак\n3. Запаска\n🏪 Сервис: шиномонтаж',
    'дтп': '💥 ДТП\n️ НЕМЕДЛЕННО:\n1. Аварийка\n2. Знак\n3. Пострадавшие?\n4. ГИБДД: 102\n5. Фото места'
}

GARAGE_TIPS = [
    '💡 ЛАЙФХАК: Зимой не включайте сразу печку - дайте прогреться 2-3 минуты',
    '💡 ЛАЙФХАК: Проверяйте давление в шинах раз в месяц - экономия до 5%',
    '💡 ЛАЙФХАК: Меняйте масло каждые 7-8 тыс. км вместо 15 тыс.',
    '💡 ЛАЙФХАК: Не тормозите двигателем на вариаторе',
    '💡 ЛАЙФХАК: Держите бак полным зимой - меньше конденсата'
]

GLOSSARY = {
    'вариатор': '🔧 ВАРИАТОР (CVT) - бесступенчатая трансмиссия. Требует частой замены масла.',
    'робот': '🔧 РОБОТ (DCT) - роботизированная коробка с двумя сцеплениями.',
    'дмрв': '🔧 ДМРВ - датчик массового расхода воздуха.',
    'лямбда': '🔧 ЛЯМБДА-ЗОНД - датчик кислорода в выхлопе.',
    'шрус': ' ШРУС - шарнир равных угловых скоростей.',
    'турбина': ' ТУРБИНА - нагнетает воздух в двигатель.'
}

# 2. МЕНЮ
def get_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add('🔍 Ошибки', '🚗 Марки')
    markup.add('📍 Запчасти', ' Калькуляторы')
    markup.add('🛒 Б/у Авто', ' Помощь')
    markup.add('💡 Лайфхаки', '📖 Словарь')
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
    markup.add('💰 Стоимость владения')
    markup.add('🌨️ Сезонные советы')
    markup.add('⬅️ Главное меню')
    return markup

def get_emergency_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add('🔥 Перегрев', '🔑 Не заводится')
    markup.add('🛞 Прокол', '💥 ДТП')
    markup.add('⬅️ Главное меню')
    return markup

# 3. КОМАНДЫ
@bot.message_handler(commands=['start', 'help'])
def start(message):
    text = '🚗 Привет! Я АвтоЯсно - твой друг и помощник!\n\nЯ помогу:\n• Расшифровать ошибки\n• Узнать о проблемах авто\n• Дать советы по ремонту\n• Помочь в экстренной ситуации\n\nВыбери раздел 👇'
    bot.send_message(message.chat.id, text, reply_markup=get_main_menu())

@bot.message_handler(commands=['parts'])
def parts_command(message):
    bot.send_message(message.chat.id, '📍 ПОИСК ЗАПЧАСТЕЙ\n\nНапишите: Марка, Запчасть, Год\nПример: Haval, колодки, 2023', reply_markup=get_main_menu())

@bot.message_handler(commands=['errors'])
def errors_command(message):
    bot.send_message(message.chat.id, '🔍 ПОИСК ОШИБОК\n\nНапишите код ошибки (P0420)\nили опишите проблему:\n• "свист ремня"\n• "масляные пятна"\n• "вибрация"', reply_markup=get_main_menu())

@bot.message_handler(commands=['brands'])
def brands_command(message):
    bot.send_message(message.chat.id, '🚗 Выберите марку:', reply_markup=get_brands_menu())

@bot.message_handler(commands=['calc'])
def calc_command(message):
    bot.send_message(message.chat.id, '🧮 Выберите калькулятор:', reply_markup=get_calc_menu())

@bot.message_handler(commands=['emergency'])
def emergency_command(message):
    bot.send_message(message.chat.id, ' ЭКСТРЕННАЯ ПОМОЩЬ\n\nВыберите ситуацию:', reply_markup=get_emergency_menu())

@bot.message_handler(commands=['tips'])
def tips_command(message):
    tip = random.choice(GARAGE_TIPS)
    bot.send_message(message.chat.id, tip, reply_markup=get_main_menu())

@bot.message_handler(commands=['glossary'])
def glossary_command(message):
    bot.send_message(message.chat.id, '📖 СЛОВАРЬ ТЕРМИНОВ\n\nНапишите термин:\n• вариатор\n• робот\n• дмрв\n• лямбда\n• шрус\n• турбина', reply_markup=get_main_menu())

# 4. ОБРАБОТЧИКИ КНОПОК
@bot.message_handler(func=lambda m: m.text in ['⬅️ Главное меню', 'Главное меню'])
def back(message):
    bot.send_message(message.chat.id, '🚗 Главное меню', reply_markup=get_main_menu())

@bot.message_handler(func=lambda m: m.text in ['🔍 Ошибки', 'Ошибки'])
def search(message):
    text = '🔍 ПОИСК ОШИБОК\n\nНапишите код ошибки (P0420)\nили опишите проблему:\n• "свист ремня"\n• "масляные пятна"\n• "вибрация"\n\nДоступные коды: P0420, P0300, P0171, P0172, P0135, P0442'
    bot.send_message(message.chat.id, text, reply_markup=get_main_menu())

@bot.message_handler(func=lambda m: m.text in ['🚗 Марки', 'Марки'])
def brands(message):
    bot.send_message(message.chat.id, '🚗 Выберите марку:', reply_markup=get_brands_menu())

@bot.message_handler(func=lambda m: m.text in CAR_BRANDS)
def show_brand(message):
    bot.send_message(message.chat.id, CAR_BRANDS[message.text], reply_markup=get_brands_menu())

@bot.message_handler(func=lambda m: m.text in ['📍 Запчасти', 'Запчасти'])
def parts_menu(message):
    text = '📍 ПОИСК ЗАПЧАСТЕЙ\n\nНапишите: Марка, Запчасть, Год\nПример: Haval, колодки, 2023\n\n💡 Совет: используйте оригинальные запчасти!'
    bot.send_message(message.chat.id, text, reply_markup=get_main_menu())

@bot.message_handler(func=lambda m: m.text in ['📅 Калькуляторы', 'Калькуляторы'])
def calc_menu(message):
    bot.send_message(message.chat.id, '🧮 Выберите калькулятор:', reply_markup=get_calc_menu())

@bot.message_handler(func=lambda m: m.text in [' Б/у Авто', 'Б/у Авто'])
def used_car(message):
    text = '🛒 ЧЕК-ЛИСТ ПРОВЕРКИ\n\n📋 Документы: ПТС, СТС, VIN\n🚗 Кузов: зазоры, окраска\n⚙️ Двигатель: течи, звук\n🔧 Трансмиссия: плавность\n⚡ Электрика: все кнопки\n🛞 Подвеска: стуки\n\n💡 Совет: берите автоподборщика!\n💰 3 000 - 10 000 руб.'
    bot.send_message(message.chat.id, text, reply_markup=get_main_menu())

@bot.message_handler(func=lambda m: m.text in ['🆘 Помощь', 'Помощь'])
def emergency(message):
    text = '🆘 ЭКСТРЕННАЯ ПОМОЩЬ\n\nВыберите ситуацию:'
    bot.send_message(message.chat.id, text, reply_markup=get_emergency_menu())

@bot.message_handler(func=lambda m: m.text in ['💡 Лайфхаки', 'Лайфхаки'])
def tips(message):
    tip = random.choice(GARAGE_TIPS)
    bot.send_message(message.chat.id, tip + '\n\n💡 Нажмите еще раз для нового совета!', reply_markup=get_main_menu())

@bot.message_handler(func=lambda m: m.text in ['📖 Словарь', 'Словарь'])
def glossary(message):
    text = '📖 СЛОВАРЬ ТЕРМИНОВ\n\nНапишите термин:\n• вариатор\n• робот\n• дмрв\n• лямбда\n• шрус\n• турбина'
    bot.send_message(message.chat.id, text, reply_markup=get_main_menu())

# 5. КАЛЬКУЛЯТОРЫ (С ЗАЩИТОЙ ОТ ОШИБОК)
@bot.message_handler(func=lambda m: m.text in ['📊 Расчет ТО', 'Расчет ТО'])
def calc_to_start(message):
    msg = bot.send_message(message.chat.id, '📊 Напишите пробег (цифры): 85000')
    bot.register_next_step_handler(msg, calc_to_process)

def calc_to_process(message):
    try:
        if not message.text.strip():
            raise ValueError('Пустой ввод')
        mileage = int(message.text.strip())
        if mileage < 0:
            raise ValueError('Отрицательное число')
        recs = []
        if mileage % 10000 == 0: recs.append('✅ Замена масла ДВС')
        if mileage % 30000 == 0: recs.append('✅ Замена свечей')
        if mileage % 40000 == 0: recs.append('✅ Масло в вариаторе')
        if mileage % 60000 == 0: recs.append('✅ Замена антифриза')
        if mileage % 90000 == 0: recs.append('⚠️ Замена ремня ГРМ')
        
        if not recs:
            text = f'📊 Пробег {mileage} км.\nСрочных работ нет.'
        else:
            text = f'📊 Пробег {mileage} км.\n\n🔧 РЕКОМЕНДУЕТСЯ:\n' + '\n'.join(recs)
        bot.send_message(message.chat.id, text, reply_markup=get_main_menu())
    except:
        bot.send_message(message.chat.id, ' Ошибка. Напишите только цифры: 85000', reply_markup=get_main_menu())

@bot.message_handler(func=lambda m: m.text in [' Расход топлива', 'Расход топлива'])
def calc_fuel_start(message):
    msg = bot.send_message(message.chat.id, '⛽ Напишите: Пробег, Литры, Цена\nПример: 500, 40, 55')
    bot.register_next_step_handler(msg, calc_fuel_process)

def calc_fuel_process(message):
    try:
        parts = [x.strip() for x in message.text.split(',')]
        if len(parts) != 3:
            raise ValueError('Неверное количество значений')
        km = float(parts[0])
        liters = float(parts[1])
        price = float(parts[2])
        if km == 0 or liters <= 0 or price <= 0:
            raise ValueError('Некорректные значения')
        consumption = (liters / km) * 100
        cost = (liters * price) / km
        text = f'⛽ Расход: {consumption:.1f} л/100 км\n💰 1 км: {cost:.2f} руб'
        bot.send_message(message.chat.id, text, reply_markup=get_main_menu())
    except:
        bot.send_message(message.chat.id, '❌ Ошибка. Пример: 500, 40, 55', reply_markup=get_main_menu())

@bot.message_handler(func=lambda m: m.text in ['💰 Стоимость владения', 'Стоимость владения'])
def calc_ownership_start(message):
    msg = bot.send_message(message.chat.id, '💰 Напишите через запятую:\nЦена авто, Пробег в год, Цена топлива\nПример: 1500000, 20000, 55')
    bot.register_next_step_handler(msg, calc_ownership_process)

def calc_ownership_process(message):
    try:
        parts = [x.strip() for x in message.text.split(',')]
        if len(parts) != 3:
            raise ValueError('Неверное количество значений')
        price = float(parts[0])
        mileage = float(parts[1])
        fuel_price = float(parts[2])
        if mileage == 0 or price <= 0 or fuel_price <= 0:
            raise ValueError('Некорректные значения')
        
        fuel_cost = (mileage / 100) * 10 * fuel_price
        insurance = price * 0.03
        maintenance = mileage * 5
        depreciation = price * 0.15
        
        total_year = fuel_cost + insurance + maintenance + depreciation
        total_month = total_year / 12
        
        text = f'💰 СТОИМОСТЬ ВЛАДЕНИЯ\n\n📊 Исходные данные:\n• Цена авто: {price:,.0f} руб\n• Пробег в год: {mileage:,.0f} км\n• Цена топлива: {fuel_price} руб/л\n\n🔢 РАСЧЕТ В ГОД:\n• Топливо: {fuel_cost:,.0f} руб\n• Страховка: {insurance:,.0f} руб\n• ТО и ремонт: {maintenance:,.0f} руб\n• Потеря стоимости: {depreciation:,.0f} руб\n\n💵 ИТОГО В ГОД: {total_year:,.0f} руб\n💵 В МЕСЯЦ: {total_month:,.0f} руб'
        bot.send_message(message.chat.id, text, reply_markup=get_main_menu())
    except:
        bot.send_message(message.chat.id, '❌ Ошибка. Пример: 1500000, 20000, 55', reply_markup=get_main_menu())

@bot.message_handler(func=lambda m: m.text in ['🌨️ Сезонные советы', 'Сезонные советы'])
def seasonal(message):
    text = '🌨️ СЕЗОННЫЕ СОВЕТЫ\n\n❄️ ЗИМА:\n• Проверьте аккумулятор\n• Залейте незамерзайку\n• Смените резину\n• Смажьте уплотнители\n\n☀️ ЛЕТО:\n• Проверьте кондиционер\n• Смените резину\n• Проверьте антифриз\n• Очистите радиатор'
    bot.send_message(message.chat.id, text, reply_markup=get_main_menu())

@bot.message_handler(func=lambda m: m.text in ['🔥 Перегрев', 'Перегрев'])
def emergency_overheat(message):
    bot.send_message(message.chat.id, EMERGENCY_HELP['перегрев'], reply_markup=get_emergency_menu())

@bot.message_handler(func=lambda m: m.text in ['🔑 Не заводится', 'Не заводится'])
def emergency_no_start(message):
    bot.send_message(message.chat.id, EMERGENCY_HELP['не заводится'], reply_markup=get_emergency_menu())

@bot.message_handler(func=lambda m: m.text in ['🛞 Прокол', 'Прокол'])
def emergency_tire(message):
    bot.send_message(message.chat.id, EMERGENCY_HELP['прокол'], reply_markup=get_emergency_menu())

@bot.message_handler(func=lambda m: m.text in ['💥 ДТП', 'ДТП'])
def emergency_accident(message):
    bot.send_message(message.chat.id, EMERGENCY_HELP['дтп'], reply_markup=get_emergency_menu())

# 6. ОБРАБОТЧИК КОДОВ ОШИБОК (С ЗАЩИТОЙ ОТ ПРОБЕЛОВ)
@bot.message_handler(func=lambda m: m.text.strip().upper().startswith('P') and len(m.text.strip()) == 5)
def check_error(message):
    code = message.text.strip().upper()
    if code in ERROR_CODES:
        bot.send_message(message.chat.id, ERROR_CODES[code], reply_markup=get_main_menu())
    else:
        bot.send_message(message.chat.id, f' Код {code} не найден\n\nДоступные: P0420, P0300, P0171, P0172, P0135, P0442', reply_markup=get_main_menu())

# 7. УМНЫЙ ТЕКСТОВЫЙ ПОИСК (ИСПРАВЛЕННЫЙ)
@bot.message_handler(content_types=['text'])
def text_handler(message):
    text = message.text.lower().strip()
    
    if not text:
        bot.send_message(message.chat.id, '🤔 Пустой запрос. Попробуйте еще раз!', reply_markup=get_main_menu())
        return
    
    # Марки авто (проверяем в первую очередь)
    if 'chery' in text or 'чери' in text:
        bot.send_message(message.chat.id, CAR_BRANDS['Chery'], reply_markup=get_brands_menu())
    elif 'haval' in text or 'хавал' in text:
        bot.send_message(message.chat.id, CAR_BRANDS['Haval'], reply_markup=get_brands_menu())
    elif 'geely' in text or 'джели' in text:
        bot.send_message(message.chat.id, CAR_BRANDS['Geely'], reply_markup=get_brands_menu())
    elif 'changan' in text or 'cangan' in text or 'чанган' in text:
        bot.send_message(message.chat.id, CAR_BRANDS['Changan'], reply_markup=get_brands_menu())
    elif 'baic' in text or 'баик' in text:
        bot.send_message(message.chat.id, CAR_BRANDS['BAIC'], reply_markup=get_brands_menu())
    
    # Редкие проблемы
    elif 'свист ремня' in text:
        bot.send_message(message.chat.id, RARE_PROBLEMS['свист ремня'], reply_markup=get_main_menu())
    elif 'масляные пятна' in text or 'масло под' in text:
        bot.send_message(message.chat.id, RARE_PROBLEMS['масляные пятна'], reply_markup=get_main_menu())
    elif 'вибрация' in text or 'вибрирует' in text:
        bot.send_message(message.chat.id, RARE_PROBLEMS['вибрация'], reply_markup=get_main_menu())
    elif 'скрип тормозов' in text or 'тормоза скрипят' in text:
        bot.send_message(message.chat.id, RARE_PROBLEMS['скрип тормозов'], reply_markup=get_main_menu())
    
    # Словарь терминов (ЧАСТИЧНОЕ СОВПАДЕНИЕ)
    elif any(term in text for term in GLOSSARY):
        for term, definition in GLOSSARY.items():
            if term in text:
                bot.send_message(message.chat.id, definition, reply_markup=get_main_menu())
                return
    
    # Запчасти
    elif 'запча' in text or 'parts' in text or 'детал' in text:
        bot.send_message(message.chat.id, '📍 Напишите: Марка, Запчасть, Год\nПример: Haval, колодки, 2023', reply_markup=get_main_menu())
    
    # Общие проблемы
    elif 'стук' in text or 'стучит' in text:
        bot.send_message(message.chat.id, '🔍 СТУК\n\nВозможные причины:\n• Гидрокомпенсаторы\n• ГРМ\n• Подшипники\n• Подвеска\n\n🏪 Сервис: диагностика', reply_markup=get_main_menu())
    elif 'не заводится' in text or 'не запускается' in text:
        bot.send_message(message.chat.id, '🔑 НЕ ЗАВОДИТСЯ\n\nПроверьте:\n• АКБ\n• Стартер\n• Свечи\n• Бензонасос\n\n💡 Нажмите "🆘 Помощь"', reply_markup=get_main_menu())
    elif 'check' in text or 'чек' in text or 'ошибка' in text:
        bot.send_message(message.chat.id, '🔍 CHECK ENGINE\n\nНапишите код ошибки (P0420)\nили опишите симптомы', reply_markup=get_main_menu())
    else:
        bot.send_message(message.chat.id, '🤔 Не понял\n\nПопробуйте:\n• Код ошибки (P0420)\n• Марка (Chery, Haval)\n• Проблема (свист ремня, вибрация)\n• Термин (вариатор, робот)\n• Нажмите "💡 Лайфхаки"', reply_markup=get_main_menu())

if __name__ == '__main__':
    print('🚗 АвтоЯсно запущен')
    bot.infinity_polling()
