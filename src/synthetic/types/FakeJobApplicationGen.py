from faker import Faker
from FakeCprGen import FakeCprNumber

class JobApplicationGenerator:
    def __init__(self):
        self.fake = Faker()

    def generate_application(self, num_employments=3, num_educations=2, num_references=2, sensitive=False):
        personal_details = []
        employments = []
        educations = []
        references_list = []

        detail = {
            "applicant_name": self.fake.name(),
            "applicant_email": self.fake.email(),
            "phone_number": self.fake.phone_number(),
            "address": self.fake.address(),
            "position_applied_for": self.fake.job(),
            "cover_letter": self.fake.text(max_nb_chars=500)
        }

        if sensitive:
            gen = FakeCprNumber()
            detail["cpr"] = gen.generate_cpr()

        personal_details.append(detail)
        
        # Employment History
        for _ in range(num_employments):
            employment = {
                "employer": self.fake.company(),
                "job_title": self.fake.job(),
                "start_date": self.fake.date_this_decade(),
                "end_date": self.fake.date_this_decade(),
                "reason_for_leaving": self.fake.sentence(nb_words=6)
            }
            employments.append(employment)

        # Education
        for _ in range(num_educations):
            education = {
                "institution": "",
                "degree": self.fake.random_element(elements=("B.S.", "M.S.", "Ph.D.", "Associate's")),
                "major": self.fake.bs(),
                "graduation_date": self.fake.date_this_century()
            }
            educations.append(education)

        # References
        for _ in range(num_references):
            reference = {
                "name": self.fake.name(),
                "relationship": self.fake.random_element(elements=("Previous Employer", "Professor", "Colleague")),
                "phone": self.fake.phone_number(),
                "email": self.fake.email()
            }
            references_list.append(reference)
        
        return personal_details, employments, educations, references_list