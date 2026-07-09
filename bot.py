import telebot
from telebot import types
import re

BOT_TOKEN = '8842420512:AAG5ctJuJTh_XknmFNnB26uJC9p4kIpF5Vw'
bot = telebot.TeleBot(BOT_TOKEN)

# ===== БАЗА ДАННЫХ (Сокращена для примера, но структура полная) =====
ERROR_CODES = {
    'P0420': {'desc': '🔴 P0420 - Катализатор', 'causes': '⚠️ Износ, лямбда-зонд', 'solution': '🔧 Замена, проверка'},
    'P0300': {'desc': '🔴 P0300 - Пропуски зажигания', 'causes': '️ Свечи, катушки', 'solution': '🔧 Замена свечей/катушек'},
    'P0171': {'desc': '🟡 P0171 - Бедная смесь', 'causes': '⚠️ Подсос воздуха, ДМРВ', 'solution': '🔧 Проверка впуска'},
}

CAR_BRANDS = {
    'Chery': {'info': ' Chery\nМодели: Tiggo 7/8, Omoda', 'problems': '• Стук гидрокомпенсаторов\n• Вариатор', 'tips': '💡 Масло каждые 7 тыс. км'},
    'Haval': {'info': '🚗 Haval\nМодели: F7, Jolion, Dargo', 'problems': '• Мультимедиа\n• Подвеска', 'tips': '💡 Обновляйте прошивку'},
    'Geely': {'info': ' Geely\nМодели: Coolray, Atlas, Monjaro', 'problems': '• Турбина\n• Рулевая рейка', 'tips': '💡 Масло 5W-30'},
    'Changan': {'info': ' Changan\nМодели: CS35, UNI-T', 'problems': '• Шум вариатора\n• Электроника', 'tips': '💡 Масло в вариаторе каждые 40 тыс.'},
    'BAIC': {'info': '🚗 BAIC\nМодели: X35, X55', 'problems': '• Шумоизоляция\n• Кондиционер', 'tips': '💡 Доп. шумоизоляция'},
}

# ===== МЕНЮ =====
def get_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add('🔍 Ошибки', '🚗 Марки', ' Запчасти')
    markup.add(' Калькуляторы', '🛒 Б/у Авто', 'ℹ️ О нас')
    return markup

def get_calc_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(' Расчет ТО', '⛽ Расход топлива', '🌨️ Сезонные советы', '️ Назад')
    return markup

# ===== СТАРТ =====
@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.send_message(message.chat.id, "🚗 Добро пожаловать в АвтоЯсно!\nВыберите раздел:", reply_markup=get_main_menu())

@bot.message_handler(func=lambda m: m.text == '️ Назад')
def back(message):
    bot.send_message(message.chat.id, "🚗 Главное меню", reply_markup=get_main_menu())

# ===== РАЗДЕЛЫ =====
@bot.message_handler(func=lambda m: m.text == '🔍 Ошибки')
def search(message):
    bot.send_message(message.chat.id, "🔍 Напишите код ошибки (P0420) или проблему (стук, не заводится).", reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(func=lambda m: m.text == '🚗 Марки')
def brands(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add('Chery', 'Haval', 'Geely', 'Changan', 'BAIC', '⬅️ Назад')
    bot.send_message(message.chat.id, "🚗 Выберите марку:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in CAR_BRANDS)
def show_brand(message):
    info = CAR_BRANDS[message.text]
    bot.send_message(message.chat.id, f"{info['info']}\n\n{info['problems']}\n\n{info['tips']}")

@bot.message_handler(func=lambda m: m.text == '📍 Запчасти')
def parts(message):
    bot.send_message(message.chat.id, "📍 Напишите: Марка + Запчасть + Год (например: Haval, колодки, 2023)", reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(func=lambda m: m.text == '🛒 Б/у Авто')
def used_car(message):
    text = ("🛒 ЧЕК-ЛИСТ ПРОВЕРКИ Б/У КИТАЙЦА\n\n"
            "1️ Кузов: зазоры, окрас (толщиномер)\n"
            "2️⃣ Двигатель: течи, звук, дым\n"
            "3️⃣ Вариатор/АКПП: пинки, масло\n"
            "4️⃣ Электрика: все кнопки, экран\n"
            "5️ История: проверка по VIN (Автокод)\n\n"
            "💡 Совет: всегда берите автоподборщика!")
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda m: m.text == 'ℹ️ О нас')
def about(message):
    text = ("ℹ️ АвтоЯсно — ваш карманный эксперт!\n\n"
            "📞 Связь: @ваш_ник\n"
            " Чат владельцев: @ссылка_на_чат\n"
            "📺 Наш канал: @ссылка_на_канал")
    bot.send_message(message.chat.id, text)

# ===== КАЛЬКУЛЯТОРЫ =====
@bot.message_handler(func=lambda m: m.text == '📅 Калькуляторы')
def calc_menu(message):
    bot.send_message(message.chat.id, "🧮 Выберите калькулятор:", reply_markup=get_calc_menu())

@bot.message_handler(func=lambda m: m.text == '🌨️ Сезонные советы')
def seasonal(message):
    text = ("🌨️ СЕЗОННЫЕ СОВЕТЫ\n\n"
            "❄️ ЗИМА:\n• Проверьте аккумулятор\n• Залейте незамерзайку\n• Смажьте уплотнители\n\n"
            "☀️ ЛЕТО:\n• Проверьте кондиционер\n• Смените резину\n• Проверьте уровень антифриза")
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda m: m.text == ' Расчет ТО')
def calc_to_start(message):
    msg = bot.send_message(message.chat.id, "📅 Напишите ваш текущий пробег (только цифры, например: 85000):")
    bot.register_next_step_handler(msg, calc_to_process)

def calc_to_process(message):
    try:
        mileage = int(message.text)
        if mileage < 0: raise ValueError
        
        recs = []
        if mileage % 10000 == 0 or mileage % 15000 == 0: recs.append("• Замена масла ДВС и фильтров")
        if mileage % 30000 == 0: recs.append("• Замена свечей зажигания")
        if mileage % 40000 == 0: recs.append("• Замена масла в вариаторе/АКПП")
        if mileage % 60000 == 0: recs.append("• Замена тормозной жидкости и антифриза")
        if mileage % 90000 == 0: recs.append("• Замена ремня/цепи ГРМ")
        
        if not recs:
            text = f"📊 Пробег {mileage} км.\nСрочных регламентных работ нет. Следите за уровнем масла!"
        else:
            text = f"📊 Пробег {mileage} км.\n\n🔧 РЕКОМЕНДУЕТСЯ:\n" + "\n".join(recs)
            
        bot.send_message(message.chat.id, text, reply_markup=get_calc_menu())
    except ValueError:
        bot.send_message(message.chat.id, "❌ Ошибка. Напишите только цифры (например: 85000)", reply_markup=get_calc_menu())

@bot.message_handler(func=lambda m: m.text == '⛽ Расход топлива')
def calc_fuel_start(message):
    msg = bot.send_message(message.chat.id, "⛽ Напишите через запятую: Пробег (км), Литры, Цена за литр.\nПример: 500, 40, 55")
    bot.register_next_step_handler(msg, calc_fuel_process)

def calc_fuel_process(message):
    try:
        parts = [x.strip() for x in message.text.split(',')]
        if len(parts) != 3: raise ValueError
        km, liters, price = float(parts[0]), float(parts[1]), float(parts[2])
        
        consumption = (liters / km) * 100
        cost_per_km = (liters * price) / km
        
        text = (f" РЕЗУЛЬТАТ:\n\n"
                f"📉 Реальный расход: {consumption:.1f} л/100км\n"
                f"💰 Стоимость 1 км: {cost_per_km:.2f} руб.\n\n"
                f"💡 Сравните с паспортом!")
        bot.send_message(message.chat.id, text, reply_markup=get_calc_menu())
    except (ValueError, IndexError):
        bot.send_message(message.chat.id, "❌ Ошибка формата. Пример: 500, 40, 55", reply_markup=get_calc_menu())

# ===== ОБРАБОТКА ТЕКСТА (Ошибки и проблемы) =====
@bot.message_handler(func=lambda m: m.text.upper().startswith('P') and len(m.text) == 5)
def check_error(message):
    code = message.text.upper()
    if code in ERROR_CODES:
        e = ERROR_CODES[code]
        bot.send_message(message.chat.id, f"{e['desc']}\n\n{e['causes']}\n\n{e['solution']}")
    else:
        bot.send_message(message.chat.id, f"❓ Код {code} не найден. Опишите словами.")

@bot.message_handler(content_types=['text'])
def text_handler(message):
    text = message.text.lower()
    if 'стук' in text: bot.send_message(message.chat.id, "🔍 Стук: гидрокомпенсаторы, ГРМ, подшипники. Нужна диагностика!")
    elif 'не заводится' in text: bot.send_message(message.chat.id, "🔍 Не заводится: АКБ, стартер, свечи, бензонасос.")
    elif 'check' in text or 'чек' in text: bot.send_message(message.chat.id, "🔍 Check Engine: считайте код сканером OBD2 и напишите мне!")
    else: bot.send_message(message.chat.id, "🤔 Не понял. Выберите пункт из меню 🔍 Ошибки,  Марки или 📅 Калькуляторы.")

if __name__ == '__main__':
    print("🚗 АвтоЯсно запущен...")
    bot.infinity_polling()import telebot
from telebot import types
import re

BOT_TOKEN = '8842420512:AAG5ctJuJTh_XknmFNnB26uJC9p4kIpF5Vw'
bot = telebot.TeleBot(BOT_TOKEN)

# ===== БАЗА ДАННЫХ (Сокращена для примера, но структура полная) =====
ERROR_CODES = {
    'P0420': {'desc': '🔴 P0420 - Катализатор', 'causes': '⚠️ Износ, лямбда-зонд', 'solution': '🔧 Замена, проверка'},
    'P0300': {'desc': '🔴 P0300 - Пропуски зажигания', 'causes': '️ Свечи, катушки', 'solution': '🔧 Замена свечей/катушек'},
    'P0171': {'desc': '🟡 P0171 - Бедная смесь', 'causes': '⚠️ Подсос воздуха, ДМРВ', 'solution': '🔧 Проверка впуска'},
}

CAR_BRANDS = {
    'Chery': {'info': ' Chery\nМодели: Tiggo 7/8, Omoda', 'problems': '• Стук гидрокомпенсаторов\n• Вариатор', 'tips': '💡 Масло каждые 7 тыс. км'},
    'Haval': {'info': '🚗 Haval\nМодели: F7, Jolion, Dargo', 'problems': '• Мультимедиа\n• Подвеска', 'tips': '💡 Обновляйте прошивку'},
    'Geely': {'info': ' Geely\nМодели: Coolray, Atlas, Monjaro', 'problems': '• Турбина\n• Рулевая рейка', 'tips': '💡 Масло 5W-30'},
    'Changan': {'info': ' Changan\nМодели: CS35, UNI-T', 'problems': '• Шум вариатора\n• Электроника', 'tips': '💡 Масло в вариаторе каждые 40 тыс.'},
    'BAIC': {'info': '🚗 BAIC\nМодели: X35, X55', 'problems': '• Шумоизоляция\n• Кондиционер', 'tips': '💡 Доп. шумоизоляция'},
}

# ===== МЕНЮ =====
def get_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add('🔍 Ошибки', '🚗 Марки', ' Запчасти')
    markup.add(' Калькуляторы', '🛒 Б/у Авто', 'ℹ️ О нас')
    return markup

def get_calc_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(' Расчет ТО', '⛽ Расход топлива', '🌨️ Сезонные советы', '️ Назад')
    return markup

# ===== СТАРТ =====
@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.send_message(message.chat.id, "🚗 Добро пожаловать в АвтоЯсно!\nВыберите раздел:", reply_markup=get_main_menu())

@bot.message_handler(func=lambda m: m.text == '️ Назад')
def back(message):
    bot.send_message(message.chat.id, "🚗 Главное меню", reply_markup=get_main_menu())

# ===== РАЗДЕЛЫ =====
@bot.message_handler(func=lambda m: m.text == '🔍 Ошибки')
def search(message):
    bot.send_message(message.chat.id, "🔍 Напишите код ошибки (P0420) или проблему (стук, не заводится).", reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(func=lambda m: m.text == '🚗 Марки')
def brands(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add('Chery', 'Haval', 'Geely', 'Changan', 'BAIC', '⬅️ Назад')
    bot.send_message(message.chat.id, "🚗 Выберите марку:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in CAR_BRANDS)
def show_brand(message):
    info = CAR_BRANDS[message.text]
    bot.send_message(message.chat.id, f"{info['info']}\n\n{info['problems']}\n\n{info['tips']}")

@bot.message_handler(func=lambda m: m.text == '📍 Запчасти')
def parts(message):
    bot.send_message(message.chat.id, "📍 Напишите: Марка + Запчасть + Год (например: Haval, колодки, 2023)", reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(func=lambda m: m.text == '🛒 Б/у Авто')
def used_car(message):
    text = ("🛒 ЧЕК-ЛИСТ ПРОВЕРКИ Б/У КИТАЙЦА\n\n"
            "1️ Кузов: зазоры, окрас (толщиномер)\n"
            "2️⃣ Двигатель: течи, звук, дым\n"
            "3️⃣ Вариатор/АКПП: пинки, масло\n"
            "4️⃣ Электрика: все кнопки, экран\n"
            "5️ История: проверка по VIN (Автокод)\n\n"
            "💡 Совет: всегда берите автоподборщика!")
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda m: m.text == 'ℹ️ О нас')
def about(message):
    text = ("ℹ️ АвтоЯсно — ваш карманный эксперт!\n\n"
            "📞 Связь: @ваш_ник\n"
            " Чат владельцев: @ссылка_на_чат\n"
            "📺 Наш канал: @ссылка_на_канал")
    bot.send_message(message.chat.id, text)

# ===== КАЛЬКУЛЯТОРЫ =====
@bot.message_handler(func=lambda m: m.text == '📅 Калькуляторы')
def calc_menu(message):
    bot.send_message(message.chat.id, "🧮 Выберите калькулятор:", reply_markup=get_calc_menu())

@bot.message_handler(func=lambda m: m.text == '🌨️ Сезонные советы')
def seasonal(message):
    text = ("🌨️ СЕЗОННЫЕ СОВЕТЫ\n\n"
            "❄️ ЗИМА:\n• Проверьте аккумулятор\n• Залейте незамерзайку\n• Смажьте уплотнители\n\n"
            "☀️ ЛЕТО:\n• Проверьте кондиционер\n• Смените резину\n• Проверьте уровень антифриза")
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda m: m.text == ' Расчет ТО')
def calc_to_start(message):
    msg = bot.send_message(message.chat.id, "📅 Напишите ваш текущий пробег (только цифры, например: 85000):")
    bot.register_next_step_handler(msg, calc_to_process)

def calc_to_process(message):
    try:
        mileage = int(message.text)
        if mileage < 0: raise ValueError
        
        recs = []
        if mileage % 10000 == 0 or mileage % 15000 == 0: recs.append("• Замена масла ДВС и фильтров")
        if mileage % 30000 == 0: recs.append("• Замена свечей зажигания")
        if mileage % 40000 == 0: recs.append("• Замена масла в вариаторе/АКПП")
        if mileage % 60000 == 0: recs.append("• Замена тормозной жидкости и антифриза")
        if mileage % 90000 == 0: recs.append("• Замена ремня/цепи ГРМ")
        
        if not recs:
            text = f"📊 Пробег {mileage} км.\nСрочных регламентных работ нет. Следите за уровнем масла!"
        else:
            text = f"📊 Пробег {mileage} км.\n\n🔧 РЕКОМЕНДУЕТСЯ:\n" + "\n".join(recs)
            
        bot.send_message(message.chat.id, text, reply_markup=get_calc_menu())
    except ValueError:
        bot.send_message(message.chat.id, "❌ Ошибка. Напишите только цифры (например: 85000)", reply_markup=get_calc_menu())

@bot.message_handler(func=lambda m: m.text == '⛽ Расход топлива')
def calc_fuel_start(message):
    msg = bot.send_message(message.chat.id, "⛽ Напишите через запятую: Пробег (км), Литры, Цена за литр.\nПример: 500, 40, 55")
    bot.register_next_step_handler(msg, calc_fuel_process)

def calc_fuel_process(message):
    try:
        parts = [x.strip() for x in message.text.split(',')]
        if len(parts) != 3: raise ValueError
        km, liters, price = float(parts[0]), float(parts[1]), float(parts[2])
        
        consumption = (liters / km) * 100
        cost_per_km = (liters * price) / km
        
        text = (f" РЕЗУЛЬТАТ:\n\n"
                f"📉 Реальный расход: {consumption:.1f} л/100км\n"
                f"💰 Стоимость 1 км: {cost_per_km:.2f} руб.\n\n"
                f"💡 Сравните с паспортом!")
        bot.send_message(message.chat.id, text, reply_markup=get_calc_menu())
    except (ValueError, IndexError):
        bot.send_message(message.chat.id, "❌ Ошибка формата. Пример: 500, 40, 55", reply_markup=get_calc_menu())

# ===== ОБРАБОТКА ТЕКСТА (Ошибки и проблемы) =====
@bot.message_handler(func=lambda m: m.text.upper().startswith('P') and len(m.text) == 5)
def check_error(message):
    code = message.text.upper()
    if code in ERROR_CODES:
        e = ERROR_CODES[code]
        bot.send_message(message.chat.id, f"{e['desc']}\n\n{e['causes']}\n\n{e['solution']}")
    else:
        bot.send_message(message.chat.id, f"❓ Код {code} не найден. Опишите словами.")

@bot.message_handler(content_types=['text'])
def text_handler(message):
    text = message.text.lower()
    if 'стук' in text: bot.send_message(message.chat.id, "🔍 Стук: гидрокомпенсаторы, ГРМ, подшипники. Нужна диагностика!")
    elif 'не заводится' in text: bot.send_message(message.chat.id, "🔍 Не заводится: АКБ, стартер, свечи, бензонасос.")
    elif 'check' in text or 'чек' in text: bot.send_message(message.chat.id, "🔍 Check Engine: считайте код сканером OBD2 и напишите мне!")
    else: bot.send_message(message.chat.id, "🤔 Не понял. Выберите пункт из меню 🔍 Ошибки,  Марки или 📅 Калькуляторы.")

if __name__ == '__main__':
    print("🚗 АвтоЯсно запущен...")
    bot.infinity_polling()
