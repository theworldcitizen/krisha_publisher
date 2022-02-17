import requests
from bs4 import BeautifulSoup
import pika
import time
import json

from pika import channel

from config import RabbitMQ

headers = {
    'authority': 'krisha.kz',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://krisha.kz/',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
}

ENTRY_POINT = 'https://krisha.kz/'
CITIES = ["almaty", "nur-sultan", "shymkent", "akmolinskaja-oblast", "aktjubinskaja-oblast",
          "almatinskaja-oblast", "atyrauskaja-oblast", "vostochno-kazahstanskaja-oblast", "zhambylskaja-oblast",
          "zapadno-kazahstanskaja-oblast", "karagandinskaja-oblast", "kostanajskaja-oblast",
          "kyzylordinskaja-oblast", "mangistauskaja-oblast", "pavlodarskaja-oblast",
          "severo-kazahstanskaja-oblast", "juzhno-kazahstanskaja-oblast"]
CATEGORIES = ['doma', 'dachi', 'uchastkov', 'ofisa', 'pomeshhenija', 'zdanija', 'magazina', 'prombazy',
              'prochej-nedvizhimosti']


def make_request(url: str, retries=3):
    attempts = 0
    while attempts < retries:
        retries += 1
        try:
            html = requests.get(ENTRY_POINT + url, headers=headers)
            if html.ok:
                return html.text
            else:
                return None
        except requests.exceptions.RequestException as message:
            print(message)
            time.sleep(2)
            attempts += 1
        except AttributeError as message:
            print(message)
        except Exception:
            time.sleep(5)
            pass


def get_soup(html) -> BeautifulSoup:
    soup = BeautifulSoup(html, "html.parser")
    return soup


def get_pagination(soup: BeautifulSoup):
    try:
        content = soup.find('nav', class_='paginator')
        a_elements = content.find_all('a')
        for a in a_elements:
            url = a.get('href')
            text = a.text.strip()
            if text == 'Дальше':
                return url
    except Exception:
        return None
    return None


def get_and_publish_links(soup: BeautifulSoup):
    content = soup.find('section', class_="a-list a-search-list a-list-with-favs")
    divs = content.find_all('div', class_="a-card__inc")
    for div in divs:
        a = div.find('a')
        link = a.get("href")
        channel.basic_publish(exchange='', routing_key=RabbitMQ.RABBIT_MQ_PUBLISH_QUEUE,
                              body=json.dumps(link, ensure_ascii=False))


    return


def loop(soup):
    links = get_and_publish_links(soup)
    return get_pagination(soup)


def run():
    page = make_request('prodazha/doma/almaty/')
    soup = get_soup(page)
    link = loop(soup)
    while True:
        page = make_request(link)
        soup = get_soup(page)
        link = loop(soup)
        if link == None or '':
            break
    return


if __name__ == "__main__":
    credentials = pika.PlainCredentials(username=RabbitMQ.RABBIT_MQ_LOGIN,
                                        password=RabbitMQ.RABBIT_MQ_PASSWORD)

    parameters = pika.ConnectionParameters(host=RabbitMQ.RABBIT_MQ_HOST,
                                           port=RabbitMQ.RABBIT_MQ_PORT,
                                           credentials=credentials)

    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()
    channel.queue_declare(queue=RabbitMQ.RABBIT_MQ_PUBLISH_QUEUE, durable=True)
    channel.basic_qos(prefetch_count=1)
    result = run()


