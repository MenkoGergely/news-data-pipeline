import requests
import psycopg2
from datetime import datetime, time
from dotenv import load_dotenv
import os

load_dotenv()
print(f"API Key loaded: {os.getenv('NEWS_API_KEY') is not None}")
print(f"DB Host: {os.getenv('DB_HOST')}")
print(f"DB Name: {os.getenv('DB_NAME')}")
url = (f"https://newsapi.org/v2/everything?q=AI&apiKey={os.getenv('NEWS_API_KEY')}")

def get_news_info(name):
  response = requests.get(name)
  if(response.status_code==200):
    return response.json()
  else:
    print(f"failed to retrieve data {response.status_code}")



conn=None
cur=None
max_retries=5
try:
    for attempt in range(max_retries):
      try:  
        conn = psycopg2.connect(host=os.getenv('DB_HOST'),dbname=os.getenv('DB_NAME'),user=os.getenv('DB_USER'),password=os.getenv('DB_PASSWORD'),port=os.getenv('DB_PORT'))
        cur = conn.cursor()
        break
      except Exception as error:
         print(f"Attempt failed {e}")
         time.sleep(3)
         
      create_script ='''CREATE TABLE IF NOT EXISTS headlines(
          id  serial PRIMARY KEY,
          title varchar,
          source varchar,
          author varchar,
          url varchar,
          published_at varchar,
          fetched_at timestamp
        )'''

      cur.execute(create_script)
      conn.commit()

      news_json=get_news_info(url)



      for data in news_json["articles"]:
          insert_script ="INSERT INTO headlines (title,source,author,url,published_at,fetched_at) VALUES (%s,%s,%s,%s,%s,%s)"

          insert_value = (data["title"],data["source"]["name"],data["author"],data["url"],data["publishedAt"],datetime.now())
          cur.execute(insert_script,insert_value)
      conn.commit()
      print("All articles inserted!")
       
    
except Exception as error:
    print(error)
finally:
    if cur is not None:
        cur.close()
    if conn is not None:
      conn.close()
      
