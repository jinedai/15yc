#!/usr/bin/env python
# coding=utf-8
import pymongo
from scrapy.conf import settings  

class MongoPipeline(object):

    def __init__(self):  
        connection = pymongo.MongoClient(  
           settings[ 'MONGODB_SERVER' ],  
           settings[ 'MONGODB_PORT' ]  
        )  
        db = connection[settings[ 'MONGODB_DB' ]]  
        self.collection = db[settings[ 'MONGODB_COLLECTION' ]] 


    def process_item(self, item, spider):
#        self.db[self.collection_name].update({'video_name': item['videoname']}, {'$set': dict(item)}, True)
        self.collection.save({'video_name': item['videoname'], 'video_url': item['videourl']})
        return item
