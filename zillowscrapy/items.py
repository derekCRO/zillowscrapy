# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZillowItem(scrapy.Item):   
    state = scrapy.Field()
    city = scrapy.Field()
    zipcode = scrapy.Field()
    neighborhood = scrapy.Field()
    lot = scrapy.Field()
    mls = scrapy.Field()
    year = scrapy.Field()
    price = scrapy.Field()
    zestimate = scrapy.Field()
    zestimate_rent = scrapy.Field()
    bed = scrapy.Field()
    bath = scrapy.Field()
    address = scrapy.Field()
    desc = scrapy.Field()
    agent_name = scrapy.Field()
    agent_number = scrapy.Field()
    listing_type = scrapy.Field()
    image_url = scrapy.Field()
    timestamp = scrapy.Field()
    url = scrapy.Field()
    property_type = scrapy.Field()
