import telebot
import requests
from translate import Translator

bot = telebot.TeleBot('токен телеграм бота')
API = 'API токен для сайта с прогнозом погоды'

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Привет, рад тебя видеть! Напиши название своего города')

@bot.message_handler(commands=['today'])
@bot.message_handler(commands=['tomorrow'])
@bot.message_handler(commands=['week'])
def error(message):
    pass

@bot.message_handler(content_types=['text'])
def get_weather(message):
    '''
    Принимает от пользователя город, возвращает ответ сколько градусов и советует что надеть
    '''
    translator = Translator(to_lang="en")
    city = translator.translate(str(message.text.strip().lower()))
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if res.status_code == 200:
        data = res.json()
        temp = data["main"]["temp"]
        bot.send_message(message.chat.id, f'На улице: {round(temp)}°C')
        сlothe(message, temp)
    else:
        bot.send_message(message.chat.id,'город указан не верно')

def сlothe(message,temp):
    '''
    Функция в зависимости от температуры возвращает что надеть
    '''
    if temp < -25: bot.send_message(message.chat.id, f'Сегодня мороз❄️\n'
                                         f'Советую надеть:\nТеплую зимнюю куртку\nУтепленные ботинки\nТеплую шапку или варежки\nПредварительно выпить стопку водки перед выходом')
    elif 25 <= temp <= -15:
       bot.send_message(message.chat.id, f'Сегодня мороз❄️\n'
                                         f'Советую надеть:\nТеплую зимнюю куртку\nУтепленные ботинки\nТеплую шапку или варежки')
    elif -15 < temp <= -5:
        bot.send_message(message.chat.id, f'Сегодня холодно❄️\n'
                                          f'Советую надеть:\nЗимнюю куртку или пуховик\nУтепленные ботинки или сапоги\nШапку\nВарежки или перчатки')
    elif -5 < temp <= 5:
        bot.send_message(message.chat.id, f'Сегодня холодно☁️\n'
                                          f'Советую надеть:\nТеплую куртку или пальто\nОбувь на теплой подошве (ботинки или полуботинки)\nШапка или ушанка\nПерчатки или варежки')
    elif 5 < temp <= 15:
        bot.send_message(message.chat.id, f'Сегодня холодновато🌥\n'
                                          f'Советую надеть:\nЛегкую куртка или ветровка\nДемисезонную обувь (ботинки или кеды)\nШапку или легкий головной убор')
    elif 15 < temp <= 25:
        bot.send_message(message.chat.id, f'Сегодня тепло☀️\n'
                                          f'Советую надеть:\nФутболку, рубашку или блузку\nЛегкие брюки или юбка\nЛегкая обувь (туфли, сандалии, кеды)')
    elif 25 < temp:
        bot.send_message(message.chat.id, f'Сегодня жарко☀️\n'
                                          f'Советую надеть:\nЛегкую одежду (платье, футболка, шорты)\nЛегку обувь (сандалии, тапочки, кеды)')

bot.polling(none_stop=True)






