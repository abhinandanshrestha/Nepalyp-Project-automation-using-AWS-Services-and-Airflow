# nepalypscraper
This is a data pipelining project that scrapes data from https://www.nepalyp.com/

## Steps followed:
1. Scraped data from https://www.nepalyp.com
2. Stored the scraped data into PostgreSQL database.
3. Created api from the database.
4. Requested data from the API server and created visualization using Plotly.

## Framework and tools used:
1. Scrapy: To scrape data from https://www.nepalyp.com
2. PostgreSQL: To store scraped data using Scrapy.
3. Nodejs and Express.js: To create API endpoint from the data stored in the PostgreSQL database.
4. Plotly: To create visualization from the data received as a response from the API server.

## How to run the project?
>Step1:
> pip install -r requirements.txt

>Step2:
> scrapy crawl scrape 

>Step3:
> npm install 

>Step4:
> npm install -g nodemon

>Step5:
> nodemon index

>Step 6:
> open visualization.ipynb 