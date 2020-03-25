# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['russia.superjob.ru']
    start_urls = ['https://russia.superjob.ru/vacancy/search/?keywords=python']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[contains(@class,'dalshe')]/@href").extract_first()
        if next_page is None:
            yield
        yield response.follow(next_page, callback=self.parse)

        vac_list = response.xpath("//a[contains(@href,'vakansii')]/@href").extract()

        for link in vac_list:
            yield response.follow(link, callback=self.vacansy_parse)

    def vacansy_parse(self, response: HtmlResponse):
        link = response.url
        name = response.xpath("//h1[@class='_3mfro rFbjy s1nFK _2JVkc']/text()").extract()[0]
        salary = response.xpath("//span[@class='_3mfro _2Wp8I ZON4b PlM3e _2JVkc']/text()").extract()
        yield JobparserItem(name=name, salary=salary, link=link)
