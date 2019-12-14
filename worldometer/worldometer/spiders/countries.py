# -*- coding: utf-8 -*-
import scrapy


class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['www.worldometers.info']
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        countries = response.xpath('//td/a')
        for country in countries:
            name = country.xpath('.//text()').get()
            link = country.xpath('.//@href').get()
            ''' To actually go to the link of each country you need to join the schema https with the link
            absolute_url = response.urljoin(link) BUT scrapy has a command to follow links. Also, the name of the
            country is needed in the response_country yield. To do this add the meta argument and set it to a dict 
            in the response.follow yield and also add name = response.request.meta['country_name']
            to response_country() this way you can add the country to the yield. Sooo...
            '''
            yield response.follow(url=link, callback=self.response_country, meta={'country_name': name})

    def response_country(self, response):
        name = response.request.meta['country_name']
        ''' The brackets around the rows xpath statement are to encapsulate that one table so it can be indexed'''
        rows = response.xpath("(//table[@class='table table-striped table-bordered table-hover table-condensed table-list'])[1]/tbody/tr")
        for row in rows:
            year = row.xpath('.//td[1]/text()').get()
            population = row.xpath('.//td[2]/strong/text()').get()
            yield {
                'country': name,
                'year': year,
                'population': population
            }
