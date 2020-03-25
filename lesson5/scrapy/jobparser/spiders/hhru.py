# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?area=113&st=searchVacancy&text=python']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath(
            "//a[@class='bloko-button HH-Pager-Controls-Next HH-Pager-Control']/@href").extract_first()
        if next_page is None:
            yield
        yield response.follow(next_page, callback=self.parse)

        vac_list = response.xpath("//a[@class='bloko-link HH-LinkModifier']/@href").extract()

        for link in vac_list:
            yield response.follow(link, callback=self.vacansy_parse)

    def vacansy_parse(self, response: HtmlResponse):
        link = response.url
        name = response.xpath("//h1[@class='bloko-header-1']/text()").extract()[0]
        salary = response.xpath("//span[@class='bloko-header-2 bloko-header-2_lite']/text()").extract()
        yield JobparserItem(name=name, salary=salary, link=link)
