import csv
from multiprocessing import Pool
from types.FakeJobApplicationGen import JobApplicationGenerator
from types.FakeEcommerceSaleGen import EcommerceDataGenerator
from types.FakeBankRapportGen import FakeBankReport
from types.FakeCprGen import FakeCprNumber
from types.FakeCreditCardGen import FakeCreditCard

num_samples = 100000
generatorEcommerce = EcommerceDataGenerator()
generatorJobApplication = JobApplicationGenerator()
generatorBankRapport = FakeBankReport()
generatorCprNumber = FakeCprNumber()
generatorCreditCard = FakeCreditCard()


def generate_rapport(_):
    return generatorBankRapport.generate_report(num_transactions=5)

def generate_job_application(_, boolean = False):
    return generatorJobApplication.generate_application(num_employments=3, num_educations=2, num_references=2, sensitive= boolean)

def generate_ecommerce(_, boolean = False):
    return generatorEcommerce.generate_report(num_transactions=5, sensitive = boolean)

def generate_cprnumber(_):
    return {"cpr": generatorCprNumber.generate_cpr()}

def generate_creditcard(_):
    return {"credit card": generatorCreditCard.generate_creditcards()}

def write_to_csv(data_list, filename):
    if not data_list:  # Check if the list is empty
        return
    
    fieldnames = data_list[0].keys()
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()  
        for data in data_list:
            writer.writerow(data)


# Generate data and define number of cores
num_cores = 14
with Pool(num_cores) as pool:
    bankrapports_data = pool.map(generate_rapport, range(num_samples))
    jobApplications = pool.map(generate_job_application, range(num_samples))
    ecommerce = pool.map(generate_ecommerce, range(num_samples))
    cprnumbers = pool.map(generate_cprnumber, range(num_samples))
    creditcard = pool.map(generate_creditcard, range(num_samples / 7)) # alot of different credit type so we just divide it to make it lower, still equal of each type


write_to_csv(ecommerce, "data/generated_data/ecommerce_data.csv")
write_to_csv(bankrapports_data, "data/generated_data/bankrapports_data.csv")
jobapplicationfilename = "data/generated_data/jobapplication_data.csv"

write_to_csv(cprnumbers, "data/generated_data/sensitive/singlecprnumbers_data.csv")
write_to_csv(creditcard, "data/generated_data/sensitive/singlecreditcards_data.csv")

def flatten_application(app):
    """Flatten a job application tuple into a single dictionary."""
    personal_list, employments, educations, references = app
    personal = personal_list[0] if personal_list else {}  # Extract the dictionary from the list

    employment_data = {}
    for idx, employment in enumerate(employments, 1):
        prefix = f"employment_{idx}_"
        for key, value in employment.items():
            employment_data[prefix + key] = value

    education_data = {}
    for idx, education in enumerate(educations, 1):
        prefix = f"education_{idx}_"
        for key, value in education.items():
            education_data[prefix + key] = value

    references_data = {}
    for idx, reference in enumerate(references, 1):
        prefix = f"reference_{idx}_"
        for key, value in reference.items():
            references_data[prefix + key] = value

    combined_data = {**personal, **employment_data, **education_data, **references_data}
    return combined_data

# Flatten all job applications
flattened_applications = [flatten_application(app) for app in jobApplications]

# Write non-sensitive job applications to CSV
if flattened_applications:
    with open(jobapplicationfilename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=flattened_applications[0].keys())
        writer.writeheader()
        writer.writerows(flattened_applications)
