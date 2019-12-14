# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

class CoinSplashSpider(scrapy.Spider):
    name = 'coin_splash'
    allowed_domains = ['www.livecoin.net/en']

    script = '''
            function main(splash, args)

                  splash:on_request(function(request)
                    request:set_header('User-Agent', "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36 Other HTTP headers")
                    end)
                  splash.private_mode_enabled = false
                  
                  url = args.url
                  assert(splash:go(args.url))
                  assert(splash:wait(1))
                  
                  rur_tab = assert(splash:select_all(".filterPanelItem___2z5Gb"))
                  rur_tab[5]:mouse_click()
                  assert(splash:wait(1))
                
                  splash:set_viewport_full()
                  
                  return splash:html()
                
            end
    '''

    def start_requests(self):
        yield SplashRequest(url="https://www.livecoin.net/en", callback=self.parse, endpoint="execute", args={
            'lua_source': self.script
        })

    def parse(self, response):
        for currency in response.xpath("//div[contains(@class, 'ReactVirtualized__Table__row tableRow___3EtiS ')]"):
            yield {
                'currency pair': currency.xpath(".//div[1]/div/text()").get(),
                'volume(24h)':  currency.xpath(".//div[2]/span/text()").get()
            }
