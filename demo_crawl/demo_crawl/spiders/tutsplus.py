# -*- coding: utf-8 -*-

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class TutsplusSpider(CrawlSpider):
    name = 'tutsplus'
    allowed_domains = ['tutsplus.com']
    start_urls = ['https://code.tutsplus.com/categories/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//a[@class='alphadex__item-link']"), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths="//ol[@class='posts category-sidebar-ad-mobile view posts--with-sidebar nolinks view--loaded']/li"), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths="//a[@class='pagination__button pagination__next-button']"),
             callback='parse_item', follow=True),
    )

    def parse_item(self, response):

        for tutorial in response.xpath("//li[@class='posts__post  ']"):
            yield {
                'title': tutorial.xpath(".//a[@class='posts__post-title ']/h1/text()").extract_first(),
                'link': tutorial.xpath(".//a[@class='posts__post-title ']/@href").extract_first(),
                'category': response.xpath("//span[@class='content-banner__title-breadcrumb-category']/text()").extract_first(),
                'user agent': response.request.headers.get('User-Agent').decode('utf-8')
            }
