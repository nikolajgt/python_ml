from faker import Faker
class FakeBankReport:
    
    def __init__(self):
        self.fake = Faker()
        
    def generate_report(self, num_transactions=10):
        # Account Holder Info
        report = {
            "account_holder": self.fake.name(),
            "address": self.fake.address(),
            "account_number": self.fake.random_int(min=10000000, max=99999999),
            "account_type": self.fake.random_element(elements=('Savings', 'Current')),
            "transactions": []
        }
        
        balance = 0
        
        # Transactions
        for _ in range(num_transactions):
            transaction_type = self.fake.random_element(elements=('Deposit', 'Withdrawal'))
            amount = self.fake.random_int(min=1, max=10000)
            if transaction_type == "Withdrawal":
                amount = -amount
            balance += amount
            transaction = {
                "transaction_id": str(self.fake.uuid4()),
                "date": str(self.fake.date_time_this_month()),
                "type": transaction_type,
                "amount": amount,
                "description": self.fake.catch_phrase()
            }
            report["transactions"].append(transaction)
        
        # End of report summary
        report["closing_balance"] = balance
        report["report_date"] = str(self.fake.date_time_this_month())
        
        return report
    