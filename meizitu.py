import requests
from lxml import etree
from time import sleep
import threading
import os

class Meizitu:
    '''多线程添加代理爬取妹子图'''
    def __init__(self):
        # 分类 性感、日本、台湾、清纯 要爬那哪个类型就选哪个
        self.index_urls = ['https://www.mzitu.com/xinggan/', 'https://www.mzitu.com/japan/', 'https://www.mzitu.com/taiwan/',
                      'https://www.mzitu.com/mm/']

    def get_proxy(self):
        '''获取代理'''
        # 在本地获取代理
        PROXY_POOL_URL = 'http://localhost:5000/get'
        try:
            response = requests.get(PROXY_POOL_URL)
            proxy = {
                "https": "http://{}".format(response.text)
            }
            if response.status_code == 200:
                return proxy
        except ConnectionError:
            return None

    def create_dictionary(self,name):
        '''创建文件夹'''
        try:
            os.mkdir(name)
        except Exception as e:
            print(e)

    def judge_file(self,filename):
        '''判断文件是否存在'''
        try:
            with open(filename) as f:
                pass
            return True
        except:
            return False

    def get_response(self,url, headers=None,proxy=None):
        '''获取response响应'''
        response = requests.get(url, headers=headers,proxies=proxy)
        return response

    def parse_html1(self,response):
        '''解析response内容获取套图名称及url地址'''
        # 创建文件夹
        self.create_dictionary('Pictures')
        html = etree.HTML(response.text)
        # 用于保存该页面套图名称及url地址
        page_img_urls = []
        # 套图名称及url地址保存在 class="postlist" 的div标签下的 ul标签下 li标签内
        page_img_content = html.xpath('//div[@class="postlist"]//ul//li')
        for img_content in page_img_content:
            # 用于保存单个套图名称及url地址
            img_info = {}
            # 套图名称在li标签下第一个a标签下的img标签的alt属性
            img_info['name'] = img_content.xpath('./a[1]/img/@alt')[0]
            # 套图url在li标签下的第一个a标签的href属性
            img_info['url'] = img_content.xpath('./a[1]/@href')[0]
            # 下载图片
            thread = threading.Thread(target=self.get_picture_url,args=(img_info['name'],img_info['url']))
            thread.start()
            sleep(2)
            page_img_urls.append(img_info)
        return page_img_urls


    def get_next_page_url(self,response):
        '''获取下一页url地址'''
        html = etree.HTML(response.text)
        next_page_url = html.xpath('//a[text()="下一页»"]/@href')
        # 判断下一页是否存在
        if len(next_page_url) > 0:
            return next_page_url[0]
        else:
            return None

    def get_picture_url(self,name, url):
        '''获取图片'''
        # 保存该套图所有url
        proxy = self.get_proxy()
        response = self.get_response(url,proxy=proxy)
        html = etree.HTML(response.text)
        # 获取图片url  url在class="main-image"的div标签下的img的src属性
        img_url = html.xpath('//div[@class="main-image"]//img/@src')[0]
        self.create_dictionary(name='Pictures/' + name)
        thread = threading.Thread(target=self.download_picture, args=(name, img_url))
        thread.start()
        try:
            # 获取下一页
            next_page_url = html.xpath('//a[./span/text()="下一页»"]/@href')[0]
            while next_page_url:
                print(next_page_url)
                response = self.get_response(next_page_url)
                html = etree.HTML(response.text)
                img_url = html.xpath('//div[@class="main-image"]//img/@src')[0]
                thread = threading.Thread(target=self.download_picture, args=(name, img_url))
                thread.start()
                # 获取下一页
                next_page_url = html.xpath('//a[./span/text()="下一页»"]/@href')[0]
        except Exception as e:
            print(e, '该套图保存结束')

    def download_picture(self,name,url):
        '''下载图片'''
        # 设置headers请求头，获得下载图片权限
        headers = {
            'Referer': 'https://www.mzitu.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
        }
        # 获取代理
        proxy = self.get_proxy()
        filename = 'Pictures/' + name + '/' + name + url[-8:]
        judge = self.judge_file(filename)
        if judge:
            print('文件{}已存在'.format(filename))
        else:
            img_content = self.get_response(url, headers=headers,proxy=proxy).content
            try:
                print(filename)
                with open(filename, 'wb') as f:
                    f.write(img_content)
                    # 设置延时
                    sleep(1)
            except Exception as e:
                print(e)


    def run(self):
        '''爬虫爬取妹子图图片（多线程，设置代理下载）
        1.获取首页response响应内容
        2.解析内容获取套图名称及url地址并下载（下载时多线程）
        3.获取下一页url地址
        4.循环获取下一页response响应内容
          解析内容获取套图名称及url地址并下载（下载时多线程）
        '''
        type_choice = eval(input('爬取妹子图图片url并保存的哦呵json文件：\n1.性感\t2.日本\t3.台湾\t4.清纯\n请选择：'))
        # 1.获取首页response响应内容
        response = self.get_response(self.index_urls[type_choice-1])
        # 2.解析内容获取套图名称及url地址
        self.parse_html1(response)
        # 3.获取下一页url地址
        next_page_url = self.get_next_page_url(response)
        # 4.获取下一页response响应内容 解析内容获取套图名称及url地址
        while next_page_url:
            print(next_page_url)
            # 设置延时 2秒 防止请求过于频繁
            sleep(2)
            # 1.获取response响应内容
            response = self.get_response(next_page_url)
            # 2.解析内容获取套图名称及url地址
            self.parse_html1(response)
            # 3.获取下一页url地址
            next_page_url = self.get_next_page_url(response)
        print('该类型保存完成')


if __name__ == '__main__':
    meizi = Meizitu()
    meizi.run()