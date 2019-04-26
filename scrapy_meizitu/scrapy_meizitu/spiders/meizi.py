# -*- coding: utf-8 -*-
import scrapy


class MeiziSpider(scrapy.Spider):
    '''获取套图url并存入redis 数据库(数据类型list)'''
    name = 'meizi'
    allowed_domains = ['mzitu.com']
    # 四个分类
    start_urls = ['https://www.mzitu.com/xinggan/','https://www.mzitu.com/japan/','https://www.mzitu.com/taiwan/','https://www.mzitu.com/mm/']

    def parse(self, response):

        page_img_content = response.xpath('//div[@class="postlist"]//ul//li')

        for img_content in page_img_content:
            # 用于保存单个套图url地址
            item = {}
            # 套图url在li标签下的第一个a标签的href属性
            item['url'] = img_content.xpath('./a[1]/@href').extract_first()
            yield item

        # 获取下一页
        next_page_url = response.xpath('//a[text()="下一页»"]/@href').extract_first()
        if next_page_url is not None:
            yield scrapy.Request(
                url=next_page_url,
                callback=self.parse
            )



