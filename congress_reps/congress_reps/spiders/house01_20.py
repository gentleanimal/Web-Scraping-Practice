import scrapy


class CongressHouseSpider(scrapy.Spider):

    name = "house107-116"

    allowed_domains = ["www.congress.gov"]

    start_urls = ["https://www.congress.gov/members?pageSort=state&searchResultViewType=compact&KWICView=false&pageSize=100&q={%22congress%22:[%22116%22,%22115%22,%22114%22,%22113%22,%22112%22,%22111%22,%22110%22,%22109%22,%22108%22,%22107%22],%22chamber%22:%22House%22}"]

    def parse(self, response):

        for house in response.xpath("//ol/li[@class='compact']"):

            yield {
                'member': house.xpath(".//span/a/text()").get(),
                'state': house.xpath(".//div/div[starts-with(@class, 'member-profile')]/span[1]/span/text()").get(),
                'party': house.xpath("normalize-space(//div[starts-with(@class, 'member-profile')]/span/span[starts-with(text(), 'Republican') or starts-with(text(), 'Democratic') or starts-with(text(), 'Independent')])").get(),
                'InCongress': house.xpath(".//div[starts-with(@class, 'member-profile')]//ul[@class='member-served']/li/text()").getall(),
            }
        next_page = response.selector.xpath("//div[@class='pagination']/a[@class='next']/@href").extract_first()

        if next_page is not None:
            next = response.urljoin(next_page)
            yield scrapy.Request(url=next, callback=self.parse)
