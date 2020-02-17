import scrapy
import time


class CongressHouseRepsSpider(scrapy.Spider):

    name = "congressReps"

    allowed_domains = ["www.congress.gov"]

    start_urls = ["https://www.congress.gov/members?pageSort=state&searchResultViewType=compact&KWICView=false&pageSize=100&q={%22congress%22:[%22116%22,%22115%22,%22114%22,113],%22chamber%22:%22House%22}"]

    def parse(self, response):
        urls = response.xpath("//div[@id='main']/ol/li[@class='compact']/span/a/@href").extract()
        for url in urls:
            #  100 per page
            yield response.follow(url=url, callback=self.parse_items)

        # next_page = response.selector.xpath("//div[@class='pagination']/a[@class='next']/@href").extract_first()
        #
        # if next_page is not None:
        #     next = response.urljoin(next_page)
        #     yield scrapy.Request(url=next, callback=self.parse)

    def parse_items(self, response):
        current_url = response.request.url
        yield {
            'member': response.xpath("//div[@class='featured']/h1/text()").get(),
            'state': response.xpath("//table[@class='standard01 lateral01']/tbody/tr/td[1]/text()").get(),
            'district': response.xpath("normalize-space(//table[@class='standard01 lateral01']/tbody/tr/td[2]/text())").get(),
            'InCongress': response.xpath("normalize-space(//table[@class='standard01 lateral01']/tbody/tr/td[3]/text())").get(),
            'party': response.xpath("//div[contains(@class, 'member_profile')]/table[@class='standard01 nomargin']/tbody/tr[3]/td").get(),
            'website': response.xpath("//div[contains(@class, 'member_profile')]/table[@class='standard01 nomargin']/tbody/tr[1]/td/a/@href").get(),
            'address': response.xpath("normalize-space(//div[contains(@class, 'member_profile')]/table[@class='standard01 nomargin']/tbody/tr[2]/td/text()[1])").get(),
            'phone': response.xpath("normalize-space(//div[contains(@class, 'member_profile')]/table[@class='standard01 nomargin']/tbody/tr[2]/td/text()[2])").get(),

        }
        time.sleep(2)
        print(current_url)
#        yield scrapy.Request(url=current_url, self.parse_bills)
#        def parse_bills(self, response):
        for bill in response.xpath("//div[@id='main']/ol/li[@class='compact']"):
            #  100 per page
             yield {
                 'sectionTitle': response.xpath("//div[@class='main-wrapper']/h2/text()").get(),
                 'Legislation': bill.xpath("normalize-space(.//span/a/text())").getall(),
                 'title': bill.xpath(".//span[2]/text()").get(),
                 'sponser': bill.xpath("normalize-space(.//span/span/a/text())").getall(),
                 'committiees': bill.xpath(".//span[@class='result-item'][2]/span/text()").get(),
                 'Latest_Action': bill.xpath(".//span[@class='result-item'][3]/span/text()[1]").get(),

             }

#         next_page = response.selector.xpath("//div[@class='pagination']/a[@class='next']/@href").extract_first()
#
#         if next_page is not None:
#             next = response.urljoin(next_page)
#             yield scrapy.Request(url=next, callback=self.parse_bills)
