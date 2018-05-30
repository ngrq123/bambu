from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from .forms import UserForm
from .insurance import *
from .charts import *
from .cpf import *
from .housing import *
import datetime

# Create your views here.
def index(request):
    return render(
        request,
        'index.html',
    )

def userinfo(request):
    form = UserForm(request.POST)
    getCharts(form)
    cpf_account_balances = getTotalAmount(form)
    # jsonStr = getMedisaveLife(form)
    date_of_birth = datetime.datetime(int(form['dob_year'].value()),int(form['dob_month'].value()),int(form['dob_day'].value()))
    return render(request, 'userinfo.html', {'housetype' : form['hdb'].value(),
                                                'cpf_min_sum': retrieveMinSum(date_of_birth),
                                                'cpf_account_balances': cpf_account_balances,
                                                'age': int(form['age'].value())})

#this method is called to process the getMedisaveLife value call
# def getMedisaveLife(form):
#     return MedisaveLifePremium(form['age'].value())

def getTotalAmount(form):
    age = int(form['age'].value())
    gender = form['gender'].value()
    goalAge = 55
    plan = form['plan'].value()
    sum_assured = float(form['sum'].value())
    date_of_birth = datetime.datetime(int(form['dob_year'].value()),int(form['dob_month'].value()),int(form['dob_day'].value()))
    month_salary = float(form['salary'].value())
    bonus = float(form['bonus'].value())
    investment = int(form['investment'].value())

    dictionaryOne = countTotalPremiumAmount(age,gender,goalAge,plan,sum_assured,[1,2,3,4])
    minCPFSum = retrieveMinSum(date_of_birth)
    current_bals = (float(form['cab'].value()),float(form['mab'].value()),float(form['sab'].value()))
    dictionaryTwo = calculate_mortgage_cpf_payments(float(form['houseAmount'].value()),int(form['yearsToGo'].value())*12,int(form['ahdb'].value()),float(form['dpp'].value()))
    aatd = merge_expenses(dictionaryOne, dictionaryTwo)
    dictionaryThree = calculate_ra_account_balances(date_of_birth,month_salary,bonus,aatd,current_bals,goalAge)
    ra_chart_2(dictionaryThree, datetime.datetime(int(form['dob_year'].value()),int(form['dob_month'].value()),int(form['dob_day'].value())), int(form['age'].value()))

    return calculate_cpf_account_balances(date_of_birth,month_salary,bonus,aatd,current_bals,goalAge)

def getCharts(form):
    age = int(form['age'].value())
    gender = form['gender'].value()
    goalAge = 55
    plan = form['plan'].value()
    sum_assured = float(form['sum'].value())
    date_of_birth = datetime.datetime(int(form['dob_year'].value()),int(form['dob_month'].value()),int(form['dob_day'].value()))
    month_salary = float(form['salary'].value())
    bonus = float(form['bonus'].value())
    investment = int(form['investment'].value())

    current_bals = (float(form['cab'].value()),float(form['mab'].value()),float(form['sab'].value()))
    ra_chart(datetime.datetime(int(form['dob_year'].value()),int(form['dob_month'].value()),int(form['dob_day'].value())), form['salary'].value(), form['bonus'].value(), int(form['age'].value()), current_bals)

    labels = ['Housing', 'Insurance', 'Investments']
    mortgage_payments_dict = calculate_mortgage_cpf_payments(float(form['houseAmount'].value()), int(form['yearsToGo'].value())*12, int(form['ahdb'].value()))
    insurance_payments_dict = calculate_mortgage_cpf_payments(float(form['houseAmount'].value()),int(form['yearsToGo'].value())*12,int(form['ahdb'].value()),float(form['dpp'].value()))
    values = [sum(mortgage_payments_dict.values()), sum(mortgage_payments_dict.values()), investment]

    aatd = merge_expenses(mortgage_payments_dict, insurance_payments_dict)
    years = goalAge - age

    pie_chart(labels, values, years)
