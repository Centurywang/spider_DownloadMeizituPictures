import json
import os
from lxml import etree
from time import sleep
from spider import get_response
from spider import r

def judge_file(filename):
    '''判断文件是否存在
    存在返回True
    不存在返回False
    '''
    try:
        with open(filename) as f:
            pass
        return True
    except:
        return False


def create_dictionary(name):
    '''创建文件夹'''
    try:
        os.mkdir(name)
    except Exception as e:
        print(e)

def download_picture(name,url):
    '''下载图片'''
    # 设置headers请求头，获得下载图片权限
    headers = {
        'Referer': 'https://www.mzitu.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }
    filename = 'Pictures/'+name+'/'+name+url[-8:]
    judge = judge_file(filename)
    if judge:
        print('文件{}已存在'.format(filename))
    else:
        img_content = get_response(url,headers=headers).content
        try:
            print(filename)
            with open(filename,'wb') as f:
                f.write(img_content)
        except Exception as e:
            print(e)

def get_picture_url(name,url):
    '''获取图片'''
    response = get_response(url)
    html = etree.HTML(response.text)
    # 获取图片url  url在class="main-image"的div标签下的img的src属性
    img_url = html.xpath('//div[@class="main-image"]//img/@src')[0]
    # 下载图片到已创建文件夹下
    download_picture(name,url=img_url)
    try:
        # 获取下一页
        next_page_url = html.xpath('//a[./span/text()="下一页»"]/@href')[0]
        while next_page_url:
            print(next_page_url)
            response = get_response(next_page_url)
            html = etree.HTML(response.text)
            img_url = html.xpath('//div[@class="main-image"]//img/@src')[0]
            download_picture(name, url=img_url)
            # 获取下一页
            next_page_url = html.xpath('//a[./span/text()="下一页»"]/@href')[0]
    except Exception as e:
        print(e,'该套图保存结束')


def run():
    '''下载图片(从机)
    1.读取redis集合内url数据
    2.  根据name属性创建文件夹
        请求套图url地址获取response响应并获取图片url地址
        下载图片
        循环获取下一页并下载图片
    '''

    # 创建Picture文件夹
    create_dictionary(name='Pictures')
    # 从redis数据库获取url数据
    url = r.spop('meizitu_urls')
    # 2.循环数据
    while url:
        data = eval(url)
        print(data)
        # 根据name属性创建文件夹
        create_dictionary(name='Pictures/'+data['name'])
        # 循环套图内页面 获取url地址 并下载图片
        get_picture_url(name=data['name'],url=data['url'])
        url = r.spop('meizitu_urls')

if __name__ == '__main__':
    run()