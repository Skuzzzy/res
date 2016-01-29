from BeautifulSoup import BeautifulSoup
import urllib2
import re
from dateutil.parser import parse

def grab_link_info(url):
    page = urllib2.urlopen(url)
    print page
    return obtain_review_info(page.read())

def obtain_review_info(page_content):
    soup = BeautifulSoup(page_content)

    user = soup.find('div', {'class': 'user'})
    user_link = user.div.p.a
    user_name = user_link['href'].replace(r'/user/', '') # This isn't a completly terrible way of doing this
    real_name = user_link.contents[0]

    content = soup.find('div', {'class': 'checkin box'})
    beer = content.find('div', {'class': 'beer'})

    beer_name = beer.p.a.contents[0]
    brewery = beer.span.a.contents[0]

    timestamp = content.find('p', {'class': 'time'}).contents[0]
    timestamp =  parse(timestamp)

    rating = content.findAll('span', {'class': re.compile('^rating')})
    rating_info = rating[0]['class'].split()[-1] # TODO Make this line not suck
    rating_info = rating_info[1] + "." + rating_info[2:] # TODO This line sucks too

    comment = content.find('p', {'class': 'comment'}).contents

    return {
        'user_name' : user_name,
        'real_name' : real_name,
        'beer_name' : beer_name,
        'brewery'   : brewery,
        'timestamp' : timestamp,
        'rating'    : rating_info,
        'comment'   : comment[0] if comment else None
    }

url= 'https://untappd.com/user/pmnphxaz/checkin/268614188'
# url = 'https://untappd.com/user/pmnphxaz/checkin/270504313'
# url= 'https://untappd.com/user/namslaw1/checkin/268638791'
print grab_link_info(url)

