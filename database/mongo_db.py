import pymongo


class UserTransactionDB:
    def __init__(self):
        self.client = self._generate_mongo_client()
        self.__users_db = None
        self.__transactions = None

    def _generate_mongo_client(self):
        mongo_client = pymongo.MongoClient(
            host="mongo_db",
            port=27017,
            username="root",
            password="kberl"
        )

        return mongo_client

    def create_mongo_db(self):
        self.__users_db = self.client["users_db"]
        self.__transactions = self.__users_db["transactions"]

    def get_db_collection(self):
        return self.__transactions
