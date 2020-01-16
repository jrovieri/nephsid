# -*- coding: utf-8 -*-
from scrapy.http import Request
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders.crawl import Rule, CrawlSpider
from nephila.items import DefaultItemLoader, Recipe


"""
class DefaultNephilaSpider(CrawlSpider):
    name = 'default'

    def __init__(self, *a, **kw):
        super(DefaultNephilaSpider, self).__init__(*a, **kw)
        spider = dns.objects(identifier=self.name).get()

        self.url = spider.url
        self.subject = spider.subject
        self.identifier = spider.identifier
        self.language = spider.language
        self.start_urls = spider.start_urls
        self.allowed_domains = spider.allowed_domains

        rules = list()
        for item in spider.rules:
            le = item.link_extractor
            link_extractor = LinkExtractor(allow=le.allow,
                deny=le.deny,
                allow_domains=le.allow_domains,
                deny_domains=le.deny_domains,
                deny_extensions=le.deny_extensions,
                restrict_xpaths=le.restrict_xpaths,
                restrict_css=le.restrict_css,
                tags=le.tags,
                attrs=le.attrs,
                canonicalize=le.canonicalize,
                unique=le.unique,
                process_value=le.process_value,
                strip=le.strip)

            rule = Rule(link_extractor=link_extractor,
                callback=item.callback,
                cb_kwargs=item.cb_kwargs,
                follow=item.follow)

            rules.append(rule)

        self.rules = tuple(rules)
        self.fields = spider.fields

        super(DefaultNephilaSpider, self)._compile_rules()

    def parse_start_url(self, response):
        return Request(response.url)

    def parse_category(self, response):
        yield Request(response.url)

    def parse_item(self, response):
        item = ItemLoader(item=self.item_to_load(), response=response)

        item.add_value('url', response.url)
        item.add_value('isPartOf', self.url)

        for field in self.fields:
            if field.value:
                item.add_value(field.name, field.value)
            else:
                item.add_xpath(field.name, field.selector)

        return item.load_item()
"""

class RecipeCrawlSpider0(CrawlSpider):
    name = 'gshow'

    allow_domains = ['gshow.globo.com']
    start_urls = ['https://gshow.globo.com/receitas-gshow/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths=("//div[@class='load-more gui-color-primary-bg']",),),
            callback='parse_category',
            follow=True),
        Rule(LinkExtractor(allow=("/receitas/",),),
            callback='parse_item',
            follow=False)
    )

    def parse_category(self, response):
        yield Request(response.url)

    def parse_item(self, response):
        item = DefaultItemLoader(item=Recipe(), response=response)

        item.add_xpath('dateModified', "//time[@itemprop='dateModified']/@datetime")
        item.add_xpath('datePublished', "//time[@itemprop='datePublished']/@datetime")
        item.add_xpath('description', "//meta[@name='description']/@content")
        item.add_xpath('image', "//meta[@itemprop='image']/@content")
        item.add_xpath('language', "//html/@lang")
        item.add_xpath('name', "//meta[@name='title']/@content")
        item.add_xpath('recipeIngredient', "//li[@itemprop='recipeIngredient']/text()")
        item.add_xpath('recipeInstructions', "//li[@itemprop='recipeInstructions']/text()")
        item.add_xpath('url', "//link[@rel='canonical']/@href")

        return item.load_item()
