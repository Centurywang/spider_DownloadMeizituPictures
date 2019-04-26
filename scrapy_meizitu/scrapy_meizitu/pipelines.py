# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline


class ScrapyMeizituPipeline(object):
    def process_item(self, item, spider):
        return item

class ImagesrenamePipeline(ImagesPipeline):
    '''保存图片'''
    def get_media_requests(self, item, info):
        headers = {
            'Referer': 'https://www.mzitu.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
        }
        # 循环每一张图片地址下载，若传过来的不是集合则无需循环直接yield
        for image_url in item['image_urls']:
            # meta里面的数据是从spider获取，然后通过meta传递给下面方法：file_path
            yield scrapy.Request(image_url,headers=headers, meta={'name': item['name']})

    # 重命名，若不重写这函数，图片名为哈希，就是一串乱七八糟的名字
    def file_path(self, request, response=None, info=None):
        # 提取url前面名称作为图片名。
        image_guid = request.url[-8:]
        # 接收上面meta传递过来的图片名称
        name = request.meta['name']
        # 分文件夹存储的关键：{0}对应着name；{1}对应着image_guid
        filename = u'{0}/{1}'.format(name, image_guid)
        print(filename)
        return filename