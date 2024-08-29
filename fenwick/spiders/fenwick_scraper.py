import scrapy

class FenwickClothesItem(scrapy.Item):
    brand = scrapy.Field()
    name = scrapy.Field()
    images_url = scrapy.Field()
    price = scrapy.Field()

class ClothingSpider(scrapy.Spider):
    name = "fenwick_scraper"
    base_url = "https://www.fenwick.co.uk"
    urls = [ "/women/clothing", "/men/clothing"]
    count = 0

    def start_requests(self):
        for url in self.urls:
            url_to_scrape = self.base_url + url 
            yield scrapy.Request(url=url_to_scrape, callback=self.clothing_url_scraper)

    def clothing_url_scraper(self, response):
        clothing_link = response.css('a.b-product_tile-image_link::attr(href)').getall()
        for link in clothing_link:
            clothing_url = self.base_url + link
            yield {'Clothing url': clothing_url}
            
            yield scrapy.Request(url=clothing_url, callback=self.clothing_detail_scraper)
    
    def clothing_detail_scraper(self, response):
        brand = self.brand_scraper(response)
        product_name, images_url = self.product_scraper(response)
        price = self.price_scraper(response)
        
        clothes = FenwickClothesItem(
            brand=brand,
            name=product_name,
            images_url=images_url,
            price=price
        )
        
        if brand and product_name and price:
            self.count = self.count + 1
            print(self.count)
        
        yield clothes

    def brand_scraper(self, response):
        brand = response.css('a.b-product-brand_link::text').get()
        return brand.strip() if brand else None
    
    def product_scraper(self, response):
        product_name = response.css('span.b-product_tile-name_link::text').get()
        
        if not product_name:
            return None, None
        
        images_url = self.images_url_scraper(product_name, response)
        
        return product_name, images_url

    def images_url_scraper(self, product_name, response):
        if not product_name:
            return None
        images_url = response.css(f'img[title="{product_name}"]::attr(src)').getall()
        return images_url if images_url else None

    def price_scraper(self, response):
        price = response.css('span.b-pdp_price-price.js-item-price.m-retail::text').get()
        return price.strip() if price else None