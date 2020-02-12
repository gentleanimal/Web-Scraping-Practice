import scrapy


class CongressSenateSpider(scrapy.Spider):

    name = "senate107-116"

    allowed_domains = ["www.congress.gov"]

    start_urls = ["https://www.congress.gov/members?pageSort=state&searchResultViewType=compact&KWICView=false&q=%7B%22congress%22%3A%5B%22116%22%2C%22115%22%2C%22114%22%2C%22113%22%2C%22112%22%2C%22111%22%2C%22110%22%2C%22109%22%2C%22108%22%2C%22107%22%5D%2C%22chamber%22%3A%22Senate%22%7D&pageSize=50&page=1"]

    def parse(self, response):

        for senator in response.xpath("//ol/li[@class='compact']"):

            yield {
                'member': senator.xpath(".//span/a/text()").get(),
                'state': senator.xpath(".//div[starts-with(@class, 'member-profile')]/span[1]/span/text()").get(),
                'party': senator.xpath(".//div[starts-with(@class, 'member-profile')]/span[2]/span/text()").get(),
                'InCongress': senator.xpath(".//div[starts-with(@class, 'member-profile')]/span[3]/span/ul/li/text()").getall(),

            }
        next_page = response.selector.xpath("//div[@class='pagination']/a[@class='next']/@href").extract_first()

        if next_page is not None:
            next = response.urljoin(next_page)
            yield scrapy.Request(url=next, callback=self.parse)
