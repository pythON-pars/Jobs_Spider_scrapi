import time
import requests
import csv
import json
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# This code was written for Windows.

class Strou:
    def __init__(self):
        s = UserAgent()

        self.headers = {
            'user-agent': s.chrome
        }

    def req(self):

        res = requests.get(f'https://www.remontnik.ru/boards/', headers=self.headers)

        print(res.status_code)

        with open('data.html', 'w', encoding='utf-8') as file:
            file.write(res.text)

    def bs(self):
        with open('data.html', encoding='utf-8') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')

        table = soup.find('div', class_='sidebar-item work-categories').find_all('li')

        categiri = []
        for item in table:
            address = 'https://www.remontnik.ru' + item.find('a')['href']
            name = item.find('a').text.strip()

            print(name, address)

            categiri.append(
                {
                    'name':name,
                    'address':address
                }
            )

        with open('fui_data/data_categoria_address.json', 'w', encoding='utf-8') as file:
            json.dump(categiri, file, indent=4, ensure_ascii=False)

    def parsing(self):
        with open('fui_data/data_categoria_address.json', encoding='utf-8') as file:
            src = json.load(file)

        count = 0
        sc = 0
        c = 0
        while True:
            count += 1
            sc += 1

            try:
                api = src[c]['address'] + f'?page={count}'

                print(src[c]['name'], f' Страница №{count} {src[c]["address"]}' + f"?page={count}")

                res = requests.get(api, self.headers)
                soup = BeautifulSoup(res.text, 'lxml')

                date_time = soup.find_all('div', class_='created')
                carta = soup.find_all('div', class_='order-block')

                bimo = pars_data(date_time, api)

                if bimo == 'NULL':
                    # print(bimo)
                    count = 0
                    c += 1
                    continue

            except Exception as ex:
                print(ex)
                continue

            short = []

            for data_and_address in carta:

                try:
                    location = data_and_address.find('div', class_='location').text.strip()
                    address_carts = 'https://www.remontnik.ru' + data_and_address.find('div', class_='title').find('a')['href']
                    name_carts = data_and_address.find('div', class_='title').find('a').text.strip()

                    bim = qa(location)

                    if bim == 'INVALID LOC':
                        continue

                    time.sleep(0.2)

                    short.append(address_carts)

                except Exception as ex:
                    print(f'!!!!{ex}!!!!')
                    continue

            with open(f'fui_data/ad_carts/{sc}_center_data_address_carts.json', 'w', encoding='utf-8') as file:
                json.dump(short, file, indent=4, ensure_ascii=False)

    def test(self=None):

        data = [
            ['Дата:', 'Область и край', 'Подкатегория', 'Цена за работу(целое число)', 'Заголовок', 'Описание',
             'Имя заказчика', 'Адрес заказчика'],
        ]

        with open('test.csv', 'w', encoding='utf-8') as file:
            wr = csv.writer(file)
            wr.writerows(data)

        for i in range(0, 4604):
            try:
                with open(f'fui_data/ad_carts/{i}_center_data_address_carts.json', encoding='utf-8') as file:
                    src = json.load(file)

                print(f'Прошло итераций: {i} ||| Осталось итераций: {4604 - i}')

                for i in src:
                    res = requests.get(i, headers=self.headers)

                    soup = BeautifulSoup(res.text, 'lxml')

                    time_date = soup.find('li', class_='time').text.strip()
                    location = soup.find('li', class_='location').text.strip()
                    name_user = soup.find('li', class_='user').find('a').text.strip()
                    address_name_user = 'https://www.remontnik.ru' + soup.find('li', class_='user').find('a').get('href')
                    price = soup.find('li', class_='budget-icon').text.strip()
                    categori = '«' + soup.find('section', class_='wide-block order-examples').find('h2').text.strip().split('«')[1]
                    title = soup.find('div', class_='order-page').find('h1').text.strip()
                    opi = soup.find('div', class_='order-details').text.strip()

                    data_all = [[time_date, location, categori, price, title, opi, name_user, address_name_user]]

                    with open('test.csv', 'a', encoding='utf-8') as file:
                        wr = csv.writer(file)
                        wr.writerows(data_all)

            except Exception as ex:
                print(ex)
                continue

def main():
    Strou().test()

def rand(text):

    sets = len(text.split(' '))

    for i in range(sets):

        try:

            if text.split(' ')[i] == 'Москва':
                return 'INVALID LOC'

            elif text.split(' ')[i] == 'Москва,':
                return 'INVALID LOC'

            elif text.split(' ')[i] == 'Санкт-Петербург':
                return 'INVALID LOC'

            elif text.split(' ')[i] == 'Московская область':
                return 'INVALID LOC'

            elif text.split(' ')[i] == 'Санкт-Петербург,':
                return 'INVALID LOC'

            elif text.split(' ')[i] == 'Московская':
                return 'INVALID LOC'

            else:
                if i > i:
                    print('pass')

        except Exception as ex:
            print(f'!!!{ex}!!!')
            continue

def pars_data(data_time, api):

    for item in data_time:
        if item.text.strip()[2:5] == 'год':
            print(f'dateTime >>> 12 mounts {api} {item.text.strip()}')
            return 'NULL'

        elif item.text.strip()[2:5] == 'лет':
            print(f'dateTime >>> 12 mounts {api} {item.text.strip()}')
            return 'NULL'

def qa(text):
    sHORT = rand(text)

    if sHORT == None:
        return None

    else:
        return sHORT

if __name__ == '__main__':
    main()
