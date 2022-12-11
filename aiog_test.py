from requests_html import HTMLSession
from aiogram import types, executor, Dispatcher, Bot
from bs4 import BeautifulSoup
import requests

bot = Bot('5706348051:AAHQhwvPjTIQfCxIGP9H112NkO9Ryxu58uk')
dp = Dispatcher(bot)

kurs = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()

@dp.message_handler(commands=['start'])
async def start(message: types.message):
    await bot.send_message(message.chat.id, """
Я бот-поисковик великов на сайте <b><a href='https://www.olx.pl/'>olx</a></b>
введи название велика""",
parse_mode = 'html',disable_web_page_preview = 1)


@dp.message_handler(content_types=['text'])
async def parser(message):
    url = 'https://www.olx.pl/d/sport-hobby/rowery/q-' +message.text.replace(' ', '-') +'?search%5Border%5D=filter_float_price:asc&search%5Bfilter_float_price:from%5D=4000'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    all_links = soup.find('a', class_='css-rc5s2u')



    for link in all_links:
        url = 'https://www.olx.pl' + link['href']

        r = requests.get(url)

        soup = BeautifulSoup(r.text, 'html.parser')


        name = soup.find('h1', class_='css-r9zjja-Text').text.strip()
        price = soup.find('h3', class_='css-okktvh-Text').text.strip()
        if float(price.replace('zł', '').replace(' ', '').replace(',','.')) < 4000:
            continue

        img = soup.find('div', class_='swiper-zoom-container')
        img = img.findChildren('img')[0]
        img = img['src']



        await bot.send_photo(message.chat.id, img,
        caption = '<b>' + name + '</b>\n<i>' + price + ' = ' + str(float(price.replace('zł', '').replace(' ', '').replace(',', '.')) * round(float(kurs['Valute']['PLN']['Value']), 2))+' Руб.' + f'</i>\n<a href="{url}">Ссылка на сайт</a>',
        parse_mode = 'html')




        if all_links.index(link) == 3:
            break


executor.start_polling(dp)


