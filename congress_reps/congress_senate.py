import scrapy


class CongressSenateSpider(scrapy.Spider):

    name = "congressSenate"

    allowed_domains = ["www.congress.gov"]

    def start_requests(self):
        yield scrapy.Request(url="https://www.congress.gov/members?pageSort=state&searchResultViewType=compact&KWICView=false&q=%7B%22congress%22%3A%5B%22116%22%2C%22115%22%2C%22114%22%2C%22113%22%2C%22112%22%2C%22111%22%2C%22110%22%2C%22109%22%2C%22108%22%2C%22107%22%5D%2C%22chamber%22%3A%22Senate%22%7D&pageSize=100&page=1", callback=self.parse)

    def parse(self, response):
        for member in response.xpath("//ol/li[@class='compact']"):
            yield {
                'member': member.xpath(".//span/a/text()").get(),
                'state': member.xpath(".//div/div/span[1]/span/text()").get(),
                'party': member.xpath(".//div/div/span[2]/span/text()").get(),
                'InCongress': member.xpath(".//div/div/span[3]/span/ul/li[1]/text()").get()

            }

        next = response.xpath("//div[@class='nav-pag-top']/div[@class='pagination']/a[@class='next']/@href").get()
        if next is not None:
            next_page = response.urljoin(next)
            yield scrapy.Request(url=next_page, callback=self.parse)
