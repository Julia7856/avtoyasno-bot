import telebot
from telebot import types
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = '8842420512:AAG5ctJuJTh_XknmFNnB26uJC9p4kIpF5Vw'
bot = telebot.TeleBot(BOT_TOKEN)

# База ошибок двигателя
ERROR_CODES = {
    'P0420': '🔴 P0420 - Низкая эффективность катализатора\n️ Причины: износ катализатора, лямбда-зонд\n🔧 Решение: замена катализатора\n💰 Стоимость: 15 000 - 80 000 руб.',
    'P0300': '🔴 P0300 - Пропуски зажигания\n⚠️ Причины: свечи, катушки, форсунки\n🔧 Решение: замена свечей, диагностика\n💰 Стоимость: 2 000 - 15 000 руб.',
    'P0171': '🟡 P0171 - Бедная смесь\n⚠️ Причины: подсос воздуха, ДМРВ, фильтр\n Решение: проверка впуска\n💰 Стоимость: 3 000 - 20 000 руб.',
    'P0172': '🟡 P0172 - Богатая смесь\n⚠️ Причины: забит фильтр, ДМРВ\n Решение: замена фильтра\n💰 Стоимость: 2 000 - 15 000 руб.',
    'P0135': '🟡 P0135 - Лямбда-зонд (нагреватель)\n⚠️ Причины: обрыв цепи\n Решение: замена датчика\n💰 Стоимость: 5 000 - 25 000 руб.',
    'P0442': '🟡 P0442 - Утечка EVAP\n⚠️ Причины: крышка бензобака\n🔧 Решение: проверить крышку\n💰 Стоимость: 500 - 5 000 руб.',
    'P0401': '🟡 P0401 - Недостаточный поток EGR\n⚠️ Причины: забит клапан EGR\n🔧 Решение: чистка/замена EGR\n💰 Стоимость: 5 000 - 20 000 руб.',
    'P0421': '🟡 P0421 - Катализатор (Банк 1)\n⚠️ Причины: износ катализатора\n🔧 Решение: замена\n💰 Стоимость: 15 000 - 60 000 руб.'
}

# Полная база китайских марок
CAR_BRANDS = {
    'Chery': '🚗 CHERY\n📱 Модели: Tiggo 4/7/8 Pro, Omoda C5, Arrizo 8, Exeed\n⚠️ Типичные проблемы:\n• Стук гидрокомпенсаторов на холодную\n• Проблемы с вариатором после 100 тыс. км\n• Быстрый износ тормозных колодок\n• Глюки мультимедиа\n🔧 Регламент ТО:\n• Масло ДВС: каждые 7-10 тыс. км\n• Масло вариатора: каждые 40-60 тыс. км\n• Свечи: каждые 30 тыс. км\n💡 Совет: используйте только оригинальное масло',
    'Haval': '🚗 HAVAL\n📱 Модели: Jolion, F7, F7x, Dargo, H9, M6\n⚠️ Типичные проблемы:\n• Глюки мультимедийной системы\n• Шум подвески на неровностях\n• Проблемы с электроникой\n• Износ тормозных дисков\n Регламент ТО:\n• Масло ДВС: каждые 10 тыс. км\n• Масло АКПП: каждые 60 тыс. км\n• Тормозная жидкость: каждые 2 года\n💡 Совет: регулярно обновляйте прошивку у дилера',
    'Geely': ' GEELY\n📱 Модели: Coolray, Atlas Pro, Monjaro, Tugella, Emgrand\n⚠️ Типичные проблемы:\n• Проблемы с турбиной после 80 тыс. км\n• Износ рулевой рейки\n• Шум в салоне на скорости\n• Проблемы с роботом DCT\n🔧 Регламент ТО:\n• Масло ДВС: 5W-30, каждые 10 тыс. км\n• Масло АКПП: каждые 60 тыс. км\n• Ремень ГРМ: каждые 90 тыс. км\n Совет: следите за уровнем масла в турбине',
    'Changan': '🚗 CHANGAN\n📱 Модели: CS35 Plus, CS55, UNI-T, UNI-K, UNI-V\n⚠️ Типичные проблемы:\n• Шум вариатора при разгоне\n• Проблемы с электроникой\n• Быстрый износ сайлентблоков\n• Слабая шумоизоляция\n🔧 Регламент ТО:\n• Масло в вариаторе: каждые 40 тыс. км\n• Масло ДВС: каждые 10 тыс. км\n• Свечи: каждые 30 тыс. км\n💡 Совет: избегайте резких стартов',
    'BAIC': '🚗 BAIC\n📱 Модели: X35, X55, BJ40, U5 Plus\n️ Типичные проблемы:\n• Слабая шумоизоляция\n• Проблемы с кондиционером\n• Быстрый износ сцепления (МКПП)\n• Качество сборки\n🔧 Регламент ТО:\n• Масло ДВС: каждые 10 тыс. км\n• Масло МКПП: каждые 60 тыс. км\n• Тормозные колодки: проверка каждые 20 тыс. км\n Совет: рекомендуется доп. шумоизоляция',
    'Great Wall': '🚗 GREAT WALL (Wingle, Poer)\n Модели: Wingle 5/7, Poer, Tank 300/500\n⚠️ Типичные проблемы:\n• Проблемы с полным приводом\n• Износ подвески на бездорожье\n• Коррозия кузова\n• Проблемы с дизелем\n Регламент ТО:\n• Масло ДВС: каждые 10 тыс. км\n• Масло раздатки: каждые 40 тыс. км\n• Проверка полного привода: каждые 20 тыс. км\n💡 Совет: чаще мойте днище зимой',
    'Jetour': '🚗 JETOUR\n📱 Модели: X70, X90, Dashing, T2\n⚠️ Типичные проблемы:\n• Проблемы с роботом DCT\n• Глюки электроники\n• Шум вариатора\n• Износ подвески\n🔧 Регламент ТО:\n• Масло ДВС: каждые 10 тыс. км\n• Масло DCT: каждые 60 тыс. км\n• Свечи: каждые 30 тыс. км\n💡 Совет: не перегревайте робот в пробках',
    'Exeed': '🚗 EXEED (премиум Chery)\n📱 Модели: TXL, VX, LX, RX\n⚠️ Типичные проблемы:\n• Проблемы с пневмоподвеской (VX)\n• Глюки мультимедиа\n• Износ турбины\n• Проблемы с АКПП\n🔧 Регламент ТО:\n• Масло ДВС: каждые 10 тыс. км\n• Масло АКПП: каждые 60 тыс. км\n• Пневмоподвеска: диагностика каждые 30 тыс. км\n💡 Совет: только оригинальные запчасти',
    'Tank': '🚗 TANK (внедорожники)\n📱 Модели: Tank 300, Tank 500\n⚠️ Типичные проблемы:\n• Проблемы с полным приводом\n• Износ подвески\n• Проблемы с дизелем 2.4\n• Коррозия\n🔧 Регламент ТО:\n• Масло ДВС: каждые 10 тыс. км\n• Масло раздатки и мостов: каждые 40 тыс. км\n• Проверка блокировок: каждые 20 тыс. км\n💡 Совет: регулярная мойка днища',
    'Omoda': ' OMODA (суббренд Chery)\n📱 Модели: Omoda C5, S5\n⚠️ Типичные проблемы:\n• Проблемы с вариатором\n• Глюки мультимедиа\n• Износ тормозных колодок\n• Шум в салоне\n🔧 Регламент ТО:\n• Масло ДВС: каждые 7-10 тыс. км\n• Масло вариатора: каждые 40-60 тыс. км\n• Свечи: каждые 30 тыс. км\n💡 Совет: избегайте агрессивной езды'
}

# Меню
def get_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add('🔍 Ошибки', '🚗 Марки')
    markup.add('📍 Запчасти', '📅 Калькуляторы')
    markup.add('🛒 Б/у Авто', 'ℹ️ О нас')
    return markup

def get_brands_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add('Chery', 'Haval', 'Geely')
    markup.add('Changan', 'BAIC', 'Great Wall')
    markup.add('Jetour', 'Exeed', 'Tank')
    markup.add('Omoda')
    markup.add('⬅️ Главное меню')
    return markup

def get_calc_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add('📊 Расчет ТО', '⛽ Расход топлива')
    markup.add('🌨️ Сезонные советы')
    markup.add('⬅️ Главное меню')
    return markup

# Обработчики
@bot.message_handler(commands=['start', 'help'])
def start(message):
    logger.info(f'Пользователь {message.chat.id} запустил бота')
    text = '🚗 Добро пожаловать в АвтоЯсно!\n\nВаш помощник для владельцев китайских авто.\n\nЯ помогу:\n• Расшифровать ошибки двигателя\n• Узнать о проблемах вашей марки\n• Рассчитать стоимость обслуживания\n• Проверить б/у авто перед покупкой\n\nВыберите раздел:'
    bot.send_message(message.chat.id, text, reply_markup=get_main_menu())

@bot.message_handler(func=lambda m: m.text == '️ Главное меню')
def back(message):
    bot.send_message(message.chat.id, '🚗 Главное меню', reply_markup=get_main_menu())

@bot.message_handler(func=lambda m: m.text in [' Ошибки', 'Ошибки'])
def search(message):
    text = '🔍 ПОИСК ОШИБОК ДВИГАТЕЛЯ\n\nНапишите код ошибки (например: P0420)\nили опишите проблему словами:\n• "стук"\n• "не заводится"\n• "check engine"\n\nДоступные коды: P0420, P0300, P0171, P0172, P0135, P0442, P0401, P0421'
    bot.send_message(message.chat.id, text, reply_markup=get_main_menu())

@bot.message_handler(func=lambda m: m.text in ['🚗 Марки', 'Марки'])
def brands(message):
    bot.send_message(message.chat.id, ' ВЫБЕРИТЕ МАРКУ:', reply_markup=get_brands_menu())

@bot.message_handler(func=lambda m: m.text in CAR_BRANDS)
def show_brand(message):
    bot.send_message(message.chat.id, CAR_BRANDS[message.text], reply_markup=get_brands_menu())

@bot.message_handler(func=lambda m: m.text in ['📍 Запчасти', 'Запчасти'])
def parts(message):
    text = '📍 ПОИСК ЗАПЧАСТЕЙ\n\nНапишите: Марка, Запчасть, Год\nПримеры:\n• Haval, тормозные колодки, 2023\n• Chery, воздушный фильтр, 2022\n• Geely, свечи зажигания, 2024'
    bot.send_message(message.chat.id, text, reply_markup=get_main_menu())

@bot.message_handler(func=lambda m: m.text in ['🛒 Б/у Авто', 'Б/у Авто'])
def used_car(message):
    text = '🛒 ЧЕК-ЛИСТ ПРОВЕРКИ Б/У КИТАЙЦА\n\n📋 ДОКУМЕНТЫ:\n• ПТС, СТС, страховка\n• Проверка по VIN (Автокод)\n\n🚗 КУЗОВ:\n• Зазоры, окраска (толщиномер)\n• Сварные швы, коррозия\n\n⚙️ ДВИГАТЕЛЬ:\n• Течи масла\n• Звук работы, дым\n\n🔧 ТРАНСМИССИЯ:\n• Плавность переключений\n• Течи из коробки\n\n💡 Совет: берите автоподборщика!\n💰 Стоимость проверки: 3 000 - 10 000 руб.'
    bot.send_message(message.chat.id, text, reply_markup=get_main_menu())

@bot.message_handler(func=lambda m: m.text in ['ℹ️ О нас', 'О нас'])
def about(message):
    text = 'ℹ️ АВТОЯСНО - ВАШ ПОМОЩНИК\n\nМы создали бота для владельцев китайских авто:\n• Быстро расшифровывать ошибки\n• Знать о типичных проблемах\n• Планировать обслуживание\n• Проверять авто перед покупкой\n\n📞 СВЯЗЬ:\n• Telegram: @avtoyasno_support\n• Чат: @avtoyasno_chat\n• Канал: @avtoyasno_channel\n\n💡 Бот бесплатен и постоянно обновляется!'
    bot.send_message(message.chat.id, text, reply_markup=get_main_menu())

@bot.message_handler(func=lambda m: m.text in ['📅 Калькуляторы', 'Калькуляторы'])
def calc_menu(message):
    bot.send_message(message.chat.id, '🧮 Выберите калькулятор:', reply_markup=get_calc_menu())

@bot.message_handler(func=lambda m: m.text in ['🌨️ Сезонные советы', 'Сезонные советы'])
def seasonal(message):
    text = '🌨️ СЕЗОННЫЕ СОВЕТЫ\n\n❄️ ЗИМА:\n• Проверьте аккумулятор\n• Залейте незамерзайку (-20°C или -30°C)\n• Смените резину на зимнюю\n• Проверьте антифриз\n• Смажьте уплотнители силиконом\n• Проверьте печку\n\n☀️ ЛЕТО:\n• Проверьте кондиционер\n• Смените резину на летнюю\n• Проверьте антифриз\n• Очистите радиатор\n• Обновите салонный фильтр'
    bot.send_message(message.chat.id, text, reply_markup=get_main_menu())

@bot.message_handler(func=lambda m: m.text in ['📊 Расчет ТО', 'Расчет ТО'])
def calc_to_start(message):
    msg = bot.send_message(message.chat.id, '📊 Напишите ваш пробег (только цифры, например: 85000):')
    bot.register_next_step_handler(msg, calc_to_process)

def calc_to_process(message):
    try:
        mileage = int(message.text)
        if mileage < 0:
            raise ValueError
        recs = []
        if mileage % 10000 == 0:
            recs.append('✅ Замена масла ДВС и фильтра')
        if mileage % 15000 == 0:
            recs.append('✅ Замена воздушного и салонного фильтров')
        if mileage % 30000 == 0:
            recs.append('✅ Замена свечей зажигания')
            recs.append('✅ Проверка тормозной системы')
        if mileage % 40000 == 0:
            recs.append('✅ Замена масла в вариаторе/АКПП')
            recs.append('✅ Замена тормозной жидкости')
        if mileage % 60000 == 0:
            recs.append('✅ Замена антифриза')
            recs.append('✅ Проверка ремня/цепи ГРМ')
        if mileage % 90000 == 0:
            recs.append('⚠️ Замена ремня ГРМ (критично!)')
        if not recs:
            text = f' Пробег {mileage} км.\nСрочных работ нет. Следите за маслом!'
        else:
            text = f'📊 Пробег {mileage} км.\n\n🔧 РЕКОМЕНДУЕТСЯ:\n' + '\n'.join(recs)
        bot.send_message(message.chat.id, text, reply_markup=get_main_menu())
    except ValueError:
        bot.send_message(message.chat.id, '❌ Ошибка. Напишите только цифры (например: 85000)', reply_markup=get_main_menu())

@bot.message_handler(func=lambda m: m.text in ['⛽ Расход топлива', 'Расход топлива'])
def calc_fuel_start(message):
    msg = bot.send_message(message.chat.id, '⛽ Напишите через запятую: Пробег, Литры, Цена за литр.\nПример: 500, 40, 55')
    bot.register_next_step_handler(msg, calc_fuel_process)

def calc_fuel_process(message):
    try:
        parts = [x.strip() for x in message.text.split(',')]
        if len(parts) != 3:
            raise ValueError
        km = float(parts[0])
        liters = float(parts[1])
        price = float(parts[2])
        consumption = (liters / km) * 100
        cost_per_km = (liters * price) / km
        text = f'📉 РЕЗУЛЬТАТ:\n\n📊 Пройдено: {km} км\n⛽ Израсходовано: {liters} л\n💰 Цена: {price} руб/л\n\n🔢 Расход: {consumption:.1f} л/100 км\n💰 1 км: {cost_per_km:.2f} руб\n💰 100 км: {consumption * price:.2f} руб\n💰 1000 км: {cost_per_km * 1000:.2f} руб\n\n Средний расход китайских авто: 8-12 л/100 км'
        bot.send_message(message.chat.id, text, reply_markup=get_main_menu())
    except (ValueError, IndexError):
        bot.send_message(message.chat.id, ' Ошибка формата. Пример: 500, 40, 55', reply_markup=get_main_menu())

@bot.message_handler(func=lambda m: m.text.upper().startswith('P') and len(m.text) == 5)
def check_error(message):
    code = message.text.upper()
    if code in ERROR_CODES:
        bot.send_message(message.chat.id, ERROR_CODES[code] + '\n\n💡 Рекомендация: обратитесь в сервис для точной диагностики', reply_markup=get_main_menu())
    else:
        bot.send_message(message.chat.id, f'❓ Код {code} не найден. Доступные: P0420, P0300, P0171, P0172, P0135, P0442, P0401, P0421', reply_markup=get_main_menu())

@bot.message_handler(content_types=['text'])
def text_handler(message):
    text = message.text.lower()
    for brand in CAR_BRANDS:
        if brand.lower() in text:
            bot.send_message(message.chat.id, CAR_BRANDS[brand], reply_markup=get_brands_menu())
            return
    if 'стук' in text or 'стучит' in text:
        bot.send_message(message.chat.id, '🔍 СТУК В ДВИГАТЕЛЕ\n\nВозможные причины:\n• Гидрокомпенсаторы (на холодную)\n• Цепь/ремень ГРМ\n• Подшипники (генератор, помпа)\n• Стук пальцев/вкладышей\n\n⚠️ Рекомендуется срочная диагностика!', reply_markup=get_main_menu())
    elif 'не заводится' in text or 'не запускается' in text:
        bot.send_message(message.chat.id, '🔍 ДВИГАТЕЛЬ НЕ ЗАВОДИТСЯ\n\nПроверьте:\n• Заряд аккумулятора\n• Свечи зажигания\n• Бензонасос (звук при включении)\n• Стартер (крутит или нет)\n• Предохранители', reply_markup=get_main_menu())
    elif 'check' in text or 'чек' in text or 'ошибка' in text:
        bot.send_message(message.chat.id, '🔍 CHECK ENGINE\n\nСчитайте код сканером OBD2 и напишите мне (например: P0420)\n\nИли опишите симптомы:\n• "стук"\n• "не заводится"\n• "вибрирует"', reply_markup=get_main_menu())
    elif 'вибрирует' in text or 'вибрация' in text:
        bot.send_message(message.chat.id, '🔍 ВИБРАЦИЯ\n\nВозможные причины:\n• Дисбаланс колес\n• Износ ШРУСов\n• Проблемы с подушками двигателя\n• Неровности тормозных дисков\n\n💡 Рекомендуется диагностика ходовой', reply_markup=get_main_menu())
    elif 'греется' in text or 'перегрев' in text:
        bot.send_message(message.chat.id, '🔍 ПЕРЕГРЕВ ДВИГАТЕЛЯ\n\nПроверьте:\n• Уровень антифриза\n• Работу вентилятора\n• Термостат\n• Радиатор (чистота)\n• Помпу\n\n️ Немедленно остановитесь!', reply_markup=get_main_menu())
    else:
        bot.send_message(message.chat.id, '🤔 Не понял запрос.\n\nПопробуйте:\n• Код ошибки (P0420)\n• Название марки (Chery, Haval)\n• Опишите проблему (стук, не заводится, греется)', reply_markup=get_main_menu())

if __name__ == '__main__':
    print('🚗 АвтоЯсно запущен')
    bot.infinity_polling()
