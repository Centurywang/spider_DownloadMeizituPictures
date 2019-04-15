# spider_DownloadMeizituPictures
爬虫爬取妹子图并将图片下载

meiziSpider.py文件  获取套图名称及url地址并保存到json文件
downloadPic.py      读取保存的json文件循环获取套图内url地址并下载图片
注：为预防被检测ip，设置了延时，爬取速度较慢，可以通过添加代理进行多线程爬取，加快爬取速度

新增多线程代理下载图片

meizitu.py文件，该文件内创建爬虫类，使用多线程和添加代理来进行爬取，速度更快。
注：需要事先安装好redis数据库，并按照 https://github.com/Germey/ProxyPool 上的步骤操作。
最后运行该文件即可。