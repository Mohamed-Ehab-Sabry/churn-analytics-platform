from pymongo import MongoClient
import json
# Example URI (replace username, password, and cluster name)
uri = "mongodb+srv://sara23012713_db_user:26993221ar@firstmongo.zreshik.mongodb.net/?appName=firstmongo"

# Connect to your cluster
client = MongoClient(uri)

# Access your existing database
db = client["telecom_data"]

collection = db["customer_reviews"]

with open("customer_reviews.jsonl", "r", encoding="utf-8") as f:
    data = [json.loads(line) for line in f]
    collection.insert_many(data)

print(f"✅ Inserted {len(data)} documents into MongoDB!")
