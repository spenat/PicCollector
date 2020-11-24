import scrapy
from scrapy.http import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import PicCollectorItem


class PicsSpider(CrawlSpider):
    name = 'pics'
    allowed_domains = ['old.reddit.com', 'imgur.com']

    def __init__(self, subreddit='pics', **kwargs):
        self.start_urls = [f'https://old.reddit.com/r/{subreddit}']

        self.rules = [
            Rule(LinkExtractor(allow=[f'.*/r/{subreddit}/\?count.*']),
                 callback='parse',
                 follow=False),
        ]
        super(PicsSpider, self).__init__(**kwargs)

    def parse_commentpage(self, response):
        description = " ".join(response.url.split('/')[-2].split('_')).title()
        real_link = response.xpath('//a[@class="may-blank"]').xpath('@href').extract()
        item = PicCollectorItem()
        item['description'] = description
        item['image_urls'] = real_link
        yield item

    def parse(self, response):
        links = response.xpath('//a[@data-event-action="comments"]')
        no_links = len(links)
        urls = []
        for a in links:
            url = a.attrib['href']
            yield Request(url, callback=self.parse_commentpage)
