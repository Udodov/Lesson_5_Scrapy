# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
"""from itemadapter import ItemAdapter


class BooksScraperPipeline:
    def process_item(self, item, spider):
        return item"""

import pymongo

class MongoDBPipeline:
    def open_spider(self, spider):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["books_db"]
        self.collection = self.db["books"]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.collection.insert_one(dict(item))
        return item
    