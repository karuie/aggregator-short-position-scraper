# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FcaShortPositionsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # Define the fields for your item here
    Position_Holder = scrapy.Field()
    Name_of_Share_Issuer = scrapy.Field()
    ISIN = scrapy.Field()
    Net_Short_Position = scrapy.Field()
    Position_Date = scrapy.Field()
    pass
