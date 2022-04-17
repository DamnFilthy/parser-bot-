import codecs
import json

import requests
import telebot
from bs4 import BeautifulSoup

token = 'token'
bot = telebot.TeleBot(token)

url = 'https://quote.rbc.ru/'
header = 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36'


@bot.message_handler()
def command(message):
    request = message.text
    if request.split(' ')[0] == 'news':
        chat_id = '328583718'
        response = requests.get(url, headers={'User-Agent': header})
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')
        obj = soup.findAll('a', attrs={'class': 'q-item__link'})

        item_obj = {}
        result_obj = {}

        for i, post in enumerate(obj):
            preview = post.find('span', class_='q-item__title')
            preview_text = list(map(lambda x: x.text.strip().lower(), preview))
            description = post.find('span', class_='q-item__description').get_text().strip()
            for d, text in enumerate(preview_text):
                if request.split(' ')[1] == 'all' or any((x in text.split(' ') for x in request.split(' '))):
                    item_obj['title'] = text
                    item_obj['description'] = description
                    item_obj['link'] = post.attrs['href']
                    message = f"{text}, {description}, {post.attrs['href']}"
                    bot.send_message(chat_id, text=message)
                    result_obj[i] = item_obj.copy()
            json_res = json.dumps(result_obj, ensure_ascii=False)

            try:
                if request.split(' ')[1] == 'save':
                    with codecs.open("news-data.json", "w", encoding="UTF-8") as file:
                        file.write(json_res)
            except IndexError:
                pass


if __name__ == '__main__':
    bot.polling(none_stop=True)
