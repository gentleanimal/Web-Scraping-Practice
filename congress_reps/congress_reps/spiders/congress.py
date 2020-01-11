# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
#from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class CongressSpider(CrawlSpider):
    name = 'congress'
    allowed_domains = ["congress.gov"]

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
#  "https://www.congress.gov/members?q={%22congress%22:[%22116%22,%22115%22,%22114%22,%22113%22,%22112%22,%22111%22,%22110%22,%22109%22,%22108%22,107]}&pageSort=state&searchResultViewType=expanded&KWICView=false",
    def start_requests(self):

        yield SplashRequest(url="https://www.congress.gov/member/robert-aderholt/A000055?searchResultViewType=expanded&KWICView=false", callback=self.parse, endpoint="execute", args={'lua_source': self.script})


def parse(self, response):
   for resp in response.xpath("//div[@class='featured']/div[2]"):
       yield{
           'member': response.xpath("//div[@class='featured']/h1/text()").get(),
           'state': resp.xpath(".//table[@class='standard01 lateral01']/tbody/tr/td[1]]/text()").get(),
           'district': resp.xpath(".//table[@class='standard01 lateral01']/tbody/tr/td[2]/text()").get(),
           'InCongress': resp.xpath(".//table[@class='standard01 lateral01']/tbody/tr/td[3]/text()").get(),
           'party': resp.xpath(".//table[@class='standard01 nomargin']/tbody/tr[3]/td[1]/text()").get(),
           'website': resp.xpath(".//table[@class='standard01 nomargin']/tbody/tr[1]/td/a/@href[").get()

       }
