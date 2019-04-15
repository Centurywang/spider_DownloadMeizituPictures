import requests
from lxml import etree
from time import sleep
import json

def get_response(url,headers=None):
    '''获取response响应'''
    response = requests.get(url,headers=headers)
    return response

def parse_html1(response):
    '''解析response内容获取套图名称及url地址'''
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
        page_img_urls.append(img_info)
    print(page_img_urls)
    return page_img_urls

def get_next_page_url(response):
    '''获取下一页url地址'''
    html = etree.HTML(response.text)
    next_page_url = html.xpath('//a[text()="下一页»"]/@href')
    # 判断下一页是否存在
    if len(next_page_url)>0:
        return next_page_url[0]
    else:
        return None

def save_to_file(filename,data):
    '''保存数据到json文件'''
    data = json.dumps(data)
    filename = filename+'.json'
    with open(filename,'w') as f:
        print('正在保存{}'.format(filename))
        f.write(data)
    print('保存完成')




def run():
    '''爬虫爬取妹子图图片
    1.获取首页response响应内容
    2.解析内容获取套图名称及url地址
    3.获取下一页url地址
    4.循环获取下一页response响应内容
      解析内容获取套图名称及url地址
    5.将所获得的套图名称及url地址存入json文件（用于下载图片时使用）
    '''
    # 分类 性感、日本、台湾、清纯 要爬那哪个类型就选哪个
    index_urls = ['https://www.mzitu.com/xinggan/','https://www.mzitu.com/japan/','https://www.mzitu.com/taiwan/','https://www.mzitu.com/mm/']
    # 此处选的是性感类型
    index_url = 'https://www.mzitu.com/xinggan/'
    # 用于保存所有套图名称及url地址
    all_img_info = []
    # 1.获取首页response响应内容
    response = get_response(index_url)
    # 2.解析内容获取套图名称及url地址
    all_img_info.extend(parse_html1(response))
    # 3.获取下一页url地址
    next_page_url = get_next_page_url(response)
    # 4.获取下一页response响应内容 解析内容获取套图名称及url地址
    while next_page_url:
        print(next_page_url)
        # 设置延时 2秒 防止请求过于频繁
        sleep(2)
        # 1.获取response响应内容
        response = get_response(next_page_url)
        # 2.解析内容获取套图名称及url地址
        all_img_info.extend(parse_html1(response))
        # 3.获取下一页url地址
        next_page_url = get_next_page_url(response)
    print('爬取完成，供%d条数据'%len(all_img_info))
    # 5.保存到json文件
    # 注意：如果要爬不同类型的要修改filename变量，防止覆盖掉原来保存的json文件
    save_to_file(filename='meizi',data=all_img_info)


if __name__ == '__main__':
    run()