import requests
import json
import datetime
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def calculate_mortgage(house_amount, months_to_go, downpayment_pct=0.1):
    url = "http://microservice.dev.bambu.life/api/generalCalculator/mortgageCalculators"
    payload = {"houseAmount":str(house_amount),
               "downpaymentPct":str(downpayment_pct),
               "monthsToGo":str(months_to_go)}

    response = requests.request("POST", url, data=payload)
    response = json.loads(response.text)
    return response['response']

def calculate_mortgage_downpayment(house_amount, months_to_go, downpayment_pct=0.1):
    response = calculate_mortgage(house_amount=house_amount, months_to_go=months_to_go, downpayment_pct=downpayment_pct)
    return response['downpayment']

def calculate_mortgage_min_monthly_payment(house_amount, months_to_go, downpayment_pct=0.1):
    response = calculate_mortgage(house_amount=house_amount, months_to_go=months_to_go, downpayment_pct=downpayment_pct)
    return response['minMonthlyPayment']

def calculate_mortgage_cpf_payments(house_amount, months_to_go, age_to_buy, downpayment_pct=0.1):
    downpayment = calculate_mortgage_downpayment(house_amount, months_to_go)
    minMonthlyPayment = calculate_mortgage_min_monthly_payment(house_amount, months_to_go)

    capCPF = 1.2 * house_amount
    totalAmount = downpayment + minMonthlyPayment * months_to_go

    from collections import defaultdict
    payment = {}

    years_to_go = int(months_to_go / 12)
    payment[age_to_buy] = downpayment * 0.75

    for i in range(0, years_to_go - 1):
        for j in range(1, 12):
            payment[i + age_to_buy] = payment.get(i + age_to_buy, 0) + minMonthlyPayment
            capCPF = capCPF - minMonthlyPayment

            if capCPF < 0:
                break
        # print (capCPF)
        if capCPF < 0:
            break

    return payment

# house_amount = 500000
# years_to_go = 30
# months_to_go = years_to_go * 12
# age_to_buy = 30
#
# mortgage = calculate_mortgage(house_amount, months_to_go)
# downpayment = calculate_mortgage_downpayment(house_amount, months_to_go)
# min_monthly_payment = calculate_mortgage_min_monthly_payment(house_amount, months_to_go)
# payments = calculate_mortgage_cpf_payments(house_amount, months_to_go, age_to_buy)
#
# print(mortgage)
# print(downpayment)
# print(min_monthly_payment)
# print(payments)
