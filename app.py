from flask import Flask, jsonify
from database.mongo_db import UserTransactionDB
from funct.user_transaction import TransactionGenerator
import os

users_db = UserTransactionDB()
users_db.create_mongo_db()
transactions_coll = users_db.get_db_collection()

trans_generator = TransactionGenerator()
rand_transactions = trans_generator.generate_rnd_transactions(5)
transactions_coll.insert_many(rand_transactions)

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@app.route('/', methods=["GET"])
def index():
    transactions_json = jsonify(
        [trans for trans in transactions_coll.find(
            {}, {'_id': False, 'date': 0})
         ]
    )

    return transactions_json


@app.route('/transactions', methods=["GET"])
def user_transactions():
    transactions_json = jsonify(
        [trans for trans in transactions_coll.find({}, {'_id': False})])

    return transactions_json


@app.route('/transactions/grouped_by_type', methods=["GET"])
def transactions_by_type():
    group_by_type = [
        {
            "$group": {
                "_id": "$user_email",
                "total_inflow": {
                    "$sum": {
                        "$cond": [
                            {"$eq": ["$type", "inflow"]}, "$amount", 0]
                    }
                },
                "total_outflow": {
                    "$sum": {
                        "$cond": [{"$eq": ["$type", "outflow"]}, "$amount", 0]
                    }
                },
            }
        },
        {
            "$project": {
                "_id": 0,
                "user_email": "$_id",
                "total_inflow": "$total_inflow",
                "total_outflow": "$total_outflow"}
        }
    ]

    group_by_type_coll = transactions_coll.aggregate(group_by_type)
    group_by_type_coll = jsonify(list(group_by_type_coll))

    return group_by_type_coll


@app.route('/transactions/<user>/summary', methods=["GET"])
def transactions_user_summary(user):
    user_summary = [
        {"$match": {"user": user}},
        {
            "$group": {
                "_id": "$type",
                "categories": {"$addToSet": "$category"},
                "amounts": {"$addToSet": "$amount"}
            }
        },
        {"$sort": {"_id": 1}}
    ]

    user_summary_coll = transactions_coll.aggregate(user_summary)
    user_summary = {}

    for user_summary_dict in user_summary_coll:
        summary = {}
        transaction_type = user_summary_dict["_id"]
        categories = user_summary_dict["categories"]
        amounts = user_summary_dict["amounts"]

        for category, amount in zip(categories, amounts):
            summary[category] = amount

        user_summary[transaction_type] = summary

    return user_summary


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
