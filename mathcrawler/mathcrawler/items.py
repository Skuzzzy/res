# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Person(scrapy.Item):
    identifier = scrapy.Field()
    name = scrapy.Field()
    title = scrapy.Field()
    university = scrapy.Field()
    year = scrapy.Field()
    dissertation = scrapy.Field()
    subject_classification = scrapy.Field()
    advisors = scrapy.Field()
    students = scrapy.Field()
