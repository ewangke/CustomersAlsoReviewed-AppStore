"""
Find what customers also reviewed based on a centain app, specifically in China App Store
First version by ewangke at gmail.com
"""
import urllib2
from bs4 import BeautifulSoup
import unicodecsv
from gevent import monkey
monkey.patch_all()
import gevent
from gevent.queue import Queue
import datetime
import argparse
import sys

appStores = {
'Argentina':            143505,
'Australia':            143460,
'Belgium':              143446,
'Brazil':               143503,
'Canada':               143455,
'Chile':                143483,
'China':                143465,
'Colombia':             143501,
'Costa Rica':           143495,
'Croatia':              143494,
'Czech Republic':       143489,
'Denmark':              143458,
'Deutschland':          143443,
'El Salvador':          143506,
'Espana':               143454,
'Finland':              143447,
'France':               143442,
'Greece':               143448,
'Guatemala':            143504,
'Hong Kong':            143463,
'Hungary':              143482,
'India':                143467,
'Indonesia':            143476,
'Ireland':              143449,
'Israel':               143491,
'Italia':               143450,
'Korea':                143466,
'Kuwait':               143493,
'Lebanon':              143497,
'Luxembourg':           143451,
'Malaysia':             143473,
'Mexico':               143468,
'Nederland':            143452,
'New Zealand':          143461,
'Norway':               143457,
'Osterreich':           143445,
'Pakistan':             143477,
'Panama':               143485,
'Peru':                 143507,
'Phillipines':          143474,
'Poland':               143478,
'Portugal':             143453,
'Qatar':                143498,
'Romania':              143487,
'Russia':               143469,
'Saudi Arabia':         143479,
'Schweiz/Suisse':       143459,
'Singapore':            143464,
'Slovakia':             143496,
'Slovenia':             143499,
'South Africa':         143472,
'Sri Lanka':            143486,
'Sweden':               143456,
'Taiwan':               143470,
'Thailand':             143475,
'Turkey':               143480,
'United Arab Emirates': 143481,
'United Kingdom':       143444,
'United States':        143441,
'Venezuela':            143502,
'Vietnam':              143471,
'Japan':                143462,
'Dominican Republic':   143508,
'Ecuador':              143509,
'Egypt':                143516,
'Estonia':              143518,
'Honduras':             143510,
'Jamaica':              143511,
'Kazakhstan':           143517,
'Latvia':               143519,
'Lithuania':            143520,
'Macau':                143515,
'Malta':                143521,
'Moldova':              143523,
'Nicaragua':            143512,
'Paraguay':             143513,
'Uruguay':              143514
}

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--product_id", help="Required. ID for app in App Store")
parser.add_argument("-v", "--verbose", help="show verbose log", action="store_true")
parser.add_argument("-l", "--list", help="list all store ids.", action="store_true")
parser.add_argument("-c", "--count", help="get the oldest ammount of pages of reviews, default is all pages.", type=int, default=sys.maxint)
parser.add_argument("-s", "--store_id", help="country/region for app store, default is China.", default='143465')
parser.add_argument("-w", "--worker_count", help="concurrent worker count, default is 10.", type=int, default=10)
args = parser.parse_args()

should_list_stores = args.list
if should_list_stores:
    print '%20s%20s' % ("Store", "StoreID")
    for key in appStores:
        print "%20s%20s" % (key, appStores[key])
    exit(0)

verbose = args.verbose
page_limit = args.count
store_id = args.store_id
worker_count = args.worker_count
product_id = args.product_id
#print product_id
#print verbose
#print count
#print store_id
#print worker_count
#print should_list_stores

if product_id is None:
    print 'product_id is required. Use the -p parameter'
    exit(0)

# 143465(China) is the store ID, I don't know -1,12 means
# To check all other store ids, see https://github.com/grych/AppStoreReviews/blob/master/AppStoreReviews.py
store_front = '%s-1,12' % store_id
userAgent = 'iTunes/10.1.1 (Macintosh; Intel Mac OS X 10.6.5) AppleWebKit/533.19.4'     # Change your user agent if u want
relations = {}  # key: App Name, value: count
links = []  # links for reviewers
relations['only-self'] = 0
tasks = Queue()


def page_worker(pid):
    while not tasks.empty():
        task = tasks.get()
        if verbose:
            print('Page_worker %s got page with number %s' % (pid, task))
        processPage(task)

    print('Page_worker %s done!' % pid)


def reviewer_worker(pid):
    while not tasks.empty():
        task = tasks.get()
        if verbose:
            print('Reviewer_worker %s got reviewer link %s' % (pid, task))
        processReviewerLink(task)

    print('Reviewer_worker %s done!' % pid)


def processPage(page):
    result = []

    url = "http://itunes.apple.com/WebObjects/MZStore.woa/wa/customerReviews?s=%s&id=%s&displayable-kind=11&page=%d&sort=4" % (store_front, product_id, page)
    req = urllib2.Request(url, headers={"X-Apple-Store-Front": store_front, "User-Agent": userAgent})

    # Handle possible network exception
    while True:
        try:
            u = urllib2.urlopen(req, timeout=15)
            break
        except:
            print 'Fail to get %s' % url

    soup = BeautifulSoup(u.read(), "lxml")
    all_reviews = soup.find("div", {"class": "paginate all-reviews"})
    if all_reviews:
        reviewers = all_reviews.findAll("a", {"class": "reviewer"})
        result = [link['href'] for link in reviewers]
    if result != []:
        links.extend(result)
    if verbose:
        print 'Get reviewers: Page %d processed' % page


def processReviewerLink(link):
    # FIXIT: we only handle the first page review here
    reviewer_id = link.replace('http://itunes.apple.com/WebObjects/MZStore.woa/wa/viewUsersUserReviews?userProfileId=', '')
    reviewer_url = "http://itunes.apple.com//WebObjects/MZStore.woa/wa/allUserReviewsForReviewerFragment?userProfileId=%s&page=1&sort=14" % reviewer_id
    req = urllib2.Request(reviewer_url, headers={"X-Apple-Store-Front": store_front, "User-Agent": userAgent})

    # Handle possible network exception
    while True:
        try:
            u = urllib2.urlopen(req, timeout=15)
            break
        except:
            print 'Fail to get %s' % reviewer_url

    soup = BeautifulSoup(u.read(), "lxml")
    nodes = soup.findAll("div", {"class": "lockup small detailed option application"})

    if nodes is None:
        print 'Oops! %s has no reviews' % reviewer_id
        return

    if len(nodes) == 1:
        relations['only-self'] += 1
    else:
        for node in nodes:
            app_name = node.find("li", {"class": "name"}).contents[0].contents[0]
            if app_name in relations:
                relations[app_name] += 1
            else:
                relations[app_name] = 1


def analyze(product_id):
    page_count = get_reviews_page_count(product_id)
    for page_number in xrange(1, page_count + 1):
        tasks.put_nowait(page_number)
    gevent.joinall([gevent.spawn(page_worker, i) for i in xrange(worker_count)])

    reviewer_count = len(links)
    print 'Finish getting reviewers: %d reviewers found.' % reviewer_count

    for link in links:
        tasks.put_nowait(link)
    gevent.joinall([gevent.spawn(reviewer_worker, i) for i in xrange(worker_count)])

    #for k in relations:
    #    print "%s\t%s\n" % (k.encode('utf-8'), relations[k])
    output_filename = get_app_title(product_id)
    sorted_relations = sorted(relations.items(), key=lambda relations: relations[1], reverse=True)
    csv_writer = unicodecsv.writer(open('%s-%s.csv' % (output_filename.encode('utf-8'), str(datetime.date.today())), 'w'), encoding='utf-8')
    for relation in sorted_relations:
        csv_writer.writerow(relation)


def get_reviews_page_count(product_id):
    # TODO: get pages count
    url = "http://itunes.apple.com/WebObjects/MZStore.woa/wa/customerReviews?s=%s&id=%s&displayable-kind=11&page=%d&sort=4" % (store_front, product_id, 1)
    req = urllib2.Request(url, headers={"X-Apple-Store-Front": store_front, "User-Agent": userAgent})
    while True:
        try:
            u = urllib2.urlopen(req, timeout=15)
            break
        except:
            print 'Fail to get total page count, retry'

    soup = BeautifulSoup(u.read(), "lxml")
    all_reviews = soup.find("div", {"class": "paginate all-reviews"})
    if all_reviews != []:
        page_count = int(all_reviews.find("div", {"class": "paginated-content"})["total-number-of-pages"])
    page_count = min(page_limit, page_count)
    print 'Total page count is %d' % page_count
    return page_count


def get_app_title(product_id):
    url = "http://itunes.apple.com/cn/app/id%s?mt=8" % product_id
    req = urllib2.Request(url, headers={"X-Apple-Store-Front": store_front, "User-Agent": userAgent})

    # Handle possible network exception
    while True:
        try:
            u = urllib2.urlopen(req, timeout=15)
            break
        except:
            print 'Fail to get %s' % url

    soup = BeautifulSoup(u.read(), "lxml")
    app_title = soup.find("div", {"class": "title"}).find("a").contents[0]
    return app_title


if __name__ == "__main__":
    analyze(product_id)
