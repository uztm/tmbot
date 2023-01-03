import requests
import datetime
# from config import tg_bot_token, open_weather_token
from aiogram import *
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

open_weather_token = "d7748d00159d9aa009b940c9e80a5100"
tg_bot_token = "5635638593:AAFib_FaLcKfPp12aHn438v62oLgwJBxFXU"


bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer(f"Salom {'<b>'}{message.from_user.full_name}{'</b>'} Iltmos Ob-havo haqida ma'lumot olish uchun shahar nomini yozing. 🌤️",parse_mode = 'HTML')



@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Ochiq \U00002600",
        "Clouds": "Bulutli \U00002601",
        "Rain": "Yomg'ir \U00002614",
        "Drizzle": "Yomg'ir \U00002614",
        "Thunderstorm": "Momaqaldiroq \U000026A1",
        "Snow": "Qor \U0001F328",
        "Mist": "Tuman \U0001F32B"
    }

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно, не пойму что там за погода!"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])

        await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
              f"🌤️ Shahar ob-havosi: {city}\n🌡️ Temperatra: {cur_weather}C° {wd}\n"
              f"💧 Namlik: {humidity}%\n🔵 Bosim: {pressure} mm.s\n🌬️ Shamol: {wind} m/с\s\n"
              f"🌅 Quyosh chiqishi: {sunrise_timestamp}\n🌅Quyosh botishi: {sunset_timestamp}\n⏳ Kun davomiyligi: {length_of_the_day}\n"
              f"***Xayrli kun!***"
              )

    except:
        await message.reply("🆎 Shahar nomini tekshiring 🆎")



if __name__ == '__main__':
    executor.start_polling(dp)