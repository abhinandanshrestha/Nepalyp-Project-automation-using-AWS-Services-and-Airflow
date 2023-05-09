import scrapy

class ScrapeSpider(scrapy.Spider):
    name = 'scrape'
    # allowed_domains = ['nepalyp.com']
    start_urls = ['http://nepalyp.com/category/Communications/']
    # base_url='http://www.nepalyp.com'

    def parse(self, response):
        pages=int(response.css('div.pages_container a:nth-child(5)::text').get())
        for page in range(1,pages+1):
            page_url=self.start_urls[0]+str(page)
            yield response.follow(page_url,callback=self.individualPageScraper)

    def individualPageScraper(self,response):
        for link in response.css('div.company h4 a::attr(href)'):
            yield response.follow(link.get(),callback=self.parsecat)

    def parsecat(self,response):
        # info_list=response.css('div.info::text').getall()

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

        yield{
            'rating':response.css('div.cmp_rate span.rate::text').get(),
            'no_of_reviews':response.css('div.cmp_rate a.reviews_count span::text').get(),
            'company_name':response.css('#company_name::text').get(),
            'district_location':response.css('.location a::text').get(),
            'phone_no':response.css('.phone::text').get(),
            'website':response.css('div.weblinks a::attr(href)').get(),
            'working_hour':working_hours,
            'establishment_year':establishment_year,
            'no_of_employess':employees,
            'company_manager':manager
        }
