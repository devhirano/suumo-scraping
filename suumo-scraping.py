#!/usr/bin/env python3

from bs4 import BeautifulSoup
import urllib3
import re
import requests
import time
import pandas as pd
from pandas import Series, DataFrame

#URL（ここにURLを入れてください）
url = 'https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=13&sc=13120&cb=8.5&ct=15.0&mb=65&mt=9999999&md=06&md=07&md=09&md=10&md=11&md=12&md=13&md=14&ts=1&et=9999999&cn=30&co=1&kz=1&kz=2&kz=4&tc=0400301&tc=0400503&tc=0401301&shkr1=03&shkr2=03&shkr3=03&shkr4=03&sngz=&po1=04'

result = requests.get(url)
c = result.content

soup = BeautifulSoup(c)

summary = soup.find("div",{'id':'js-bukkenList'})
body = soup.find("body")
pages = body.find_all("div",{'class':'pagination pagination_set-nav'})
pages_text = str(pages)
pages_split = pages_text.split('</a></li>\n</ol>')

names = []
addresses = []
locations0 = []
locations1 = []
locations2 = []
ages = []
heights = []
floors = []
rent = []
admin = []
rentsum = []
others = []
floor_plans = []
areas = []
detail_urls = []

urls = [
    'https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=13&sc=13120&cb=8.5&ct=15.0&mb=65&mt=9999999&md=06&md=07&md=09&md=10&md=11&md=12&md=13&md=14&ts=1&et=9999999&cn=30&co=1&kz=1&kz=2&kz=4&tc=0400301&tc=0400503&tc=0401301&shkr1=03&shkr2=03&shkr3=03&shkr4=03&sngz=&po1=04&page=1',
    'https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=13&sc=13120&cb=8.5&ct=15.0&mb=65&mt=9999999&md=06&md=07&md=09&md=10&md=11&md=12&md=13&md=14&ts=1&et=9999999&cn=30&co=1&kz=1&kz=2&kz=4&tc=0400301&tc=0400503&tc=0401301&shkr1=03&shkr2=03&shkr3=03&shkr4=03&sngz=&po1=04&page=2',
    'https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=13&sc=13120&cb=8.5&ct=15.0&mb=65&mt=9999999&md=06&md=07&md=09&md=10&md=11&md=12&md=13&md=14&ts=1&et=9999999&cn=30&co=1&kz=1&kz=2&kz=4&tc=0400301&tc=0400503&tc=0401301&shkr1=03&shkr2=03&shkr3=03&shkr4=03&sngz=&po1=04&page=3',
    'https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=13&sc=13120&cb=8.5&ct=15.0&mb=65&mt=9999999&md=06&md=07&md=09&md=10&md=11&md=12&md=13&md=14&ts=1&et=9999999&cn=30&co=1&kz=1&kz=2&kz=4&tc=0400301&tc=0400503&tc=0401301&shkr1=03&shkr2=03&shkr3=03&shkr4=03&sngz=&po1=04&page=4',
]

urls.append(url)


for url in urls:
    result = requests.get(url)
    c = result.content
    soup = BeautifulSoup(c)
    summary = soup.find("div",{'id':'js-bukkenList'})
    apartments = summary.find_all("div",{'class':'cassetteitem'})

    for apartment in apartments:

        room_number = len(apartment.find_all('tbody'))

        name = apartment.find('div', class_='cassetteitem_content-title').text
        address = apartment.find('li', class_='cassetteitem_detail-col1').text

        for i in range(room_number):
            names.append(name)
            print(name)
            addresses.append(address)

        sublocation = apartment.find('li', class_='cassetteitem_detail-col2')
        cols = sublocation.find_all('div')
        for i in range(len(cols)):
            text = cols[i].find(text=True)
            for j in range(room_number):
                if i == 0:
                    locations0.append(text)
                elif i == 1:
                    locations1.append(text)
                elif i == 2:
                    locations2.append(text)

        age_and_height = apartment.find('li', class_='cassetteitem_detail-col3')
        age = age_and_height('div')[0].text
        height = age_and_height('div')[1].text

        for i in range(room_number):
            ages.append(age.replace('築',''))
            heights.append(height)

        table = apartment.find('table')
        rows = []
        rows.append(table.find_all('tr'))

        data = []
        for row in rows:
            for tr in row:
                cols = tr.find_all('td')
                if len(cols) != 0:
                    _floor = cols[2].text
                    _floor = re.sub('[\r\n\t]', '', _floor)

                    _rent_cell = cols[3].find('ul').find_all('li')
                    _rent = _rent_cell[0].find('span').text
                    _admin = _rent_cell[1].find('span').text

                    _rentsum = float(_rent.replace('万円','')) * 10000
                    if '円' in _admin:
                        _rentsum += float(_admin.replace('円',''))

                    _deposit_cell = cols[4].find('ul').find_all('li')
                    _deposit = _deposit_cell[0].find('span').text
                    _reikin = _deposit_cell[1].find('span').text
                    _others = _deposit + '/' + _reikin

                    _floor_cell = cols[5].find('ul').find_all('li')
                    _floor_plan = _floor_cell[0].find('span').text
                    _area = _floor_cell[1].find('span').text

                    _detail_url = cols[8].find('a')['href']
                    _detail_url = 'https://suumo.jp' + _detail_url

                    text = [_floor, _rent, _admin, _rentsum, _others, _floor_plan, _area, _detail_url]
                    data.append(text)

        for row in data:
            floors.append(row[0])
            rent.append(row[1])
            admin.append(row[2])
            rentsum.append(row[3])
            others.append(row[4])
            floor_plans.append(row[5])
            areas.append(row[6])
            detail_urls.append(row[7])

        time.sleep(1)

names = Series(names)
addresses = Series(addresses)
locations0 = Series(locations0)
locations1 = Series(locations1)
locations2 = Series(locations2)
ages = Series(ages)
heights = Series(heights)
floors = Series(floors)
rent = Series(rent)
admin = Series(admin)
rentsum = Series(rentsum)
others = Series(others)
floor_plans = Series(floor_plans)
areas = Series(areas)
detail_urls = Series(detail_urls)

suumo_df = pd.concat([
    names,
    addresses,
    locations0,
    locations1,
    locations2,
    ages,
    heights,
    floors,
    rent,
    admin,
    rentsum,
    others,
    floor_plans,
    areas,
    detail_urls
],axis=1)

suumo_df.columns=['マンション名','住所','立地1','立地2','立地3','築年数','建物の高さ','階層','賃料料','管理費', '賃料計', '敷/礼/保証/敷引,償却','間取り','専有面積', '詳細URL']

suumo_df.to_csv('suumo.csv', sep = '\t', encoding='utf-16', header=True, index=False)
