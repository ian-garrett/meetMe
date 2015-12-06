#Script for clearing out all memos from a DB
from pymongo import MongoClient

import CONFIG

try:
	dbclient = MongoClient(CONFIG.MONGO_URL)
	db = dbclient.meetme
	collection = db.dated

except:
	print("Failure opening database. Is Mongo running? Correct password?")
	sys.exit(1)

for record in collection.find({}):
	print(record)

collection.remove({})
