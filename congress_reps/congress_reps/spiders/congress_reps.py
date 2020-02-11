import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class CongressRepsSpider(CrawlSpider):

    name = "congressReps1"

    allowed_domains = ["www.congress.gov"]
    start_urls = ["https://www.congress.gov/members?pageSort=state&searchResultViewType=compact&KWICView=false&pageSize=100&q=%7B%22congress%22%3A%5B%22116%22%2C%22115%22%2C%22114%22%2C%22113%22%2C%22112%22%2C%22111%22%2C%22110%22%2C%22109%22%2C%22108%22%2C%22107%22%5D%2C%22chamber%22%3A%22House%22%7D"]

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//ol/li[@class='compact']/span/a"), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths="//div[@class='nav-pag-top']/div[@class='pagination']/a[@class='next']"),
             callback='parse_item', follow=True),
    )


    def parse_item(self, response):

        yield {
            'member': response.xpath("//h1/text()").get(),
            'state': response.xpath("//table[1]/tbody/tr/td[1]/text()").get(),
            'district': response.xpath("normalize-space(//table[1]/tbody/tr/td[2]/text())").get(),
            'InCongress': response.xpath("normalize-space(//table[1]/tbody/tr/td[3]/text())").get(),
            'party': response.xpath("//table[2]/tbody/tr[3]/td/text()").get(),
            'website': response.xpath("//table[2]/tbody/tr/td/a/@href").get(),
            'contact': response.xpath("//table[2]/tbody/tr[2]/td/text()").get(),

        }
