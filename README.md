###“用户也评论了这些应用” -- App Store跨App评论相关性分析脚本
不谈刷榜的问题了。只介绍一下这个脚本的用途和思路。
本脚本接收一个productID作为参数（iTunes里面链接的ID），并抓取所以评论此app的用户，他们也评论了哪些其它的app。最后按其它app作为key，数量作为value聚合。

###本脚本依赖BeautifulSoup, lxml, unicodecsv和gevent。以Ubuntu为例：
####安装lxml
`sudo apt-get install python-lxml`
####安装[Beautiful Soap](http://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup)
我的ubuntu版本，需要手动下载[安装包](http://www.crummy.com/software/BeautifulSoup/bs4/download/4.0/beautifulsoup4-4.0.0b3.tar.gz)，之后执行：
    `python setup.py install`
####安装unicodecsv
    `pip install unicodecsv`
####安装[gevent](http://www.gevent.org/intro.html#installation)
	`easy_install greenlet`
	`sudo apt-get install libevent`
    `sudo apt-get install python-gevent` // For Ubuntu 10.04

###Mac版本安装，需要[HomeBrew](http://mxcl.github.com/homebrew/)：
    `brew install libevent`
    `pip install greenlet`

###使用
`python analyze.py <productID>`

###输出
根据指定的productID, 生成中国区该app的评论相关性csv格式的表格

###Known Issues
* 抓取用户评论的所有app，目前只抓取了第一页6个。最完整的结果应该抓取所有评论过的app，但请求至少会翻倍，而且“特殊”账号普通评论过的app不超过6个
* 代码不健壮，没有做异常处理并retry

###如何获得请求的地址：
* 使用tcpdump来监测iTunes请求的实际地址：`sudo tcpdump -s 0 -A -i en0 port 80`
* Inspired by [ReviewDownloadManager of AppSales](https://github.com/omz/AppSales-Mobile/blob/master/Classes/ReviewDownloadManager.h)

###Contribute
* Bug请提交到Issues
* 作者是python菜，请python熟的朋友帮助我改进代码及性能(可能有问题的地方，我已经用FIXIT标明；)
* 开发问题可联系ewangke at gmail.com

###Contributors
* [yuchao](https://github.com/yuchao), [用gevent多线程处理请求, 目前设置了10个](https://github.com/ewangke/CustomersAlsoReviewed-AppStore/commit/011adcbf74c814be77a8e3f2cdaba62720aa296e)

###Copyright
This script is FREE to use, copy or modifiy for both commercial and non-commercial purpose.