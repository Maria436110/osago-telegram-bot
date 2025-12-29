import telebot
from telebot import types
from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage
from telebot import custom_filters
import os
import logging
from dotenv import load_dotenv
import math

# Загружаем переменные окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Хранилище состояний
state_storage = StateMemoryStorage()

# Получаем токен из переменных окружения
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not BOT_TOKEN:
    logger.error("Токен бота не найден! Убедитесь, что файл .env существует и содержит TELEGRAM_BOT_TOKEN")
    raise ValueError("Токен бота не найден")

bot = telebot.TeleBot(BOT_TOKEN, state_storage=state_storage)

# Коэффициенты (взяты из вашего Tkinter кода)
KT_COEFFICIENTS = {
    'Москва': 1.8, 'Санкт-Петербург': 1.64, 'Воронеж': 1.35,
    'Ростов-на-Дону': 1.56, 'Уфа': 1.56, 'Смоленск': 1.16,
    'Брянск': 1.4, 'Калининград': 1.08, 'Казань': 1.7,
    'Нижний Новгород': 1.56, 'Омск': 1.42, 'Пермь': 1.7,
    'Волгоград': 1.21, 'Краснодар': 1.56, 'Новосибирск': 1.56,
    'Челябинск': 1.77, 'Саратов': 1.42, 'Томск': 1.48,
    'Владивосток': 1.36, 'Рязань': 1.32
}

KC_COEFFICIENTS = {
    3: 0.5, 4: 0.6, 5: 0.65, 6: 0.7,
    7: 0.8, 8: 0.9, 9: 0.95, 10: 1,
    11: 1, 12: 1
}

KBS_COEFFICIENTS = {
    # Стаж 0 лет
    (0, 18, 22): 2.27, (0, 22, 25): 1.88, (0, 25, 30): 1.72,
    (0, 30, 35): 1.56, (0, 35, 40): 1.54, (0, 40, 50): 1.50,
    (0, 50, 60): 1.46, (0, 60, 150): 1.43,
    # Стаж 1 год
    (1, 18, 22): 1.92, (1, 22, 25): 1.72, (1, 25, 30): 1.60,
    (1, 30, 35): 1.50, (1, 35, 40): 1.47, (1, 40, 50): 1.44,
    (1, 50, 60): 1.40, (1, 60, 150): 1.36,
    # Стаж 2 года
    (2, 18, 22): 1.84, (2, 22, 25): 1.71, (2, 25, 30): 1.54,
    (2, 30, 35): 1.48, (2, 35, 40): 1.46, (2, 40, 50): 1.43,
    (2, 50, 60): 1.39, (2, 60, 150): 1.35,
    # Стаж 3-4 года
    (3, 18, 22): 1.65, (3, 22, 25): 1.13, (3, 25, 30): 1.09,
    (3, 30, 35): 1.05, (3, 35, 40): 1.00, (3, 40, 50): 0.96,
    (3, 50, 60): 0.93, (3, 60, 150): 0.91,
    (4, 18, 22): 1.65, (4, 22, 25): 1.13, (4, 25, 30): 1.09,
    (4, 30, 35): 1.05, (4, 35, 40): 1.00, (4, 40, 50): 0.96,
    (4, 50, 60): 0.93, (4, 60, 150): 0.91,
    # Стаж 5-6 лет
    (5, 18, 22): 1.62, (5, 22, 25): 1.10, (5, 25, 30): 1.08,
    (5, 30, 35): 1.04, (5, 35, 40): 0.97, (5, 40, 50): 0.95,
    (5, 50, 60): 0.92, (5, 60, 150): 0.90,
    (6, 18, 22): 1.62, (6, 22, 25): 1.10, (6, 25, 30): 1.08,
    (6, 30, 35): 1.04, (6, 35, 40): 0.97, (6, 40, 50): 0.95,
    (6, 50, 60): 0.92, (6, 60, 150): 0.90,
    # Стаж 7-9 лет
    (7, 22, 25): 1.09, (7, 25, 30): 1.07, (7, 30, 35): 1.01,
    (7, 35, 40): 0.95, (7, 40, 50): 0.94, (7, 50, 60): 0.91,
    (7, 60, 150): 0.89,
    (8, 22, 25): 1.09, (8, 25, 30): 1.07, (8, 30, 35): 1.01,
    (8, 35, 40): 0.95, (8, 40, 50): 0.94, (8, 50, 60): 0.91,
    (8, 60, 150): 0.89,
    (9, 22, 25): 1.09, (9, 25, 30): 1.07, (9, 30, 35): 1.01,
    (9, 35, 40): 0.95, (9, 40, 50): 0.94, (9, 50, 60): 0.91,
    (9, 60, 150): 0.89,
    # Стаж 10-14 лет
    (10, 25, 30): 1.02, (10, 30, 35): 0.97, (10, 35, 40): 0.94,
    (10, 40, 50): 0.93, (10, 50, 60): 0.90, (10, 60, 150): 0.88,
    (11, 25, 30): 1.02, (11, 30, 35): 0.97, (11, 35, 40): 0.94,
    (11, 40, 50): 0.93, (11, 50, 60): 0.90, (11, 60, 150): 0.88,
    (12, 25, 30): 1.02, (12, 30, 35): 0.97, (12, 35, 40): 0.94,
    (12, 40, 50): 0.93, (12, 50, 60): 0.90, (12, 60, 150): 0.88,
    (13, 25, 30): 1.02, (13, 30, 35): 0.97, (13, 35, 40): 0.94,
    (13, 40, 50): 0.93, (13, 50, 60): 0.90, (13, 60, 150): 0.88,
    (14, 25, 30): 1.02, (14, 30, 35): 0.97, (14, 35, 40): 0.94,
    (14, 40, 50): 0.93, (14, 50, 60): 0.90, (14, 60, 150): 0.88,
    # Стаж 15+ лет
    (15, 30, 35): 0.95, (15, 35, 40): 0.93, (15, 40, 50): 0.91,
    (15, 50, 60): 0.86, (15, 60, 150): 0.83,
    (16, 30, 35): 0.95, (16, 35, 40): 0.93, (16, 40, 50): 0.91,
    (16, 50, 60): 0.86, (16, 60, 150): 0.83,
    (17, 30, 35): 0.95, (17, 35, 40): 0.93, (17, 40, 50): 0.91,
    (17, 50, 60): 0.86, (17, 60, 150): 0.83,
    (18, 30, 35): 0.95, (18, 35, 40): 0.93, (18, 40, 50): 0.91,
    (18, 50, 60): 0.86, (18, 60, 150): 0.83,
    (19, 30, 35): 0.95, (19, 35, 40): 0.93, (19, 40, 50): 0.91,
    (19, 50, 60): 0.86, (19, 60, 150): 0.83,
    (20, 30, 35): 0.95, (20, 35, 40): 0.93, (20, 40, 50): 0.91,
    (20, 50, 60): 0.86, (20, 60, 150): 0.83,
}

KO_COEFFICIENTS = {
    'Физическое лицо': 3.16,
    'Юридическое лицо': 1.97,
    'Ограниченная страховка': 1
}

KBM_COEFFICIENTS = {
    (1, 0): 1.76, (1, 1): 3.92,
    (2, 0): 1.17, (2, 1): 2.25, (2, 2): 3.92,
    (3, 0): 1, (3, 1): 2.25, (3, 2): 3.92,
    (4, 0): 0.91, (4, 1): 1.76, (4, 2): 2.25, (4, 3): 3.92,
    (5, 0): 0.83, (5, 1): 1.17, (5, 2): 2.25, (5, 3): 3.92,
    (6, 0): 0.78, (6, 1): 1, (6, 2): 1.76, (6, 3): 3.92,
    (7, 0): 0.74, (7, 1): 1, (7, 2): 1.76, (7, 3): 3.92,
    (8, 0): 0.68, (8, 1): 0.91, (8, 2): 1.76, (8, 3): 3.92,
    (9, 0): 0.63, (9, 1): 0.91, (9, 2): 1.76, (9, 3): 2.25, (9, 4): 3.92,
    (10, 0): 0.57, (10, 1): 0.83, (10, 2): 1.76, (10, 3): 2.25, (10, 4): 3.92,
    (11, 0): 0.52, (11, 1): 0.83, (11, 2): 1.76, (11, 3): 2.25, (11, 4): 3.92,
    (12, 0): 0.46, (12, 1): 0.78, (12, 2): 1.76, (12, 3): 2.25, (12, 4): 3.92,
}

KM_COEFFICIENTS = {
    50: 0.6, 70: 1, 100: 1.1, 120: 1.2, 150: 1.4
}

# Определение состояний
class UserState(StatesGroup):
    waiting_for_insurance_type = State()
    waiting_for_city = State()
    waiting_for_power = State()
    waiting_for_experience = State()
    waiting_for_age = State()
    waiting_for_period = State()
    waiting_for_novice = State()
    waiting_for_accidents = State()
    waiting_for_accident_period = State()

# Хранение данных пользователя
user_data = {}

# Функции расчета (исправленные)
def ko_coef(lico):
    return KO_COEFFICIENTS.get(lico, 1)

def kbm_coef(period, accidents):
    for (per, acc), coef in KBM_COEFFICIENTS.items():
        if per == period and acc == accidents:
            return coef
    return 3.92  # Максимальный коэффициент при несовпадении

def kt_coef(city):
    return KT_COEFFICIENTS.get(city, 1.5)

def kbs_coef(experience, age):
    max_exp = int(min(experience, 20))  # Исправлено: приведение к int
    for (exp, min_age, max_age), coef in KBS_COEFFICIENTS.items():
        if exp == max_exp and min_age <= age < max_age:
            return coef
    return 1.5

def kc_coef(period):
    return KC_COEFFICIENTS.get(period, 1)

def km_coef(power):
    for key in sorted(KM_COEFFICIENTS):
        if power <= key:
            return KM_COEFFICIENTS[key]
    if power > 150:
        return 1.6
    return 1

# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    logger.info(f"Пользователь {message.chat.id} запустил бота")
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Начать расчет")
    btn2 = types.KeyboardButton("ℹ️ Какие данные нужны?")
    btn3 = types.KeyboardButton("📚 Помощь")
    markup.add(btn1, btn2, btn3)
    
    welcome_text = (
        "👋 Привет! Я твой бот-калькулятор ОСАГО!\n\n"
        "Я помогу рассчитать стоимость полиса ОСАГО "
        "на основе твоих данных.\n\n"
        "Выбери действие:"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

# Команда /help
@bot.message_handler(commands=['help'])
@bot.message_handler(func=lambda message: message.text == "📚 Помощь")
def show_help(message):
    help_text = (
        "📚 <b>Доступные команды:</b>\n\n"
        "/start - Начать работу с ботом\n"
        "/help - Показать это сообщение\n"
        "/calc - Начать новый расчет\n\n"
        "<b>Для расчета ОСАГО потребуются:</b>\n"
        "• Вид страхователя\n"
        "• Город регистрации ТС\n"
        "• Мощность двигателя (л.с.)\n"
        "• Стаж вождения (лет)\n"
        "• Возраст водителя\n"
        "• Период страхования\n"
        "• Информация об авариях\n\n"
        "<i>Расчет производится по данным водителя "
        "с наименьшим стажем или новичка.</i>"
    )
    bot.send_message(message.chat.id, help_text, parse_mode='HTML')

# Команда /calc
@bot.message_handler(commands=['calc'])
@bot.message_handler(func=lambda message: message.text == "👋 Начать расчет")
def start_calculation(message):
    try:
        # Инициализируем данные пользователя
        user_data[message.chat.id] = {}
        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('Физическое лицо')
        btn2 = types.KeyboardButton('Юридическое лицо')
        btn3 = types.KeyboardButton('Ограниченная страховка')
        markup.add(btn1, btn2, btn3)
        
        bot.send_message(
            message.chat.id,
            "🏢 Выберите вид страхователя:",
            reply_markup=markup
        )
        bot.set_state(message.from_user.id, UserState.waiting_for_insurance_type, message.chat.id)
        logger.info(f"Пользователь {message.chat.id} начал расчет")
        
    except Exception as e:
        logger.error(f"Ошибка в start_calculation: {e}")
        bot.send_message(message.chat.id, "❌ Произошла ошибка. Попробуйте снова /start")

@bot.message_handler(func=lambda message: message.text == "ℹ️ Какие данные нужны?")
def show_instructions(message):
    instructions = (
        "📋 <b>Для расчета ОСАГО нужны следующие данные:</b>\n\n"
        "1. <b>Вид страхователя:</b>\n"
        "   • Физическое лицо\n"
        "   • Юридическое лицо\n"
        "   • Ограниченная страховка\n\n"
        "2. <b>Город регистрации ТС</b>\n"
        "3. <b>Мощность двигателя</b> (л.с.)\n"
        "4. <b>Стаж вождения</b> (лет)\n"
        "5. <b>Возраст водителя</b>\n"
        "6. <b>Период страхования</b> (3-12 мес.)\n"
        "7. <b>Начинающий водитель?</b>\n"
        "8. <b>Количество аварий</b> (если не новичок)\n\n"
        "<i>Расчет производится по данным водителя "
        "с наименьшим стажем или новичка.</i>"
    )
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Начать расчет")
    markup.add(btn1)
    bot.send_message(message.chat.id, instructions, parse_mode='HTML', reply_markup=markup)

# Обработчики состояний
@bot.message_handler(state=UserState.waiting_for_insurance_type)
def get_insurance_type(message):
    try:
        if message.text in ['Физическое лицо', 'Юридическое лицо', 'Ограниченная страховка']:
            user_data[message.chat.id]['insurance_type'] = message.text
            user_data[message.chat.id]['ko'] = KO_COEFFICIENTS[message.text]
            
            # Создаем клавиатуру с городами
            cities = list(KT_COEFFICIENTS.keys())
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            
            # Добавляем кнопки для городов
            buttons = []
            for i in range(0, len(cities), 2):
                row = cities[i:i+2]
                markup.row(*[types.KeyboardButton(city) for city in row])
            
            bot.send_message(
                message.chat.id,
                "📍 Выберите город регистрации транспортного средства:",
                reply_markup=markup
            )
            bot.set_state(message.from_user.id, UserState.waiting_for_city, message.chat.id)
        else:
            bot.send_message(message.chat.id, "Пожалуйста, выберите один из предложенных вариантов.")
    except Exception as e:
        logger.error(f"Ошибка в get_insurance_type: {e}")
        bot.send_message(message.chat.id, "❌ Произошла ошибка. Попробуйте снова /start")

@bot.message_handler(state=UserState.waiting_for_city)
def get_city(message):
    try:
        if message.text in KT_COEFFICIENTS:
            user_data[message.chat.id]['city'] = message.text
            user_data[message.chat.id]['kt'] = KT_COEFFICIENTS[message.text]
            
            bot.send_message(
                message.chat.id,
                "🚗 Введите мощность двигателя в лошадиных силах (например: 105):",
                reply_markup=types.ReplyKeyboardRemove()
            )
            bot.set_state(message.from_user.id, UserState.waiting_for_power, message.chat.id)
        else:
            bot.send_message(message.chat.id, "Пожалуйста, выберите город из списка.")
    except Exception as e:
        logger.error(f"Ошибка в get_city: {e}")
        bot.send_message(message.chat.id, "❌ Произошла ошибка. Попробуйте снова /start")

@bot.message_handler(state=UserState.waiting_for_power)
def get_power(message):
    try:
        power = float(message.text.replace(',', '.'))
        if power > 0:
            user_data[message.chat.id]['power'] = power
            
            bot.send_message(
                message.chat.id,
                "📅 Введите стаж вождения в годах (например: 5):"
            )
            bot.set_state(message.from_user.id, UserState.waiting_for_experience, message.chat.id)
        else:
            bot.send_message(message.chat.id, "Мощность должна быть положительным числом. Попробуйте снова:")
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите число (например: 105):")
    except Exception as e:
        logger.error(f"Ошибка в get_power: {e}")
        bot.send_message(message.chat.id, "❌ Произошла ошибка. Попробуйте снова /start")

@bot.message_handler(state=UserState.waiting_for_experience)
def get_experience(message):
    try:
        experience = float(message.text.replace(',', '.'))
        if experience >= 0:
            user_data[message.chat.id]['experience'] = experience
            
            bot.send_message(
                message.chat.id,
                "🎂 Введите возраст водителя (от 18 лет):"
            )
            bot.set_state(message.from_user.id, UserState.waiting_for_age, message.chat.id)
        else:
            bot.send_message(message.chat.id, "Стаж не может быть отрицательным. Попробуйте снова:")
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите число (например: 5):")
    except Exception as e:
        logger.error(f"Ошибка в get_experience: {e}")
        bot.send_message(message.chat.id, "❌ Произошла ошибка. Попробуйте снова /start")

@bot.message_handler(state=UserState.waiting_for_age)
def get_age(message):
    try:
        age = int(message.text)
        if age >= 18:
            user_data[message.chat.id]['age'] = age
            
            # Создаем клавиатуру для выбора периода
            periods = list(KC_COEFFICIENTS.keys())
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
            
            for i in range(0, len(periods), 3):
                row = periods[i:i+3]
                markup.row(*[types.KeyboardButton(str(period)) for period in row])
            
            bot.send_message(
                message.chat.id,
                "📆 Выберите период страхования (в месяцах):",
                reply_markup=markup
            )
            bot.set_state(message.from_user.id, UserState.waiting_for_period, message.chat.id)
        else:
            bot.send_message(message.chat.id, "Возраст должен быть не менее 18 лет. Попробуйте снова:")
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите целое число (например: 25):")
    except Exception as e:
        logger.error(f"Ошибка в get_age: {e}")
        bot.send_message(message.chat.id, "❌ Произошла ошибка. Попробуйте снова /start")

@bot.message_handler(state=UserState.waiting_for_period)
def get_period(message):
    try:
        period = int(message.text)
        if 3 <= period <= 12:
            user_data[message.chat.id]['period'] = period
            user_data[message.chat.id]['kc'] = KC_COEFFICIENTS[period]
            
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            btn1 = types.KeyboardButton('Да')
            btn2 = types.KeyboardButton('Нет')
            markup.add(btn1, btn2)
            
            bot.send_message(
                message.chat.id,
                "🎓 Вы начинающий водитель (стаж менее 3 лет)?",
                reply_markup=markup
            )
            bot.set_state(message.from_user.id, UserState.waiting_for_novice, message.chat.id)
        else:
            bot.send_message(message.chat.id, "Период должен быть от 3 до 12 месяцев. Выберите из списка:")
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, выберите период из списка:")
    except Exception as e:
        logger.error(f"Ошибка в get_period: {e}")
        bot.send_message(message.chat.id, "❌ Произошла ошибка. Попробуйте снова /start")

@bot.message_handler(state=UserState.waiting_for_novice)
def get_novice(message):
    try:
        if message.text in ['Да', 'Нет']:
            is_novice = (message.text == 'Да')
            user_data[message.chat.id]['is_novice'] = is_novice
            
            if is_novice:
                user_data[message.chat.id]['kbm'] = 1.17
                # Переходим к расчету
                perform_calculation(message.chat.id, message.from_user.id)
            else:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
                
                # Создаем кнопки для количества аварий
                accidents_buttons = []
                for i in range(0, 5):
                    accidents_buttons.append(types.KeyboardButton(str(i)))
                
                for i in range(0, len(accidents_buttons), 3):
                    row = accidents_buttons[i:i+3]
                    markup.row(*row)
                
                bot.send_message(
                    message.chat.id,
                    "⚠️ Введите количество аварий за последние несколько лет:",
                    reply_markup=markup
                )
                bot.set_state(message.from_user.id, UserState.waiting_for_accidents, message.chat.id)
        else:
            bot.send_message(message.chat.id, "Пожалуйста, ответьте 'Да' или 'Нет':")
    except Exception as e:
        logger.error(f"Ошибка в get_novice: {e}")
        bot.send_message(message.chat.id, "❌ Произошла ошибка. Попробуйте снова /start")

@bot.message_handler(state=UserState.waiting_for_accidents)
def get_accidents(message):
    try:
        accidents = int(message.text)
        if accidents >= 0:
            user_data[message.chat.id]['accidents'] = accidents
            
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
            
            # Создаем кнопки для периода аварийности
            period_buttons = []
            for i in range(1, 13):
                period_buttons.append(types.KeyboardButton(str(i)))
            
            for i in range(0, len(period_buttons), 3):
                row = period_buttons[i:i+3]
                markup.row(*row)
            
            bot.send_message(
                message.chat.id,
                "📊 За какой период (в годах) учитываются аварии?",
                reply_markup=markup
            )
            bot.set_state(message.from_user.id, UserState.waiting_for_accident_period, message.chat.id)
        else:
            bot.send_message(message.chat.id, "Количество аварий не может быть отрицательным. Попробуйте снова:")
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите число (например: 0, 1, 2):")
    except Exception as e:
        logger.error(f"Ошибка в get_accidents: {e}")
        bot.send_message(message.chat.id, "❌ Произошла ошибка. Попробуйте снова /start")

@bot.message_handler(state=UserState.waiting_for_accident_period)
def get_accident_period(message):
    try:
        accident_period = int(message.text)
        if 1 <= accident_period <= 12:
            user_data[message.chat.id]['accident_period'] = accident_period
            
            # Рассчитываем КБМ
            accidents = user_data[message.chat.id].get('accidents', 0)
            kbm = kbm_coef(accident_period, accidents)
            user_data[message.chat.id]['kbm'] = kbm
            
            # Переходим к расчету
            perform_calculation(message.chat.id, message.from_user.id)
        else:
            bot.send_message(message.chat.id, "Период должен быть от 1 до 12 лет. Выберите из списка:")
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, выберите период из списка:")
    except Exception as e:
        logger.error(f"Ошибка в get_accident_period: {e}")
        bot.send_message(message.chat.id, "❌ Произошла ошибка. Попробуйте снова /start")

def perform_calculation(chat_id, user_id):
    try:
        data = user_data.get(chat_id, {})
        if not data:
            bot.send_message(chat_id, "❌ Данные не найдены. Начните расчет снова /start")
            return
        
        # Получаем все коэффициенты
        ko = data.get('ko', 1)
        kt = data.get('kt', 1)
        power = data.get('power', 100)
        experience = data.get('experience', 5)
        age = data.get('age', 30)
        period = data.get('period', 10)
        kc = data.get('kc', 1)
        kbm = data.get('kbm', 1)
        
        # Рассчитываем остальные коэффициенты
        kbs = kbs_coef(experience, age)
        km = km_coef(power)
        
        # Базовые тарифы
        tarif_min = 1646
        tarif_max = 3535
        
        # Рассчитываем стоимость
        summa_min = int(tarif_min * ko * km * kc * kbs * kbm * kt)
        summa_max = int(tarif_max * ko * km * kc * kbs * kbm * kt)
        
        # Формируем результат
        result_text = (
            f"✅ <b>Расчет ОСАГО завершен!</b>\n\n"
            f"📊 <b>Итоговая стоимость:</b>\n"
            f"   <b>От:</b> {summa_min:,} руб.\n"
            f"   <b>До:</b> {summa_max:,} руб.\n\n"
            f"📈 <b>Примененные коэффициенты:</b>\n"
            f"   КО (вид страхования): {ko}\n"
            f"   КТ (территория): {kt}\n"
            f"   КВС (стаж/возраст): {kbs}\n"
            f"   КС (период): {kc}\n"
            f"   КБМ (аварийность): {kbm}\n"
            f"   КМ (мощность): {km}\n\n"
            f"📋 <b>Введенные данные:</b>\n"
            f"   Вид страхования: {data.get('insurance_type', 'Не указано')}\n"
            f"   Город: {data.get('city', 'Не указан')}\n"
            f"   Мощность: {power} л.с.\n"
            f"   Стаж: {experience} лет\n"
            f"   Возраст: {age} лет\n"
            f"   Период: {period} мес.\n"
            f"   Новичок: {'Да' if data.get('is_novice', False) else 'Нет'}"
        )
        
        if not data.get('is_novice', True):
            result_text += f"\n   Аварий: {data.get('accidents', 0)} за {data.get('accident_period', 1)} лет"
        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("👋 Начать новый расчет")
        btn2 = types.KeyboardButton("📚 Помощь")
        markup.add(btn1, btn2)
        
        bot.send_message(chat_id, result_text, reply_markup=markup, parse_mode='HTML')
        
        # Логируем успешный расчет
        logger.info(f"Пользователь {chat_id} выполнил расчет: {summa_min} - {summa_max} руб.")
        
    except Exception as e:
        logger.error(f"Ошибка в perform_calculation для пользователя {chat_id}: {e}")
        bot.send_message(chat_id, "❌ Произошла ошибка при расчете. Попробуйте снова /start")
    
    finally:
        # Очищаем состояние и данные пользователя
        try:
            bot.delete_state(user_id, chat_id)
            if chat_id in user_data:
                del user_data[chat_id]
        except:
            pass

@bot.message_handler(func=lambda message: message.text == "👋 Начать новый расчет")
def new_calculation(message):
    start_calculation(message)

# Обработчик всех остальных сообщений
@bot.message_handler(func=lambda message: True)
def handle_other_messages(message):
    if message.text not in ["👋 Начать расчет", "ℹ️ Какие данные нужны?", "👋 Начать новый расчет", "📚 Помощь"]:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("👋 Начать расчет")
        btn2 = types.KeyboardButton("📚 Помощь")
        markup.add(btn1, btn2)
        
        bot.send_message(
            message.chat.id,
            "Для начала расчета нажмите '👋 Начать расчет'.\n"
            "Для получения помощи нажмите '📚 Помощь'",
            reply_markup=markup
        )

# Регистрация фильтров состояний
bot.add_custom_filter(custom_filters.StateFilter(bot))

# Обработка ошибок
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        bot.answer_callback_query(call.id)
    except Exception as e:
        logger.error(f"Ошибка в callback_query: {e}")

if __name__ == "__main__":
    logger.info("Бот запускается...")
    try:
        bot.polling(none_stop=True, interval=0, timeout=60)
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")