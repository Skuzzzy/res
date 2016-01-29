from BeautifulSoup import BeautifulSoup
import urllib2
import re

def grab_link_info(url):
    page = urllib2.urlopen(url)
    return obtain_review_info(page.read())

def obtain_review_info(page_content):
    soup = BeautifulSoup(page_content)

    user = soup.find('div', {'class': 'user'})
    user_link = user.div.p.a
    user_name = user_link['href'].replace(r'/user/', '') # Should use regex but this is easy and should work every time
    real_name = user_link.contents

    content = soup.find('div', {'class': 'checkin box'})
    beer = content.find('div', {'class': 'beer'})

    beer_name = beer.p.a.contents # list of 1 len
    brewery = beer.span.a.contents # list of 1 len

    timestamp = content.find('p', {'class': 'time'}).contents
    rating = content.findAll('span', {'class': re.compile('^rating')})
    rating_info = rating[0]['class'].split()[-1] # TODO Make this line not suck
    print rating_info

    # print rating_info
    # print soup
    comment = content.find('p', {'class': 'comment'}).contents
    if comment:
        print comment[0]

    print "what"
    return {
        'user_name' : user_name,
        'real_name' : real_name[0],
        'beer_name' : beer_name[0],
        'brewery'   : brewery[0],
        'timestamp' : timestamp[0],
        'comment'   : comment[0] if comment else None
    }

url= 'https://untappd.com/user/pmnphxaz/checkin/268614188'
# url = 'https://untappd.com/user/pmnphxaz/checkin/270504313'
# url= 'https://untappd.com/user/namslaw1/checkin/268638791'
print grab_link_info(url)
