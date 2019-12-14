import scrapy


#  Spider comes in 3 parts - identity, requests, and response
class QuotesToScrape(scrapy.Spider):

    #  Identity
    name = 'goodreadsOld'

    #  Request
    def start_requests(self):

        url = "https://www.goodreads.com/quotes?page=1"
        yield scrapy.Request(url=url, callback=self.parse)

        #  Response
    def parse(self, response):

        for quote in response.selector.xpath("//div[@class='quote']"):
            yield {

                'quote': quote.xpath(".//div[@class='quoteText']/text()[1]").extract_first(),
                'author': quote.xpath(".//div[@class='quoteText']/child::span[1]/text()").extract_first(),
                'tags': quote.xpath(".//div[@class='greyText smallText left']/a/text()").extract()
            }

        # /quotes?page=2 to start next page
        next_page = response.selector.xpath("//a[@class='next_page']/@href").extract_first()

        if next_page is not None:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, callback=self.parse)

#  When you want to run it in the terminal type into the terminal - scrapy crawl goodreads
#  When you want to run it and save the file, the -o is output
#  scrapy crawl goodreads -o filename. - if it is a csv or json put it at the end
#  If you want it automatic then uncomment the appropriate line in settings.py
