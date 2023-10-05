import telebot
from telebot import types
import requests

token_bot = "6481230201:AAFVOV-I-YAu1jnxoTaNZirHGvMZYIhGxZ8"
bot = telebot.TeleBot(token_bot)

Api_key ="4a8c2e8e98bb4251a1d124508230410"

#функция добовления кнопок
def create_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    weathe_today = types.InlineKeyboardButton(text="Погода сегодня", callback_data='1')
    weathe_futur2 = types.InlineKeyboardButton(text="Прогноз погоды на 2 дня", callback_data='2')
    weathe_futur3 = types.InlineKeyboardButton(text="Прогноз погоды на 3 дня", callback_data='3')
    weathe_futur4 = types.InlineKeyboardButton(text="Прогноз погоды на 4 дня", callback_data='4')
    weathe_futur5 = types.InlineKeyboardButton(text="Прогноз погоды на 5 дней", callback_data='5')
    weathe_futur6 = types.InlineKeyboardButton(text="Прогноз погоды на 6 дней", callback_data='6')
    weathe_futur7 = types.InlineKeyboardButton(text="Прогноз погоды на 7 дней", callback_data='7')
    keyboard.add(weathe_today)
    keyboard.add(weathe_futur2)
    keyboard.add(weathe_futur3)
    keyboard.add(weathe_futur4)
    keyboard.add(weathe_futur5)
    keyboard.add(weathe_futur6)
    keyboard.add(weathe_futur7)
    return keyboard

#оброботка команды старт
@bot.message_handler(commands=['start'])
def start_bot(message):
    bot.send_message(
        message.chat.id,
        "Добрый день, я бот для прогноза погоды! Введите название города",
    )

#прием сообщения и проверка есть ли введенный населенный пункт в базе сайта
@bot.message_handler(func=lambda message: True)
def handle_text_message(message):
    global mes
    mes = message.text
    chat_id= message.chat.id
    geo = requests.get(
        f'http://api.weatherapi.com/v1/forecast.json?key={Api_key}&q={mes}&lang=ru')
    geo_data = geo.json()
    if 'error' in geo_data.keys():
        bot.send_message(chat_id, "Не нашел данный населенный пункт, введите другое название")
    else:
        keyboard = create_keyboard()
        bot.send_message(message.chat.id, 'Выберите на сколько дней нужен прогноз', reply_markup=keyboard)


#выбор на сколько дней нужна погода
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "1":
            weather_future(mes, 1, call.message.chat.id)
        elif call.data == "2":
            weather_future(mes, 2, call.message.chat.id)
        elif call.data == "3":
            weather_future(mes, 3, call.message.chat.id)
        elif call.data == "4":
            weather_future(mes, 4, call.message.chat.id)
        elif call.data == "5":
            weather_future(mes, 5, call.message.chat.id)
        elif call.data == "6":
            weather_future(mes, 6, call.message.chat.id)
        elif call.data == "7":
            weather_future(mes, 7, call.message.chat.id)


#получаем данные от API сайта погоды и выводим сообщение
def weather_future(city, days, chat_id):
    geo = requests.get(
        f'http://api.weatherapi.com/v1/forecast.json?key={Api_key}&q={city}&days={days}&lang=ru')
    geo_data = geo.json()
    for i in range(days):
        futur_sity_time = geo_data['forecast']['forecastday'][i]['date']
        futur_sity_max_temp = geo_data['forecast']['forecastday'][i]['day']['maxtemp_c']
        futur_sity_min_temp = geo_data['forecast']['forecastday'][i]['day']['mintemp_c']
        futur_sity_sr_temp = geo_data['forecast']['forecastday'][i]['day']['avgtemp_c']
        futur_sity_max_wind = geo_data['forecast']['forecastday'][i]['day']['maxwind_kph']
        futur_current = geo_data['forecast']['forecastday'][i]['day']['condition']['text']
        fut_weat = ("В городе {}, в день {} ожидается следующая погода:\n"
                    "{}\n"
                    "максимальная температура: {}°\n"
                    "минимальная температура: {}°\n"
                    "средняя температура: {}°\n"
                    "Максимальная скорость ветра: {} км/ч".format(city, futur_sity_time, futur_current, futur_sity_max_temp, futur_sity_min_temp, futur_sity_sr_temp, futur_sity_max_wind))
        bot.send_message(chat_id, fut_weat)

if __name__ == "__main__":
    bot.polling(none_stop=True)