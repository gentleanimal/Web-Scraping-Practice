import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class QuotesToScrapeCrawlSpider(CrawlSpider):

    name = "quotestoscrapecrawl"
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ["http://quotes.toscrape.com"]

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//span[@class='tag-item']/a[@class='tag']"), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths="//li[@class='next']/a"), callback='parse_item', follow=True)
    )

    def parse_item(self, response):

        for tag in response.xpath("//span[@class='tag-item']/a[@class='tag']"):
            for quote in tag.xpath("//div[@class='quote']"):
                yield {
                    'quote': quote.xpath(".//span[@class='text']/text()").extract_first()
                }
