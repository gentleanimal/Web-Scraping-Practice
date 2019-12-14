# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem


class FilterDuplicate(object):

    def open_spider(self, spider):
        # instantiate your set here
        self.quote = set()

    def process_item(self, item, spider):
        # check if item is already in your set:
        if item['quote'] in self.quote:
            raise DropItem("Item dropped {0}".format(item.get('quote')))
        else:
            # means if the item doesn't exist in your set then add it to it
            self.quote.add(item['quote'])
            return item
