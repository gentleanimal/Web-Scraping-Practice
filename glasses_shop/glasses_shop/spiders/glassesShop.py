# -*- coding: utf-8 -*-
import scrapy


class GlassesShopSpider(scrapy.Spider):
    name = 'glassesShop'
    allowed_domains = ["www.glassesshop.com"]
    start_urls = ["https://www.glassesshop.com/bestsellers"]

    def parse(self, response):
        glasses = response.xpath("//div[@class='col-sm-6 col-md-4 m-p-product']")
        for glass in glasses:
            product_url = glass.xpath(".//div[@class='pimg default-image-front']/a/@href").get()
            image_url = glass.xpath(".//div[@class='pimg default-image-front']/a/img[1]/@src").get()
            product_name = glass.xpath(".//div[@class='row']/p/a/text()").get()
            product_price = glass.xpath(".//div[@class='pprice col-sm-12']/span/text()").get()
            yield {
                'product_url': product_url,
                'product_image_link': image_url,
                'product_name': product_name,
                'product_price': product_price
            }
        next_page = response.xpath("//a[contains(@aria-label, 'Next »')]/@href").get()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)
