import requests
import json
import datetime
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def retrieveMinSum(date_of_birth):
    # date_turning_55: datetime.datetime object
    # Returns minimum CPF sum: int

    date_turning_55 = datetime.datetime(date_of_birth.year + 55, date_of_birth.month, date_of_birth.day)

    # 55th birthday on or after 1 July for 2003 to 2015, and
    # 1 January from 2017 onwards (no date for 2016)
    retirement_sums_dict = {2002: 0,
                            2003: 80000,
                            2004: 84500,
                            2005: 90000,
                            2006: 94600,
                            2007: 99600,
                            2008: 106000,
                            2009: 117000,
                            2010: 123000,
                            2011: 131000,
                            2012: 139000,
                            2013: 148000,
                            2014: 155000,
                            2015: 161000,
                            2016: 161000,
                            2017: 166000,
                            2018: 171000,
                            2019: 176000,
                            2020: 181000}

    min_cpf_sum = min_cpf_sum = retirement_sums_dict[2020]
    if date_turning_55.year < 2003:
        # Before 2003
        min_cpf_sum = 0
    elif date_turning_55.year < 2017:
        # Between 2003 to 2017
        # Check if before or after July
        if date_turning_55.month < 7:
            # Added 2002 in dictionary for corner case where 55th birthday is on 2003 but before July
            min_cpf_sum = retirement_sums_dict[date_turning_55.year - 1]
        else:
            min_cpf_sum = retirement_sums_dict[date_turning_55.year]
    elif date_turning_55.year < 2020:
            min_cpf_sum = retirement_sums_dict[date_turning_55.year]

    return min_cpf_sum

def get_current_age(date_of_birth):
    # date_of_birth: datetime.datetime object
    # Returns age: int
    return datetime.datetime.today().year - date_of_birth.year

def get_annual_CPF_contribution(date_of_birth, monthly_salary, age, annual_bonus=0):
    # date_of_birth: datetime.datetime object
    # monthly_salary: number
    # annual_bonus (optional): number, default 0
    # age (optional): numberm, default current age
    # Returns CPF contribution: number

    # Invoke Non-Pension CPF Contribution Calculator
    url = "http://dev.bambu.life:8081/api/CPFContributionCalculator/NonPension"
    querystring = {"date_of_birth": str(date_of_birth.month).zfill(2) + "-" +
                                       str(date_of_birth.day).zfill(2) + "-" +
                                       str(datetime.datetime.today().year - age),
                   "ordinary_wage": monthly_salary,
                   "additional_wage": annual_bonus,
                   "non_pensionable_element": "0"}
    # print(querystring)
    response = requests.request("GET", url, params=querystring)
    response = json.loads(response.text)
    return response[0]['TotalCPFContribution'] * 12

def get_annual_CPF_allocation(cpf_contribution, date_of_birth, age):
    # cpf_contribution: number
    # date_of_birth: datetime.datetime object
    # age (optional): numberm, default current age
    # Returns allocation by account (OA, MA, SA): tuple

    # Invoke Non-Pension CPF Allocation Calculator
    url = "http://dev.bambu.life:8081/api/CPFAllocationCalculator/NonPension"
    querystring = {"date_of_birth": str(date_of_birth.month).zfill(2) + "-" +
                                       str(date_of_birth.day).zfill(2) + "-" +
                                       str(datetime.datetime.today().year - age),
                   "cpf_contribution": cpf_contribution}
    response = requests.request("GET", url, params=querystring)
    # Calculate amount eligible to be transferred to retirement account
    response = json.loads(response.text)
    oa_ma_sa_tuple = (response[0]['OrdinaryAccount'], response[0]['Medisave'], response[0]['SpecialAccount'])

    return oa_ma_sa_tuple

def calculate_cpf_account_balances(date_of_birth,
                                   monthly_salary,
                                   annual_bonus=0,
                                   age_amount_to_deduct=None,
                                   current_balances=(0, 0, 0),
                                   goal_age=55):
    # date_of_birth: datetime.datetime object
    # monthly_salary: number
    # annual_bonus (optional): number, default: 0
    # age_amount_to_deduct (optional): dictionary of age and amounts to deduct in OA, default: None (null)
    # goal_age: number, age to retire, default: 55
    # Returns cpf allocation by age (int) by account [(OA, MA, SA) - tuple]: dictionary

    age = get_current_age(date_of_birth)
    cpf_contribution = get_annual_CPF_contribution(date_of_birth, monthly_salary, age, annual_bonus)
    oa_ma_sa_tuple = get_annual_CPF_allocation(cpf_contribution, date_of_birth, age)

    predicted_cpf_balances_dict = {0: (0, 0, 0),
                                  age-1: (0, 0, 0),
                                  age: current_balances}

    for i in range(age+1, goal_age+1):

        if i in [56, 61, 66]:
            # Recalculate CPF contribution
            cpf_contribution = get_annual_CPF_contribution(date_of_birth, monthly_salary, annual_bonus, age=i)

        if i in [36, 46, 51, 56, 61, 66]:
            # Recalculate CPF allocation
            oa_ma_sa_tuple = get_annual_CPF_allocation(cpf_contribution, date_of_birth, age=i)

        amount_to_deduct = 0

        if age_amount_to_deduct != None:
            amount_to_deduct = age_amount_to_deduct[i]

        previous_oa_ma_sa_tuple = predicted_cpf_balances_dict[i - 1]
        predicted_cpf_balances_dict[i] = (previous_oa_ma_sa_tuple[0] + oa_ma_sa_tuple[0] - amount_to_deduct,
                                          previous_oa_ma_sa_tuple[1] + oa_ma_sa_tuple[1],
                                          previous_oa_ma_sa_tuple[2] + oa_ma_sa_tuple[2])
        if predicted_cpf_balances_dict[i][0] < 0:
            predicted_cpf_balances_dict[i] = (0, predicted_cpf_balances_dict[i][1], predicted_cpf_balances_dict[i][2])
        # print(predicted_cpf_balances_dict[i])

    return predicted_cpf_balances_dict

def calculate_ra_account_balances(date_of_birth,
                                  monthly_salary,
                                  annual_bonus=0,
                                  age_amount_to_deduct=None,
                                  current_balances=(0, 0, 0),
                                  goal_age=55):
    # date_of_birth: datetime.datetime object
    # monthly_salary: number
    # annual_bonus (optional): number, default: 0
    # age_amount_to_deduct (optional): dictionary of age and amounts to deduct in OA, default None (null)
    # goal_age: number, age to retire, default: 55
    # Returns predicted RA account balance (number) by age (int): dictionary

    predicted_ra_balances_dict = calculate_cpf_account_balances(date_of_birth,
                                                                monthly_salary,
                                                                annual_bonus=annual_bonus,
                                                                age_amount_to_deduct=age_amount_to_deduct,
                                                                current_balances=current_balances,
                                                                goal_age=goal_age)

    for i in predicted_ra_balances_dict.keys():
        predicted_ra_balances_dict[i] = (predicted_ra_balances_dict[i][0] +
                                         predicted_ra_balances_dict[i][2])

    return predicted_ra_balances_dict

def merge_expenses(dictionary1, dictionary2):
    merged = dictionary1.copy()
    for key in dictionary2.keys():
        try:
            merged[key] = dictionary1[key] + dictionary2[key]
        except KeyError:
            merged[key] = dictionary2[key]
    return merged

# date_of_birth = datetime.datetime(1995, 9, 8)
# monthly_salary = 10000
# annual_bonus = 15000
#
# cpf_min_sum = retrieveMinSum(date_of_birth)
# age = get_current_age(date_of_birth)
# cpf_contribution = get_annual_CPF_contribution(date_of_birth, monthly_salary, age, annual_bonus)
# cpf_allocation = get_annual_CPF_allocation(cpf_contribution, date_of_birth, age)
# cpf_account_balances = calculate_cpf_account_balances(date_of_birth, monthly_salary, annual_bonus)
# ra_account_balances = calculate_ra_account_balances(date_of_birth, monthly_salary, annual_bonus)
#
# print(date_of_birth)
# print(monthly_salary)
# print(cpf_min_sum)
# print(age)
# print(cpf_contribution)
# print(cpf_allocation)
# print(cpf_account_balances)
# print(ra_account_balances)
# print(merge_expenses({30: 2, 31: 5}, {31: 10, 35: 9}))
