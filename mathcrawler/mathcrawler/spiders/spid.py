import scrapy
from mathcrawler.items import Person

root = "http://genealogy.math.ndsu.nodak.edu/"

class MathSpider(scrapy.Spider):
    name = "math"
    allowed_domains = ["genealogy.math.ndsu.nodak.edu"]
    # start_urls = [
        # "http://genealogy.math.ndsu.nodak.edu/query-prep.php",
    # ]

    def start_requests(self):
        return [ scrapy.FormRequest("http://genealogy.math.ndsu.nodak.edu/query-prep.php",
                     formdata={
                         'given_name' : '',
                         'other_names' : '',
                         'family_name' : '',
                         'school' : '',
                         'year' : '',
                         'thesis' : 'mining',
                         'country' : '',
                         'msc' : '68',
                         },
                     callback=self.initial_parse) ]

    def initial_parse(self, response):
        # Select all the links in the td of the table
        # TODO Link Pattern
        link_snippets = response.selector.xpath('//table//td/a//@href').extract()
        links = [ root + snippet for snippet in link_snippets]
        # print "\n".join(links)
	for link in links:
	    yield scrapy.Request(link, callback=self.parse)

    def parse(self, response):
	# Note, I am going to make the assumption that a student will never be
	# the advistor, or a 'parent' of an advisor of themselves
        # Note2: All code following this note sucks. Beware

	main = response.selector.xpath('//div[@id="paddingWrapper"]') # Grabbing main content area
	name = main.xpath('./h2/text()').extract()[0].strip() # Index 0 as there should only be one name
	info = main.xpath('./div/span/text()').extract() # This grabs a couple different info
        info = [part.strip() for part in info]
	univ = main.xpath('./div/span/span/text()').extract()[0].strip() # University info (hint not actually)
	subject_infos = main.xpath('./div/text()').extract() # Contains Subject Classification somewhere...
        students_links = response.selector.xpath('//table//td/a//@href').extract()

        # This website doesn't have a good structure or label the its elements
        # So I have to do this stuff, well it's likely that I'm just not seeing
        # something basic, which would make this a lot cleaner
        partial_advisors = main.xpath('./p/a')
        links = partial_advisors.xpath('./@href').extract()
        text = partial_advisors.xpath('./text()').extract()
        unfiltered_advisors = zip(links, text)
        advisors = [(pair[1], int(pair[0][10:])) for pair in unfiltered_advisors if pair[0].startswith('id.php?')]

        for part in subject_infos:
            # Locate the correct part
            looking_for = 'Mathematics Subject Classification'
            if looking_for in part:
                # Magic constants take a string such as
                # 'Mathematics Subject classification: 68 ......'
                # And grabs the 68 part. (Regex is much more appropriate and should be used here)
                classification = part[len(looking_for)+2:len(looking_for)+4]

        # This grabs the professor ID number (their db index)
        # The response url is just a string so I don't have a nice method to grab the args
        identifier = response.url[response.url.index("=")+1:]


        # Grabbing the student id (their db index)
        students = [int(student[student.index('=')+1:]) for student in students_links]

        # Build person object
        person = Person()
        person['name'] = name
        person['identifier'] = int(identifier)
        person['title'] = info[0]
        person['university'] = univ
        person['year'] = int(info[1])
        person['dissertation'] = info[3]
        person['subject_classification'] = classification
        person['students'] = students
        person['advisors'] = advisors
        # Grab advisor information as well?

        links = [ root + snippet for snippet in students_links]
        for link in links:
            yield scrapy.Request(link, callback=self.parse)

        yield person
