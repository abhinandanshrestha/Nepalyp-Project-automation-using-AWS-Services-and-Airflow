# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

# I want to use PostgreSQL as my database
# I have to follow the following steps
# Scraped data --> Item containers --> Store in the database (Postgresql)

import scrapy


class FinalquestionItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    category = scrapy.Field()
    rating = scrapy.Field()
    no_of_reviews = scrapy.Field()
    company_name = scrapy.Field()
    district_location = scrapy.Field()
    phone_no = scrapy.Field()
    website = scrapy.Field()
    working_hour = scrapy.Field()
    establishment_year = scrapy.Field()
    no_of_employee = scrapy.Field()
    company_manager = scrapy.Field()