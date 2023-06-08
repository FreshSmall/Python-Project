import scrapy
from scrapy import Selector, Request
from scrapy.http import HtmlResponse

#from demo.demo.items import DemoItem

class DemoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    score = scrapy.Field()
    motto = scrapy.Field()


class DoubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["movie.douban.com"]
    start_urls = ["https://movie.douban.com/top250?start=0&filter="]

    def parse(self, response: HtmlResponse):
        sel = Selector(response)
        movie_items = sel.css('#content > div > div.article > ol > li')
        for movie_sel in movie_items:
            item = DemoItem()
            item['title'] = movie_sel.css('.title::text').extract_first()
            item['score'] = movie_sel.css('.rating_num::text').extract_first()
            item['motto'] = movie_sel.css('.inq::text').extract_first()
            yield item

        hrefs = sel.css('#content > div > div.article > div.paginator > a::attr("href")')
        for href in hrefs:
            full_url = response.urljoin(href.extract())
            yield Request(url=full_url)
