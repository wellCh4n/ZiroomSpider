import json
import uuid
from io import BytesIO

import requests
import scrapy
import pytesseract
from PIL import Image
from scrapy.spiders import CrawlSpider

from ziroom_demo.ziroom.items import ZiRoomItem


class ZiRoomSpider(CrawlSpider):
    name = 'ziroom_spider'

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.page = 1

    def start_requests(self):
        url = 'https://miniphoenix.ziroom.com/v7/room/list.json?city_code=330100&page={}&size=10'.format(self.page)
        yield scrapy.Request(url=url, callback=self.parse_data)

    def parse_data(self, response):
        response_data = json.loads(response.text)
        rooms = response_data.get('data').get('rooms')

        if len(rooms) <= 0:
            return

        rule_dict = {}

        for room in rooms:
            house_id = room.get('house_id')
            name = room.get('name')
            face = room.get('face')
            floor = room.get('floor')
            floor_total = room.get('floor_total')
            subway_info = room.get('subway_station_info')
            price = room.get('price')

            price_img = price[0]
            file_name = save_img('http:{}'.format(price_img))
            price_rule = price[1]
            real_price = parse_price(file_name, price_rule, rule_dict)

            item = ZiRoomItem()
            item['house_id'] = house_id
            item['name'] = name
            item['face'] = face
            item['floor'] = floor
            item['floor_total'] = floor_total
            item['subway_info'] = subway_info
            item['price'] = real_price

            yield item

        self.page += 1
        url = 'https://miniphoenix.ziroom.com/v7/room/list.json?city_code=330100&page={}&size=10'.format(self.page)
        yield scrapy.Request(url=url, callback=self.parse_data)


def save_img(url):
    url_arr = url.split('/')
    file_name = url_arr[len(url_arr) - 1]

    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    image.save(file_name)
    return file_name


def parse_price(file_name, rule_arr, rule_dict):
    rule_arr.reverse()
    image = Image.open(file_name)
    width, height = image.size
    price = ''
    for i in range(len(rule_arr)):
        if not rule_dict.get(rule_arr[i]):
            inx = len(rule_arr) - i - 1
            position = rule_arr[inx] * 30
            v_width = 30
            box = (position, 0, position + v_width, height)
            v = image.crop(box)
            white = Image.new('L', (120, 50), 'black')
            white.paste(v, (0, 10))
            white.paste(v, (30, 10))
            white.paste(v, (60, 10))
            white.paste(v, (90, 10))
            num = pytesseract.image_to_string(white)[0:1]
            rule_dict[rule_arr[i]] = num
            price += num
        else:
            num = rule_dict[rule_arr[i]]
            price += num
    return price



