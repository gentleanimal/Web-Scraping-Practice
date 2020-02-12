import scrapy

class CongressHouseRepsSpider(scrapy.Spider):

    name = "congressReps"

    allowed_domains = ["www.congress.gov"]

    start_urls = ["https://www.congress.gov/members?pageSort=state&searchResultViewType=compact&KWICView=false&pageSize=100&q={%22congress%22:[%22116%22,%22115%22,%22114%22,113],%22chamber%22:%22House%22}"]

    def parse(self, response):
        urls = response.xpath("//div[@id='main']/ol/li[@class='compact']/span/a/@href").extract()
        for url in urls:
           yield response.follow(url=url, callback=self.parse_items)

    def parse_items(self, response):
        yield {
            'member': response.xpath("//div[@class='featured']/h1/text()").get(),
            'state': response.xpath("//table[@class='standard01 lateral01']/tbody/tr/td[1]/text()").get(),
            'district': response.xpath("normalize-space(//table[@class='standard01 lateral01']/tbody/tr/td[2]/text())").get(),
            'InCongress': response.xpath("normalize-space(//table[@class='standard01 lateral01']/tbody/tr/td[3]/text())").get(),
            'party': response.xpath("//table[@class='standard01 nomargin']/tbody/tr[3]/td/text()").get(),
            'website': response.xpath("//table[@class='standard01 nomargin']/tbody/tr[1]/td/a/@href").get(),
            'address': response.xpath("normalize-space(//table[@class='standard01 nomargin']/tbody/tr[2]/td/text()[1])").get(),
            'phone': response.xpath("normalize-space(//table[@class='standard01 nomargin']/tbody/tr[2]/td/text()[2])").get(),

        }
