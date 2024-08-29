from fastapi import FastAPI
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import json
import sqlite3

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello"}

@app.get("/scrape")
def run_scraper():
    from fenwick.spiders.fenwick_scraper import ClothingSpider
    
    process = CrawlerProcess(get_project_settings())
    
    process.crawl(ClothingSpider)
    process.start()
    
    return {"spider": "started"}

@app.get("/data")
def get_data():
    connection = sqlite3.connect("fenwick.db")
    cursor = connection.cursor()
    cursor.execute("SELECT brand, name, price, images_url FROM FenwickClothes")
    rows = cursor.fetchall()
    connection.close()
    
    data = []
    for row in rows:
        data.append({
            "brand": row[0],
            "name": row[1],
            "price": row[2],
            "images_url": json.loads(row[3])
        })
    
    return {"data": data}
