import requests
import json
import datetime
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot
import seaborn as sns

from .cpf import *
from .insurance import *
from .housing import *

def ra_chart(date_of_birth, monthly_salary, annual_bonus, age, current_bals):
    predicted_ra_balances_dict = calculate_ra_account_balances(date_of_birth, monthly_salary, annual_bonus, None, current_bals)
    min_cpf_sum = retrieveMinSum(date_of_birth)
    sns.set_context("talk")
    sns.set_style('darkgrid')

    plt.plot(predicted_ra_balances_dict.keys(), predicted_ra_balances_dict.values(), marker='.')
    plt.xlim(age, 55)
    plt.ylim(0, max(min_cpf_sum, predicted_ra_balances_dict[55]))
    plt.annotate(s=int(predicted_ra_balances_dict[55]), xy=(55, predicted_ra_balances_dict[55]))
    plt.xlabel('Age (years)')
    plt.ylabel('Predicted RA Amount')
    plt.fill_between(predicted_ra_balances_dict.keys(), predicted_ra_balances_dict.values(), alpha=0.5)
    plt.axhline(y = min_cpf_sum, color='gray', ls=':')

    plt.savefig('AssetOptimizer/static/foo.png', bbox_inches='tight', figsize=(8, 6))
    plt.close()

def ra_chart_2(predicted_ra_balances_dict, date_of_birth, age):
    min_cpf_sum = retrieveMinSum(date_of_birth)
    sns.set_context("talk")
    sns.set_style('darkgrid')

    plt.plot(predicted_ra_balances_dict.keys(), predicted_ra_balances_dict.values(), marker='.')
    plt.xlim(age, 55)
    plt.ylim(0, max(min_cpf_sum, predicted_ra_balances_dict[55]))
    plt.annotate(s=int(predicted_ra_balances_dict[55]), xy=(55, predicted_ra_balances_dict[55]))
    plt.xlabel('Age (years)')
    plt.ylabel('Predicted RA Amount')
    plt.fill_between(predicted_ra_balances_dict.keys(), predicted_ra_balances_dict.values(), alpha=0.5)
    plt.axhline(y = min_cpf_sum, color='gray', ls=':')

    plt.savefig('AssetOptimizer/static/foo2.png', bbox_inches='tight', figsize=(8, 6))
    plt.close()

def pie_chart(labels, values, years):

    plt.pie(values, labels=labels, radius=2, wedgeprops=dict(width=1, edgecolor='w'))
    plt.title("Average annual payments with CPF: $" + str(int(sum(values)/years)))
    plt.axis("equal")

    plt.savefig('AssetOptimizer/static/pie.png', bbox_inches='tight', figsize=(8, 6))
    plt.close()
