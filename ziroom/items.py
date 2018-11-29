from scrapy import Item, Field


class ZiRoomItem(Item):
    house_id = Field()
    name = Field()
    face = Field()
    floor = Field()
    floor_total = Field()
    subway_info = Field()
    price = Field()
