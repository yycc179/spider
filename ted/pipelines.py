# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import settings
from video_url import get_play_url
from pymongo import MongoClient
import json
import time

class TedPipeline(object):
    def __init__(self):
        self.client = MongoClient(settings.MONGO_HOST)
        db = self.client[settings.MONGODB_DB]
        self.collection = db[settings.MONGODB_COLLECTION]
        # self.collection.remove()

    def process_item(self, item, spider):
        id = item['link']
        source = get_play_url(id)
        dic = json.loads(source)
        name = dic['fulltitle']
        video = {
            'name': name,
            'url': dic['url'],
            'img': item['img'],
            'duration':item['duration']
        }
        self.collection.update({'name': name}, video, True)
        # self.collection.insert_one(video)
        time.sleep(1)
        return item

    def close_spider(self, spider):
        self.client.close()
