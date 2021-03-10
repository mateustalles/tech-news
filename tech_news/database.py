from pymongo import MongoClient
from decouple import config

DB_HOST = config("DB_HOST", default="localhost")
DB_PORT = config("DB_PORT", default="27017")

client = MongoClient(host=DB_HOST, port=int(DB_PORT))
db = client.tech_news


def create_news(data):
    db.news.insert_many(data)


def insert_or_update(notice):
    return (
        db.news.update_one(
            {"url": notice["url"]}, {"$set": notice}, upsert=True
        ).upserted_id
        is not None
    )


def find_news():
    return list(db.news.find({}, {"_id": False}))


def search_news(query):
    return list(db.news.find(query))


def fetch_top5_news():
    return list(db.news.aggregate(
        [
            {
                "$project": {
                    "title": 1,
                    "url": 1,
                    "popularity": {"$sum": [
                        "$shares_count", "$comments_count"
                        ],
                    }
                }
            },
            {
                "$sort": {"popularity": -1, "title": 1}
            },
            {
                "$limit": 5
            }
        ]
    ))


def fetch_top5_categories():
    return list(db.news.aggregate(
        [
            {
                "$unwind": "$categories"
            },
            {
                "$group": {
                    "_id": "$categories",
                    "count": {"$sum": 1}
                }
            },
            {
                "$sort": {"count": -1, "_id": 1}
            },
            {
                "$limit": 5
            }
        ]
    ))
