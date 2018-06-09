# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3 as lite
from scrapy.exceptions import DropItem

con = None # this is the db connection object. 
# it gets created on init and deleted on __del__ just be carful of circular dependincys, because del might not get called in that case. 

class DuplicatesPipeline(object):

    def __init__(self):
        self.urls_seen = set()

    def process_item(self, item, spider):
        if item['url'] in self.urls_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.urls_seen.add(item['url'])
            return item

class ZillowScrapyPipeline(object):

	def __init__(self):
		self.setupDBCon()

	def process_item(self, item, spider):
		self.storeInDb(item)
		return item

	def storeInDb(self, item):

		self.cur.execute('SELECT url FROM properties_property WHERE url = ?',(item['url'],))
		urlArr = self.cur.fetchall()
		if urlArr is not None:
			self.cur.execute('UPDATE properties_property SET property_type = ? , country = ?,state = ?,city = ?,street_address = ?,agent_name = ?,agent_number = ?,bath = ? ,bed = ?,desc = ?,image_url = ?,listing_type = ?,lot = ?,mls = ?,neighborhood = ?,price = ?,timestamp = ?,url = ?,year = ?,zestimate = ?,zipcode = ?,zestimate_rent = ?  WHERE url = ?'
				, (item['property_type'],'USA',item['state'],item['city'],item['address'],
					item['agent_name'],item['agent_number'],item['bath'],item['bed'],item['desc'],
					item['image_url'],item['listing_type'],item['lot'],item['mls'],item['neighborhood'],
					item['price'],item['timestamp'],item['url'],item['year'],item['zestimate'],item['zipcode'],
					item['zestimate_rent'],item['url'],))
		else:
			self.cur.execute(
			'INSERT INTO properties_property(property_type,country,state,city,street_address,agent_name,agent_number,bath,bed,desc,image_url,listing_type,lot,mls,neighborhood,price,timestamp,url,year,zestimate,zipcode,zestimate_rent) VALUES ("%s","%s" ,"%s","%s", "%s","%s", "%s","%s" ,"%s","%s", "%s","%s", "%s","%s" ,"%s","%s", "%s","%s" ,"%s","%s", "%s","%s")'%(item['property_type'],'USA',item['state'],item['city'],item['address'],item['agent_name'],item['agent_number'],item['bath'],item['bed'],item['desc'],item['image_url'],item['listing_type'],item['lot'],item['mls'],item['neighborhood'],item['price'],item['timestamp'],item['url'],item['year'],item['zestimate'],item['zipcode'],item['zestimate_rent'])
			)
		print '------------------------'
		print 'Data Stored in Database'
		print '------------------------'
		self.con.commit()

	def setupDBCon(self):
		self.con = lite.connect('db.sqlite3')
		self.cur = self.con.cursor()

	# this is the class destructor. It will get called automaticly by python's garbage collecter once this class is no longer used. 
	def __del__(self):
		self.closeDB()

	def closeDB(self):
		self.con.close()
