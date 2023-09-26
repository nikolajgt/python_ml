from faker import Faker
import random

class FakeCprNumber:
    def __init__(self):
        self.fake = Faker()

    def generate_cpr(self):
        # Generate date in DDMMYY format
        
        birth_date = self.fake.date_of_birth(tzinfo=None, minimum_age=18, maximum_age=90)
        date_part = birth_date.strftime('%d%m%y')
        
        # Generate a random 4-digit number for the last part
        last_part = str(random.randint(1000, 9999))
        return date_part + "-" + last_part