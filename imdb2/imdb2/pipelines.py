# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#import pymongo
import sqlite3


# class MongodbPipeline(object):
#
#     collection_name = "best_movies2"
#
#     #  Reason for this method is to grab something from the settings file
# #     @classmethod
# #     def from_crawler(cls, crawler):
# # #   Now to get that something from the settings file using crawler.settings.get
# # #   but we'll just log it - the cls above is for classmethod and this will be
# # #   executed before open_spider
# #         logging.warning(crawler.settings.get("MONGO_URI"))
#
#     def open_spider(self, spider):
#         self.client = pymongo.MongoClient("mongodb+srv://krwins:#2535Tardkids@cluster0-6cx9c.mongodb.net/test?retryWrites=true&w=majority")
#         self.db = self.client['IMDB2'
#         ]
#     def close_spider(self, spider):
#        self.client.close()
#
#     def process_item(self, item, spider):
#         self.db[self.collection_name].insert(item)
#         return item

class SQLitePipeline(object):

    def open_spider(self, spider):
        self.connection = sqlite3.connect("imdb2.db")
        '''To be able to make sql queries you have to create a cursor object. 
        Next we have to execute a sql query that will create a table to store
        all the movies info'''
        self.c = self.connection.cursor()
        try:
            self.c.execute('''
                CREATE TABLE best_movies2(
                            title TEXT,
                            year TEXT,
                            rating TEXT,
                            duration TEXT,
                            genre TEXT,
                            movie_url TEXT
                )
            ''')
            self.connection.commit()
        except sqlite3.OperationalError:
            pass

    def close_spider(self, spider):
       self.connection.close()

    def process_item(self, item, spider):
        self.c.execute('''
            INSERT INTO best_movies2(title,year,rating,duration,genre,movie_url) VALUES(?,?,?,?,?,?)
        ''', (
            item.get('title'),
            item.get('year'),
            item.get('rating'),
            item.get('duration'),
            item.get('genre'),
            item.get('movie_url')
        ))
        self.connection.commit()
        return item