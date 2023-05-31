from bs4 import BeautifulSoup
import requests
import json
# import time
import datetime

date = datetime.date.today()
data_base = []

def write_json(data):
    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
        
        

def get_html(url):
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 YaBrowser/23.5.0.2282 Yowser/2.5 Safari/537.36'}
    respone = requests.get(url, headers=headers).text
    return respone


def news_kaktus(html):
    global data_base
    global date
    soup = BeautifulSoup(html, 'lxml')
    list_ = soup.find('div', class_='Tag--articles').find_all('div', class_='ArticleItem')
    
    
    list_count = len(list_)
    print(list_count)
    for i in list_:
        count = 1
        title = i.find('div', class_='ArticleItem--data ArticleItem--data--withImage').find('a', class_='ArticleItem--name').text.replace('\n', '')
        try:
            img = i.find('div', class_='ArticleItem--data ArticleItem--data--withImage').find('a', class_='ArticleItem--image').find('img').get('src')
        except Exception:
            img = "Photo not found"
        link = i.find('div', class_='ArticleItem--data ArticleItem--data--withImage').find('a', class_='ArticleItem--name').get('href')
        des = get_html(link)
        dsoup = BeautifulSoup(des, 'lxml')
        description_list = dsoup.find('div', class_ = 'BbCode').find_all('p')
        description = ''.join([i.text for i in description_list])
        data_base.append(
            {'title':title,
             'photo':img,
             'link':link,
             'description':description}
        )
        # time.sleep(1)
        print(f'Итерация завершена: {list_count - count}')
        count+=1
        list_count-=1
        if len(data_base)==20:break
        elif len(data_base)<21 and list_count != 0:continue
    if len(data_base)!=20:
        date = date - datetime.timedelta(days=1)
        data_news()
    elif len(data_base) ==20:
        print("Программа закончила работу.")
        write_json(data_base)
        data_base = []
        date = datetime.date.today()
        
    
        


def data_news():
    global date
    url = f'https://kaktus.media/?lable=8&date={date}&order=time'
    news_kaktus(get_html(url))


if __name__=='__main__':
    data_news()