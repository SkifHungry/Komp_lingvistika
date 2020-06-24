import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

# https://v1.ru/

client = MongoClient()
db = client.news_parser
news_coll = db.news

def getHtml(url):
    r = requests.get(url)
    return r.text

def getNews(html):
    soup = BeautifulSoup(html, 'lxml')
    news = soup.findAll('article', class_='MNazv')
    newTexts = ""
    for i in range(len(news)):
        Name = news[i].find('h2', class_='MNb9').find('a').text
        Link = 'https://v1.ru' + news[i].find('h2', class_='MNb9').find('a').get('href')
        Date = news[i].find('time').get('datetime')
        Views = news[i].find('div', class_='LXch').find('span').text.replace("\xa0", "")

        if news[i].find('div', class_='LXawl').findAll('span', class_='LXbt')[1].text == " Обсудить ":
            Comments = "0"
        else:
            Comments = news[i].find('div', class_='LXawl').findAll('span', class_='LXbt')[1].text

        verify = news_coll.find_one({'Name news': Name})
        if not(verify == 'None'):
            for new in news_coll.find():
                if new['Name news'] == Name:
                    new['Views news'] = Views
                    new['Comments news'] = Comments
        else:
            soup2 = BeautifulSoup(
                getHtml('https://v1.ru' + news[i].find('h2', class_='MNb9').find('a').get('href')),
                'lxml')
            blocks = soup2.findAll('div', class_='LTawf')
            for k in range(len(blocks)):
                texts = blocks[k].findAll('p')
                for r in range(len(texts)):
                    newTexts += texts[r].text + '\n'
            Text = newTexts
            newTexts = ""

            news_doc = {
                "Name news": Name,
                "Date news": Date,
                "Link news": Link,
                "Text news": Text,
                "Views news": Views,
                "Comments news": Comments
            }
            news_coll.insert_one(news_doc)


url = "https://v1.ru/text/"

getNews(getHtml(url))





