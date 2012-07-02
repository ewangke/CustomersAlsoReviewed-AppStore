"""
Find what customers also reviewed based on a centain app, specifically in China App Store
First version by ewangke at gmail.com
"""
import urllib2
import sys
from bs4 import BeautifulSoup

if len(sys.argv) != 2:
    print 'Usage: analyze.py <productID>'
    exit(0)

productID = sys.argv[1]
front = '143465-1,12'   # 143465 is the store ID, I don't know -1,12 means. To check all other store ids, see https://github.com/grych/AppStoreReviews/blob/master/AppStoreReviews.py
userAgent = 'iTunes/10.1.1 (Macintosh; Intel Mac OS X 10.6.5) AppleWebKit/533.19.4'     # Change your user agent if u want


def analyze(productID):
    links = []
    page = 1
    while(1):
        links_per_page = get_reviewer_links(productID, page)
        if links_per_page != []:
            links.extend(links_per_page)
            #print 'Get reviewers: Page %d processed' % page
            page += 1

        else:
            break

    review_count = len(links)
    print 'Finish getting reviewers: %d reviewers found.' % review_count

    relations = {}  # key: App Name, value: count
    relations['only-self'] = 0

    # FIXIT: Spawn threads to fetch web pages concurrently
    for link in links:
        # FIXIT: we only handle the first page review here
        reviewer_id = link.replace('http://itunes.apple.com/WebObjects/MZStore.woa/wa/viewUsersUserReviews?userProfileId=', '')
        reviewer_url = "http://itunes.apple.com//WebObjects/MZStore.woa/wa/allUserReviewsForReviewerFragment?userProfileId=%s&page=1&sort=14" % reviewer_id
        req = urllib2.Request(reviewer_url, headers={"X-Apple-Store-Front": front, "User-Agent": userAgent})

        # FIXIT: Handle possible network exception
        u = urllib2.urlopen(req, timeout=30)
        soup = BeautifulSoup(u.read(), "lxml")
        nodes = soup.findAll("div", {"class": "lockup small detailed option application"})

        if nodes is None:
            print 'Oops! %s has no reviews' % reviewer_id
            continue

        if len(nodes) == 1:
            relations['only-self'] += 1
        else:
            for node in nodes:
                app_name = node.find("li", {"class": "name"}).contents[0].contents[0]
                if app_name in relations:
                    relations[app_name] += 1
                else:
                    relations[app_name] = 1

        #print 'link %s processed' % link

    #for k in relations:
    #    print "%s\t%s\n" % (k.encode('utf-8'), relations[k])
    sorted_relations = sorted(relations.items(), key=lambda relations: relations[1])
    import json
    import codecs
    output_file = codecs.open("sorted_result.json", encoding='utf-8', mode='w')
    json.dump(sorted_relations, output_file)
    output_file.close()


def get_reviewer_links(productID, page):
    result = []

    url = "http://itunes.apple.com/WebObjects/MZStore.woa/wa/customerReviews?s=143465-1,12&id=%s&displayable-kind=11&page=%d&sort=4" % (productID, page)
    req = urllib2.Request(url, headers={"X-Apple-Store-Front": front, "User-Agent": userAgent})

    # FIXIT: Handle possible network exception
    u = urllib2.urlopen(req, timeout=30)
    soup = BeautifulSoup(u.read(), "lxml")
    all_reviews = soup.find("div", {"class": "paginate all-reviews"})
    if all_reviews:
        reviewers = all_reviews.findAll("a", {"class": "reviewer"})
        result = [link['href'] for link in reviewers]
    return result


if __name__ == "__main__":
    analyze(productID)
