import scrapy
from scrapy.http.response import Response
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request

class OlxSpider(scrapy.Spider):
    name = 'olx'
    allowed_domains = ["olx.com.br"]

    def __init__(self, state="sc", region="florianopolis-e-regiao", category="audio-tv-video-e-fotografia", subcategory="tvs", search="tv%2060", *args, **kwargs):
        super(OlxSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f'https://{state}.olx.com.br/{region}/{category}/{subcategory}?q={search}&sf=1']
        self.link_extractor = LinkExtractor(f'https://{state}.olx.com.br/{region}/{category}/.*-\d+')


    def parse(self, response):
        for link in self.link_extractor.extract_links(response):
            yield Request(link.url, callback=self.parse_item)

    def parse_item(self, response:Response):
        yield {
                'link': response.url,
                'title': response.css("h1::text").get(),
                'price': response.css("h2::text").get(),
                'date': response.css("span").re_first("\d{2}/\d{2} às \d{2}:\d{2}")
            }

