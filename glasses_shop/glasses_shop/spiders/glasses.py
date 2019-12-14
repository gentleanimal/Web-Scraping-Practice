# -*- coding: utf-8 -*-
import scrapy


class GlassesSpider(scrapy.Spider):
    name = 'glasses'
    allowed_domains = ['www.glassesshop.com']
    start_urls = ['https://www.glassesshop.com/bestsellers']

    def parse(self, response):
        glasses = response.xpath("//div[contains(@class, 'm-p-product')]")
        for glass in glasses:
            yield {
                'url': glass.xpath(".//div[@class='pimg default-image-front']/a/@href").get(),
                'img_url': glass.xpath(".//div[@class='pimg default-image-front']/a/img[1]/@src").get(),
                'name': glass.xpath(".//div[@class='row']/p[contains(@class, 'pname')]/a/text()").get(),
                'price': glass.xpath(".//div[@class='row']/div[contains(@class, 'pprice')]/span/text()").get()
            }

        next_page = response.xpath("//ul[@class='pagination']/li[position() = last()]/a/@href").get()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)
