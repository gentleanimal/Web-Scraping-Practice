import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class CongressSenateSpider(CrawlSpider):

    name = "congressSenate116"

    allowed_domains = ["www.congress.gov"]
    start_urls = ["https://www.congress.gov/members?pageSort=state&searchResultViewType=compact&KWICView=false&pageSize=50&q={%22congress%22:[%22116%22],%22chamber%22:%22Senate%22}"]

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//ol/li[@class='compact']/span/a"), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths="//div[@class='nav-pag-top']/div[@class='pagination']/a[@class='next']"),callback='parse_item', follow=True),
    )


    def parse_item(self, response):

        yield {
            'member': response.xpath("//div[@class='featured']/h1/text()").get(),
            'state': response.xpath("//table[1]/tbody/tr/td[1]/text()").get(),
            'InCongress': response.xpath("normalize-space(//table[1]/tbody/tr/td[3]/text())").get(),
            'party': response.xpath("//table[2]//tr[3]/td/text()").get(),
            'website': response.xpath("//table[2]//tr/td/a/@href").get(),
            'address': response.xpath("normalize-space(//table[2]//tr[2]/td/text())").get(),
            'phone': response.xpath("normalize-space(//table[2]//tr[2]/td/text()[2])").get()

        }
