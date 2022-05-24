import random
import re
import requests
import json
from bs4 import BeautifulSoup
import winsound
import time
import os


class Pastebin:
    @staticmethod
    def test_security():
        hwid = '03DE0294-0480-05A8-B406-C8070008'
        r = requests.get('https://pastebin.com/4v7EfdYJ')
        try:
            if hwid in r.text:
                pass
            else:
                print('Ошибка, данных hwid не был найден в базе данных')
                # print(f'HWID: {hwid}')
                time.sleep(5)
                os._exit()
        except:
            print('Ошибка, не удаётся соединится с базой данных')
            time.sleep(5)
            os._exit()
        print('Доступ разрешен')


class Notepad:
    @staticmethod
    def get_desired_keywords():
        list_keywords = open("keywords.txt", encoding='utf-8').read().split()
        return list_keywords

    @staticmethod
    def get_word_response():
        list_words = open("Words_on_response.txt", encoding='utf-8').readlines()
        return list_words


class Bot:
    def __init__(self, url):
        self.url = url
        self.price = None
        self.session = requests.Session()
        self.session.headers.update({
            'Connection': 'keep - alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0'
        })
        with open('Kwork_Cookies.json') as f:
            self.session.cookies.update(json.load(f))

    def sending_response(self):
        words_response = Notepad.get_word_response()
        id_users = self.get_id_users()
        for user_id in id_users:
            data = {
                'offerType': 'custom', 'wantId': user_id,'offerId': None,'description': words_response[0], 'kwork_count': '1', 'kwork_package_type': 'standard', 'kwork_name': words_response[1],'kwork_price': self.price, 'kwork_duration': '1'
            }
            resp = self.session.post('https://kwork.ru/api/offer/createoffer', data=data).json()
            print(resp)
            self.message_sound()
            self.price = self.test_resp_response(resp)
            time.sleep(2)
        if not id_users:
            print('Заказов пока нет...')
            time.sleep(random.randint(60, 120))

    def get_id_users(self):
        user_id = []
        for i in self.get_found_keywords():
            user_id.append(self.crop_link(i['link']))
        return user_id

    def test_resp_response(self, resp):
        if not resp['success']:
            return self.get_minimum_price(resp)

    @staticmethod
    def message_sound():
        freq = 440  # Hz
        winsound.MessageBeep(freq)

    @staticmethod
    def get_minimum_price(resp):
        r = resp['message']
        min = re.findall(r'\d+', r)
        return min[0]

    @staticmethod
    def crop_link(link):
        return link[26:33]

    def get_found_keywords(self):
        sort = []
        for i in self.get_list_orders():
            for j in Notepad.get_desired_keywords():
                if i['name'].lower().count(j) > 0:
                    sort.append(i)
        return sort

    def get_list_orders(self):
        list_orders = []
        resp = self.session.get(self.url)
        soup = BeautifulSoup(resp.text, 'lxml')
        items = soup.find_all('div', class_='card__content pb5')
        for item in items:
            list_orders.append({
                'name': item.find('div', class_='wants-card__header-title').text,
                'link': item.find('a').get('href')
            })
        return list_orders


def main():
    bot = Bot(url=input("Вставьте ссылку для начала: "))
    print('Программа запущена')
    print('Цена будет выставляться автоматически минимальная, так как может случиться не соответсвие цены с заказом. Почему минимальная? Так как выше шанс потом договориться с покупателем')
    try:
        while True:
            bot.sending_response()
    except BaseException:
        #TODO: Дорабоать исключение
        print('Вызвано исключение')


if __name__ == '__main__':
    main()

input()