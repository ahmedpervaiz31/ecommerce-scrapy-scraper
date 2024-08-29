from itemadapter import ItemAdapter
import sqlite3
import json

class FenwickPipeline:
    def open_spider(self, spider):
        self.connection = sqlite3.connect("fenwick.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS FenwickClothes
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        brand TEXT,
                        name TEXT NOT NULL,
                        images_url TEXT,
                        price FLOAT NOT NULL)""")
        self.connection.commit()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if self.check_duplicate(adapter):
            return item

        images_url_json = json.dumps(adapter.get('images_url', []))
        
        self.cursor.execute("INSERT INTO FenwickClothes (brand, name, images_url, price) VALUES (?, ?, ?, ?)",
                            (
                                adapter.get('brand'),
                                adapter.get('name'),
                                images_url_json,
                                adapter.get('price')
                            ))
        self.connection.commit()
        return item
    
    def check_duplicate(self, adapter):
        self.cursor.execute("SELECT * FROM FenwickClothes WHERE brand = ? AND name = ? AND price = ?", 
                            (adapter.get('brand'), adapter.get('name'), adapter.get('price')))
        result = self.cursor.fetchone()
        return result is not None
    
    def close_spider(self, spider):
        self.connection.close()
