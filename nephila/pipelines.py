# -*- coding: utf-8 -*-
import pymongo

from scrapy.utils.project import get_project_settings
from scrapy.utils import log


class MongoPipeline(object):

    def open_spider(self, spider):
        settings = get_project_settings()

        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        db.drop_collection(spider.name)

        self.collection = db[spider.name]

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item
