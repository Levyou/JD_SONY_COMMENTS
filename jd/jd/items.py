# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GoodsItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    price = scrapy.Field()
    comment_num = scrapy.Field()
    url = scrapy.Field()


class CommentItem(scrapy.Item):
    user_name = scrapy.Field()
    content = scrapy.Field()
    phone_name = scrapy.Field()
    score = scrapy.Field()
