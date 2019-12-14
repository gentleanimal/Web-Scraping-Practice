# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest


class QuotesjsSpider(scrapy.Spider):
    name = 'quotesjs'
    #  Only the Domain name NO /js or it will not give you more than one paqe
    allowed_domains = ["quotes.toscrape.com"]

    script = '''
            function main(splash, args)

                  splash:on_request(function(request)
                    request:set_header('User-Agent', "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36 Other HTTP headers")
                    end)
                  splash.private_mode_enabled = false

                  url = args.url
                  assert(splash:go(args.url))
                  assert(splash:wait(1))

                  splash:set_viewport_full()

                  return splash:html()

            end
    '''

    def start_requests(self):
        yield SplashRequest(url="http://quotes.toscrape.com/js", callback=self.parse, endpoint="execute", args={
            'lua_source': self.script
        })



    def parse(self, response):
        for quote in response.xpath("//div[@class='quote']"):
            yield {
                'Quote': quote.xpath(".//span/text()").get(),
                'Author': quote.xpath(".//span[2]/small/text()").get(),
                'Tags': quote.xpath(".//div/a/text()").getall()
            }

        next_page = response.xpath("//nav/ul/li[@class='next']/a/@href").get()

        if next_page is not None:
            next_page_link = response.urljoin(next_page)
            print(next_page_link)
            yield SplashRequest(url=next_page_link, callback=self.parse, endpoint="execute", args={
                'lua_source': self.script
            })
