from faker import Faker
import random
from .FakeCreditCardGen import FakeCreditCard

class EcommerceDataGenerator:
    def __init__(self):
        self.fake = Faker()

    def generate_cpr(self):
        # Generate date in DDMMYY format
        birth_date = self.fake.date_of_birth(tzinfo=None, minimum_age=18, maximum_age=90)
        date_part = birth_date.strftime('%d%m%y')
        # Generate a random 4-digit number for the last part
        last_part = str(random.randint(1000, 9999))
        return date_part + last_part

    def generate_report(self, num_transactions=10, sensitive=False):
        ecommerce_data = {
            "user_info": self._user_information(sensitive),
            "transaction_info": [self._transaction_information() for _ in range(num_transactions)],
            "payment_info": self._payment_information()
        }
        return ecommerce_data

    def _user_information(self, sensitive=False):
        """Generate user related data."""
        data = {
            'user_id': self.fake.uuid4(),
            'username': self.fake.user_name(),
            'email': self.fake.email(),
            'address': self.fake.address(),
        }
        if sensitive:
            data["cpr"] = self.generate_cpr()
        return data

    def _transaction_information(self):
        """Generate transaction related data."""
        data = {
            'transaction_id': self.fake.uuid4(),
            'product_id': self.fake.uuid4(),
            'product_name': self.fake.bs(),
            'product_category': self.fake.random_element(elements=('Electronics', 'Clothing', 'Home', 'Beauty')),
            'purchase_date': self.fake.date_time_this_year(),
            'amount': self.fake.random_int(min=5, max=1000)
        }
        return data

    def _payment_information(self):
        """Generate payment related data."""
        creditcardclass = FakeCreditCard()

        return creditcardclass.generate_creditcards()