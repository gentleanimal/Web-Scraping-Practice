# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class CoinsSpider(CrawlSpider):
    name = 'coins'
    allowed_domains = ['coinmarketcap.com']
    start_urls = ['https://coinmarketcap.com/']

    rules = {
        Rule(LinkExtractor(restrict_xpaths="//tr/td[2]/div/a"), callback='parse_item', follow=True),
    }


    def parse_item(self, response):
        yield {
            'name': response.xpath("normalize-space(//h1/text())").get(),
            'rank': response.xpath("//span[@class='cmc-label cmc-label--success sc-13jrx81-0 FVuRP']/text()").get(),
            'price': response.xpath("//span[@class='cmc-details-panel-price__price']/text()").get()
        }
