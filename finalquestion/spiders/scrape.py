import scrapy
from ..items import FinalquestionItem

class ScrapeSpider(scrapy.Spider):
    name = 'scrape'
    # allowed_domains = ['nepalyp.com']
    categories=['Communications','Web_Design','Computer_Consumables','Computer_services','Web_development','Computer_software_solution','Computer_training','Internet_service_providers','Web_services','Web_hosting','Software_applications','Networking','Information_technology','Online_Content','Computers_hardware','Computer_repair','Mail_Services']
    # categories=['Mail_Services']
    # start_urls = ['http://nepalyp.com/category/Communications/']
    # base_url='http://www.nepalyp.com'

    def start_requests(self):
        for category in self.categories:
            url = f'http://nepalyp.com/category/{category}/'
            yield scrapy.Request(url=url, callback=self.parse,meta={'category': category})

    def parse(self, response):
        category = response.meta['category']

        if category=='Computers_hardware' or category=='Computer_repair':
            pages=int(response.css('div.pages_container a:nth-child(3)::text').get())
        elif category=='Mail_Services':
            pages=1
        else:
            pages=int(response.css('div.pages_container a:nth-child(5)::text').get())

        for page in range(1,pages+1):
            # page_url=self.start_urls[0]+str(page)
            page_url = response.url + str(page)
            yield response.follow(page_url,callback=self.individualPageScraper, meta={'category': category})

    def individualPageScraper(self,response):
        category = response.meta['category']
        for link in response.css('div.company h4 a::attr(href)'):
            yield response.follow(link.get(),callback=self.parsecat, meta={'category': category})

    def parsecat(self,response):

        items=FinalquestionItem()

        # info_list=response.css('div.info::text').getall()
        category = response.meta['category']
        # Extract Working Hours
        working_hours_label = response.xpath('//span[@class="label" and contains(text(), "Working hours")]/following-sibling::text()').get()
        working_hours = working_hours_label.strip() if working_hours_label is not None else 'Not Specifieed'

        # Extract Establishment Year
        establishment_year_label = response.xpath('//span[@class="label" and contains(text(), "Establishment year")]/following-sibling::text()').get()
        establishment_year = establishment_year_label.strip() if establishment_year_label is not None else 'Not Specified'

        # Extract Number of Employees
        employees_label = response.xpath('//span[@class="label" and contains(text(), "Employees")]/following-sibling::text()').get()
        employees = employees_label if employees_label is not None else 'Not Specified'

        # Extract Company Manager
        manager_label = response.xpath('//span[@class="label" and contains(text(), "Company manager")]/following-sibling::text()').get()
        manager = manager_label.strip() if manager_label is not None else 'Not Specified'


        items['category']=category
        items['rating']=response.css('div.cmp_rate span.rate::text').get()
        items['no_of_reviews']=response.css('div.cmp_rate a.reviews_count span::text').get()
        items['company_name']=response.css('#company_name::text').get()
        items['district_location']=response.css('.location a::text').get()
        items['phone_no']=response.css('.phone::text').get()
        items['website']=response.css('div.weblinks a::attr(href)').get()
        items['working_hour']=working_hours
        items['establishment_year']=establishment_year
        items['no_of_employee']=employees
        items['company_manager']=manager

        yield items
        # yield{
        #     'category': category,
        #     'rating':response.css('div.cmp_rate span.rate::text').get(),
        #     'no_of_reviews':response.css('div.cmp_rate a.reviews_count span::text').get(),
        #     'company_name':response.css('#company_name::text').get(),
        #     'district_location':response.css('.location a::text').get(),
        #     'phone_no':response.css('.phone::text').get(),
        #     'website':response.css('div.weblinks a::attr(href)').get(),
        #     'working_hour':working_hours,
        #     'establishment_year':establishment_year,
        #     'no_of_employess':employees,
        #     'company_manager':manager
        # }
