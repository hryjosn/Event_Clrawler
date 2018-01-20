from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from time import sleep
import io
import json

pages = set()
page_num = 1
dataList = []

def getLinks():
    global pages, page_num, dataList
    print('第', page_num, '頁')
    html = urlopen('https://kktix.com/events?category_id=2&page='+str(page_num))  # The target URL //+str(page_num)
    bsobj = BeautifulSoup(html, "html.parser")
    event_num = 0  # event_num　record this page's number of event
    for link in bsobj.find('ul', {'class': 'event-list'}).findAll('a', {}, href=re.compile("/events/")):  #
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                newPage = link.attrs['href']
                # try:
                getInform(newPage)
                # except Exception as e:
                #     print('ERROR:',e)
                pages.add(newPage)
                event_num = event_num + 1
    page_num = page_num + 1
    if event_num >= 10:
        getLinks()


def getInform(URL):
    html = urlopen(URL)
    bsobj = BeautifulSoup(html, "html.parser")
    title = bsobj.find('div', {'class': 'header-title'})
    if ((title is not None) & ((bsobj.find('ul', {'class': 'info'})) is not None) &
            ((bsobj.find('div', {'id': 'map-content'})) is not None)):  # Time and Title is necerssary
        print(title.get_text())
        date = []
        for Object in bsobj.find('ul', {'class': 'info'}).findAll('span', {'class': 'timezoneSuffix'}):
            for a in Object:
                date.append(a)
            lat = bsobj.find('div', {'id': 'map-content'}).attrs['data-lat']
            lng = bsobj.find('div', {'id': 'map-content'}).attrs['data-lng']
        data = {}
        data.update({'Title': title.get_text().strip('\n')})
        data.update({'Date': date})
        data.update({'Lat': lat})
        data.update({'Lng': lng})
        dataList.append(data)
        print(dataList)

    with io.open('data.json', 'w', encoding='utf-8') as  json_file:
        json.dump(dataList, json_file, ensure_ascii=False)
    sleep(1)


getLinks()
