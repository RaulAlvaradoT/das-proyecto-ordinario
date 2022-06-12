import numpy as np
from faker import Faker


class Transaction:
    _REFERENCE = 1

    def __init__(self,
                 amount,
                 category,
                 ):
        self.__fake = Faker()
        self._reference = "{:06d}".format(self._REFERENCE)
        self.__date = str(self.__fake.date_between())
        self.__amount = amount
        self.__type = "inflow" if (amount >= 0) else "outflow"
        self._category = category
        self.__user = ""
        self.__user_email = ""
        Transaction._REFERENCE += 1

    def set_user_data(self, user, user_email):
        self.__user = user
        self.__user_email = user_email

    def _get_object_to_dict(self):
        transaction_dict = {
            "reference": self._reference,
            "date": self.__date,
            "amount": self.__amount,
            "type": self.__type,
            "category": self._category,
            "user": self.__user,
            "user_email": self.__user_email,
        }

        return transaction_dict

    def __str__(self):
        msg = ("==" * 15) + "\n"
        msg += f"- Reference: \t{self._reference}\n".expandtabs(20)
        msg += f"- Date: \t{self.__date}\n".expandtabs(20)
        msg += f"- Amount: \t{self.__amount}\n".expandtabs(20)
        msg += f"- Type: \t{self.__type}\n".expandtabs(20)
        msg += f"- Category: \t{self._category}\n".expandtabs(20)
        msg += f"- User: \t{self.__user}\n".expandtabs(20)
        msg += f"- User e-mail: \t{self.__user_email}\n".expandtabs(20)
        msg += ("==" * 15) + "\n"
        return msg


class TransactionGenerator:
    def __init__(self):
        pass

    def generate_rnd_transactions(self, num_users):
        categories = [
            "salary", "savings", "groceries",
            "transfer", "rent", "other"
        ]
        inflows = ["salary", "savings"]
        outflows = ["groceries", "transfer", "rent", "other"]

        transactions = []

        for _ in range(num_users):
            fake = Faker()
            fake_name = fake.name()
            fake_email = fake.email()

            for category in categories:
                if category in inflows:
                    amount = np.random.randint(3000, 5000)
                    transaction = Transaction(amount, category)
                    transaction.set_user_data(fake_name, fake_email)

                if category in outflows:
                    amount = np.random.randint(1000, 3000)
                    transaction = Transaction(-amount, category)
                    transaction.set_user_data(fake_name, fake_email)

                transaction = transaction._get_object_to_dict()
                transactions.append(transaction)

        return transactions
