###“用户也评论了这些应用” -- App Store跨App评论相关性分析脚本
不谈刷榜的问题了。只介绍一下这个脚本的用途和思路。
本脚本接收一个productID作为参数（iTunes里面链接的ID），并抓取所以评论此app的用户，他们也评论了哪些其它的app。最后按其它app作为key，数量作为value聚合。

###本脚本依赖BeautifulSoup, lxml, unicodecsv和gevent。以Ubuntu为例：
####安装lxml
    sudo apt-get install python-lxml
####安装[Beautiful Soap](http://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup)
我的ubuntu版本，需要手动下载[安装包](http://www.crummy.com/software/BeautifulSoup/bs4/download/4.0/beautifulsoup4-4.0.0b3.tar.gz)，之后执行：
    python setup.py install
####安装unicodecsv
    pip install unicodecsv
####安装[gevent](http://www.gevent.org/intro.html#installation)
	easy_install greenlet
	sudo apt-get install libevent
    sudo apt-get install python-gevent // For Ubuntu 10.04

###Mac版本安装，需要[HomeBrew](http://mxcl.github.com/homebrew/)：
    pip install beautifulsoup4
    brew install libevent
    pip install greenlet
    pip install lxml
    pip install unicodecsv

###使用方法
<pre>
usage: analyze.py [-h] [-p PRODUCT_ID] [-v] [-l] [-c COUNT] [-s STORE_ID]
                  [-w WORKER_COUNT]

optional arguments:
  -h, --help            show this help message and exit
  -p PRODUCT_ID, --product_id PRODUCT_ID
                        Required. ID for app in App Store
  -v, --verbose         show verbose log
  -l, --list            list all store ids.
  -c COUNT, --count COUNT
                        get the oldest ammount of pages of reviews, default is
                        10.
  -s STORE_ID, --store_id STORE_ID
                        country/region for app store, default is China.
  -w WORKER_COUNT, --worker_count WORKER_COUNT
                        concurrent worker count, default is 10.
</pre>

####如何阅读生成的csv文件
* 评论的相关数按降序排列
* only-self表示用户只评论过这个应用，没评论过任何其它应用（处女评）
* 如果App的名字为QQ 2012，则QQ 2012这行表示评论过QQ 2012的用户数量
* 上述两个值相加，即为总评论数
* 请注意生成文件的日期后缀，数据是有时效性的
* 一般首次上榜的应用，分析结果更有价值
* 分析结果作为猜测的辅助，不是充要条件

###Store IDs
<pre>
              Store               StoreID
              Brazil              143503
              Canada              143455
               Qatar              143498
          Kazakhstan              143517
      Czech Republic              143489
         Phillipines              143474
              Kuwait              143493
              Panama              143485
           Lithuania              143520
          Costa Rica              143495
          Luxembourg              143451
              France              143442
              Italia              143450
             Ireland              143449
           Argentina              143505
              Espana              143454
            Slovakia              143496
             Ecuador              143509
              Latvia              143519
              Israel              143491
           Australia              143460
           Nederland              143452
           Singapore              143464
         El Salvador              143506
              Norway              143457
           Venezuela              143502
          Osterreich              143445
      Schweiz/Suisse              143459
           Guatemala              143504
               China              143465
               Chile              143483
             Belgium              143446
            Thailand              143475
  Dominican Republic              143508
           Hong Kong              143463
             Lebanon              143497
           Indonesia              143476
             Jamaica              143511
             Denmark              143458
              Poland              143478
             Finland              143447
         Deutschland              143443
        Saudi Arabia              143479
              Turkey              143480
       United States              143441
            Paraguay              143513
              Sweden              143456
               Korea              143466
             Croatia              143494
               Malta              143521
               Japan              143462
             Uruguay              143514
         New Zealand              143461
             Moldova              143523
              Russia              143469
            Pakistan              143477
             Romania              143487
            Honduras              143510
             Estonia              143518
            Portugal              143453
              Mexico              143468
               Egypt              143516
United Arab Emirates              143481
        South Africa              143472
               India              143467
                Peru              143507
      United Kingdom              143444
            Malaysia              143473
             Vietnam              143471
            Slovenia              143499
            Colombia              143501
              Greece              143448
           Sri Lanka              143486
             Hungary              143482
              Taiwan              143470
           Nicaragua              143512
               Macau              143515
</pre>

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