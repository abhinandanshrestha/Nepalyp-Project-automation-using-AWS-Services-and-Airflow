# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# approach a: scraped data --> item containers --> scrapy crawl <spider> -o <outputfile>
# approach b: scraped data --> item containers --> Database (Postgresql chalako xu)

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

db_params = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}


class FinalquestionPipeline:
    def process_item(self, item, spider):
        try:
            connection = psycopg2.connect(**db_params)
    
            cursor = connection.cursor() # allows you to execute SQL queries and fetch data from the database

            # SQL query to insert the item into the database
            insert_query = '''
            INSERT INTO companytable (category, rating, no_of_reviews, company_name, district_location, phone_no, website, working_hour, establishment_year, no_of_employee, company_manager)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
            values = (
                item['category'],
                item['rating'],
                item['no_of_reviews'],
                item['company_name'],
                item['district_location'],
                item['phone_no'],
                item['website'],
                item['working_hour'],
                item['establishment_year'],
                item['no_of_employee'],
                item['company_manager']
            )
            cursor.execute(insert_query, values) # execute the query
            connection.commit() # commits the changes made by the previous INSERT query to the database. It ensures that the modifications are permanently saved.
            cursor.close() # free up system resources

        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL:", error)
        
        finally:
            # Code that will be executed regardless of exceptions
            # connection has to be closed regardless of exceptions once it has been started
            if connection:
                connection.close()

        return item