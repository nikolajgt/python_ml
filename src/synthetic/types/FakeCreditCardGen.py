from faker import Faker
class FakeCreditCard:
    """Class to generate fake credit card numbers for various card types."""

    def __init__(self):
        self.fake = Faker()

    def generate_creditcards(self):
        """Generate and return a list of fake credit card numbers."""
        creditCardTypes = ["maestro", "mastercard", "visa16", "visa13", "visa19", "amex", "discover", "diners", "jcb15", "jcb16"] 
        creditcards = []
        for type in creditCardTypes:
            data = {
                'payment_type': self.fake.random_element(elements=('Credit Card', 'PayPal', 'Bank Transfer')),
                'credit_card': self.fake.credit_card_number(card_type=type),
                'expiry_date': self.fake.credit_card_expire(),
                'cvv': self.fake.credit_card_security_code(card_type=type)
            }
            creditcards.append(data)
            
        return creditcards