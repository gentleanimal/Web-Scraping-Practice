import scrapy
from scrapy.loader import ItemLoader
from demo_project.items import QuoteItem


#  Spider comes in 3 parts - identity, requests, and response
class QuotesToScrape(scrapy.Spider):

    #  Identity
    name = 'goodreads'

    #  Request
    # def start_requests(self):
    #
    #     url = "https://www.goodreads.com/quotes?page=1"
    #     yield scrapy.Request(url=url, callback=self.parse)

    #  Instead of the function above Scrapy also will look for start_urls[ ] Saves code!
    start_urls = [
        "https://www.goodreads.com/quotes?page=1"
    ]
    #  Response
    def parse(self, response):

        #   You can get rid of .selector after response it still should work
        for quote in response.xpath("//div[@class='quote']"):
            loader = ItemLoader(item=QuoteItem(), selector=quote, response=response)
            loader.add_xpath('quote', ".//div[@class='quoteText']/text()[1]")
            loader.add_xpath('author', ".//div[@class='quoteText']/child::span[1]")
            loader.add_xpath('tags', ".//div[@class='greyText smallText left']/a")
            yield loader.load_item()

        # /quotes?page=2 to start next page
        next_page = response.xpath("//a[@class='next_page']/@href").extract_first()

        if next_page is not None:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, callback=self.parse)
