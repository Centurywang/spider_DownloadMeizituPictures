# spider_DownloadMeizituPictures
爬虫爬取妹子图并将图片下载

推荐使用**optional_page_crawler**文件夹的爬虫(可选类型和页面)
下面代码已经过时  
1.简单爬取(simple_crawler文件夹)

meiziSpider.py文件  获取套图名称及url地址并保存到json文件
downloadPic.py      读取保存的json文件循环获取套图内url地址并下载图片
 注：为预防被检测ip，设置了延时，爬取速度较慢，可以通过添加代理进行多线程爬取，加快爬取速度

2.多线程代理下载图片(multithreaded_proxy_crawler文件夹)

meizitu.py文件，该文件内创建爬虫类，使用多线程和添加代理来进行爬取，速度更快。
  注：需要事先安装好redis数据库，并按照 https://github.com/Germey/ProxyPool 上的步骤操作。
最后运行该文件即可。

3.分布式爬取(利用redis数据库;distributed_crawler文件夹)

spider.py 从网站获取所有套图name和url并存入redis数据库集合内(只需要在一台节点运行)
slave_spider.py 从redis数据库集合内获取套图name以及url，爬取该套图内所有图片并下载(用于在从节点上运行)
  注：实现原理：redis的集合类型，保存name和url时不会重复，取出数据时使用spop命令(随即删除一个数据并返回)

4.scrapy 分布式爬取 
说明： http://centuryw.cn/index.php/2019/04/26/scrapy%E7%88%AC%E5%8F%96%E5%A6%B9%E5%AD%90%E5%9B%BE%E5%88%86%E5%B8%83%E5%BC%8F/

