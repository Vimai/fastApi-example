from bson import ObjectId
from pymongo import MongoClient


class MongoRepository:
    def __init__(self):
        self.client = MongoClient(host='localhost',
                                  port=27017,
                                  username='root',
                                  password='password')
        self.db = self.client.projectdb

    def create_product(self, payload):
        products = self.db.products
        product_id = products.insert_one(payload).inserted_id
        return product_id

    def update_product_name(self, product_id, product_name):
        products = self.db.products
        products.update_one({"_id": ObjectId(product_id)}, {"$set": {"name": product_name}})


client = MongoClient(host='localhost',
                     port=27017,
                     username='root',
                     password='password')
db = client.projectdb
posts = db.posts

post = {"author": "Mike",
        "text": "My first blog post!"}

post2 = {"author": "Mike2",
         "text": "My first blog post!2"}

post3 = {"author": "Mike3",
         "text": "My first blog post!3"}

post_id = posts.insert_one(post).inserted_id

posts.insert_many([post3, post2])

print(db)
print(db.list_collection_names())

results = posts.find({"author": "Mike3"})
print(results)
print('em lop: \n')
for result in results:
    print(f"result: {result} and id: {result['_id']}")

posts.update_one({"author": "Mike3"}, {"$set": {"author": "autor 3"}})

results = posts.find({})
print(results)
print('em lop 2: \n')
for result in results:
    print(f"result: {result} and id: {result['_id']}")

breakpoint()
