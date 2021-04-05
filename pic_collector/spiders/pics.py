import scrapy
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import PicCollectorItem

cookie = {
    'edgebucket': 'dummy',
    'reddaid': 'dummy',
    'eu_cookie_v2': '3',
    'over18': '1'
}


class PicsSpider(CrawlSpider):
    name = 'pics'
    allowed_domains = ['old.reddit.com', 'imgur.com']

    def __init__(self, subreddit='pics', follow=False, **kwargs):
        self.start_urls = [f'https://old.reddit.com/r/{subreddit}']
        follow = follow == 'True'
        self.rules = [
            Rule(LinkExtractor(allow=[f'.*/r/{subreddit}/\?count.*']),
                 callback='parse',
                 follow=follow),
        ]
        super(PicsSpider, self).__init__(**kwargs)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, cookies=cookie)

    def parse_commentpage(self, response):
        description = " ".join(response.url.split('/')[-2].split('_')).title()
        real_link = response.xpath('//a[@class="may-blank"]').xpath(
            '@href').extract()
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
            yield Request(url, callback=self.parse_commentpage, cookies=cookie)
