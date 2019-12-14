import scrapy


class GdpdebtSpider(scrapy.Spider):
    name = 'gdp_debt'
    allowed_domains = ["worldpopulationreview.com/countries/countries-by-national-debt"]
    start_urls = ["http://worldpopulationreview.com/countries/countries-by-national-debt/"]

    def parse(self, response):
        rows = response.xpath("//table[@class='table table-striped']/tbody/tr")
        for row in rows:
            name = row.xpath('.//td/a/text()').get()
            gdp_debt = row.xpath('.//td[2]/text()').get()
            population = row.xpath('.//td[3]/text()').get()
            yield {
                'country_name': name,
                'gdp_debt': gdp_debt,
                'population': population
            }
