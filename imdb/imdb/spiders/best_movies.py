# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = 'best_movies'
    allowed_domains = ['imdb.com']
#    start_urls = ['https://www.imdb.com/search/title/?groups=top_250&sort=user_rating']
# Adding User_Agent and functions start_requests, set_user_agent and added to parse_item 'user_agent'
#  Added process_request to the Rules
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome' \
                 '/77.0.3865.120 Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(url='https://www.imdb.com/search/title/?groups=top_250&sort=user_rating', headers={
            'User-Agent': self.user_agent
        })


    rules = (
        Rule(LinkExtractor(restrict_xpaths="//div[@class='lister-item-content']/h3/a"), callback='parse_item', follow=True, process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths="(//a[@class='lister-page-next next-page'])[2]"), process_request='set_user_agent')
    )

    def set_user_agent(self, request):
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_item(self, response):
        # link = response.request.meta['mlink']
        # length = response.xpath("//div[@class='subtext']/time/text()").get()
        # mlength = length.replace('/n', "").strip()

        yield{
            'title': response.xpath("//h1/text()[1]").get(),
            'year': response.xpath("//h1/span/a/text()").get(),
            'rating': response.xpath("//span[@itemprop='ratingValue']/text()").get(),
            'duration': response.xpath("normalize-space(//div[@class='subtext']/time/text())").get(), # gets rid of spaces & /n
            'genre': response.xpath("//div[@class='subtext']/a[1]/text()").get(),
            'movie_url': response.url,  # link
            'user_agent': str(response.request.headers['User-Agent'])
        }
    # Below is another way to get the movie_url just to show the use of
    # response.follow(url=url, callback=self.parse_item, meta={'mlink': url})
    # def parse(self, response):
    #     base_url = "https://www.imdb.com"
    #     links = response.xpath("//tr/td[@class='titleColumn']/a")
    #     for link in links:
    #         murl = link.xpath(".//@href").get()
    #         url = base_url + murl
    #         yield response.follow(url=url, callback=self.parse_item, meta={'mlink': url})
