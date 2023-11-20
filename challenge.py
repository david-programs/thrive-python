"""Thrive challenge written in Python"""

import json
from typing import  List

from models.company import Company
from models.user import User

with open("./input/companies.json", "r", encoding="utf-8") as companies_file:
    companies_json = json.load(companies_file)
with open("./input/users.json", "r", encoding="utf-8") as users_file:
    users_json = json.load(users_file)

# deserialize

# Create companies
companies : List[Company] = []
for company_json in companies_json:
    companies.append(Company(**company_json))

# company lookup
id_to_company = { company.id: company for company in companies }

# Create users, link to the companies
users : List[User] = []
for user_json in users_json:
    user = User(**user_json)
    users.append(user)

    if user.company_id not in id_to_company:
        print("COMPANY DOES NOT EXIST company_id:",  user.company_id)
    else:
        company = id_to_company[user.company_id]
        user.set_company(company)
        company.add_user(user)

# top up active users
for user in list(filter(lambda user: user.active_status, users)):
    user.top_up()

# attempt output
companies.sort(key=lambda x: x.id)
with open('./output/output.txt', 'wt', encoding="utf-8") as f:
    f.write('\n')
    for company in companies:
        if len(company.users) == 0:
            continue
        company_users = list(filter(lambda user: user.active_status, company.users))
        company_users.sort(key=lambda x: x.last_name)
        users_to_email = list(filter(lambda user: user.should_email(), company_users))
        users_to_not_email = list(filter(lambda user: not user.should_email(), company_users))

        f.write(f'\tCompany Id: {company.id}\n')
        f.write(f'\tCompany Name: {company.name}\n')
        f.write('\tUsers Emailed:\n')
        for user_to_email in users_to_email:
            f.write(f'\t\t{user_to_email.last_name}, {user_to_email.first_name}, {user_to_email.email}\n')
            f.write(f'\t\t  Previous Token Balance, {user_to_email.previous_balance()}\n')
            f.write(f'\t\t  New Token Balance {user_to_email.balance()}\n')
        f.write('\tUsers Not Emailed:\n')
        for user_to_not_email in users_to_not_email:
            f.write(f'\t\t{user_to_not_email.last_name}, {user_to_not_email.first_name}, {user_to_not_email.email}\n')
            f.write(f'\t\t  Previous Token Balance, {user_to_not_email.previous_balance()}\n')
            f.write(f'\t\t  New Token Balance {user_to_not_email.balance()}\n')
        f.write(f'\t\tTotal amount of top ups for {company.name}: {company.top_up_sum}\n')
        f.write('\n')
