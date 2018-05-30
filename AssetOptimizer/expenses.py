import requests

def get_current_monthly_expense_prediction(monthly_salary):
    url = "http://dev.bambu.life:8081/api/TotalExpenseEstimator"
    querystring = {"monthly_income":str(monthly_salary)}

    response = requests.request("GET", url, params=querystring)

    return float(response.text)

def get_future_monthly_expense(monthly_expense, age, inflation_rate, retirement_goal_age):
    url = "http://dev.bambu.life:8081/api/MonthlyRetirementIncomeCalculator"
    querystring = {"monthly_expense": str(monthly_expense),
                   "age": str(age),
                   "inflation_rate": str(inflation_rate),
                   "retirement_age":str(retirement_goal_age)}

    response = requests.request("GET", url, params=querystring)

    return float(response.text)

# monthly_salary = 3000
# monthly_expense_prediction = get_current_monthly_expense_prediction(monthly_salary)
# future_monthly_expense = get_future_monthly_expense(monthly_expense_prediction, 18, 0.01, 55)
# print(future_monthly_expense)
