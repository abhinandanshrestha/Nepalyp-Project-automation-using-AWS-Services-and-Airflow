import os
import sys
import subprocess

# install psychopg2-binary so that the package is available to the lambda_function.py locally
subprocess.call('pip3 install psycopg2-binary -t /tmp/ --no-cache-dir'.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
sys.path.insert(1, '/tmp/')

import psycopg2

dbparams={
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'postgresql',
    'host': 'postgres.clptmxbw0fgh.us-east-1.rds.amazonaws.com',
    'port': '5432'
}

def lambda_handler(event,context):
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(**dbparams)

    # Execute a query
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM companytable')
    rows = cursor.fetchall()
    
    # print(rows)
    # returns a list of tuples
    # [(...),(...)(15768, 'Web_Design', '5.0', '1', 'Bikashsoft Technology pvt. Ltd.', 'Kathmandu', 
    # '014378541', 'http://bikashsoft.com/', 'Not Specifieed', '2011', ' 6-10', 'Not Specified')]

    # Process the results
    results = []
    for row in rows:
        result = {
            'id': row[0],
            'category': row[1],
            'rating':row[2],
            'no_of_reviews':row[3],
            'company_name':row[4],
            'district_location':row[5],
            'phone_no':row[6],
            'website':row[7],
            'working_hour':row[8],
            'establishment_year':row[9],
            'no_of_employee':row[10],
            'company_manager':row[11]
        }
        results.append(result)
    
    # Close the database connection
    conn.close()
    
    # Return the results
    return {
        'statusCode': 200,
        'body': results
    }

print(lambda_handler())