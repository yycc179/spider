
from scrapy.selector import Selector
from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


import scrapy
import sys

from ted.items import TedItem

# sys.stdout = open('output.txt', 'w')


class TedVideoSpider(CrawlSpider):
    name = 'Ted'
    allowed_domains = ['ted.com']
    start_urls = [
        "http://www.ted.com/talks?page=1",
    ]

    rules = (
        Rule(LinkExtractor(allow=('\?page=\d+$',)), callback='parse_video', follow=True),
        # Rule(LinkExtractor(allow=('/talks/', )), callback='parse_item'),
        # Rule(LinkExtractor(allow=('#searialinks$', )), callback='parse_play'),
    )

    def parse_item(self, response):
    # def parse(self, response):
        item = TedItem()
        item['link'] = response.url

        return item

    def parse_video(self, response):

        for i in response.xpath('//div[@class="media__image media__image--thumb talk-link__image"]'):
            item = TedItem()
            item['link'] = 'http://www.ted.com' + i.xpath('a/@href').extract()[0];
            item['img'] = i.xpath('//img/@src').extract()[0];
            item['duration'] = i.xpath('//span[@class="thumb__duration"]/text()').extract()[0];
            # print(item)
            yield item
