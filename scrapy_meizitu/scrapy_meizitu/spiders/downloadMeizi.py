# -*- coding: utf-8 -*-
import scrapy
import redis

class MeiziSpider(scrapy.Spider):
    '''获取套图url'''
    name = 'meizi_d'
    allowed_domains = ['mzitu.com']

    def start_requests(self):
        r = redis.Redis(password='wangshiji',host='localhost',port=6379,decode_responses=True)

        start_url = True
        while start_url is not None:
            # 从redis list 循环取出爬取url地址 作为开始url
            start_url = eval(r.lpop('meizi:items'))['url']
            yield scrapy.Request(url=start_url,callback=self.parse)

    def parse(self, response):
        # 图片地址
        img_url = response.xpath('//div[@class="main-image"]//img/@src').extract()
        item = {}
        item['image_urls'] = img_url
        item['name'] = response.xpath('//div[@class="currentpath"]//text()').extract()[-1][3:]
        print(item)
        yield item
        next_page_url = response.xpath('//a[./span/text()="下一页»"]/@href').extract_first()
        if next_page_url is not None:
            yield scrapy.Request(url=next_page_url,callback=self.parse)

