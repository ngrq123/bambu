import requests
import json

#Enhanced Income Shield Premium no output - Not doable (Unable to find nationality)
#Disability Income Premium no output
#Long Term Care Premium no output

def MedisaveLifePremium(age):
    url = "http://dev.bambu.life:8081/api/MedisaveLifePremiumCalculator/" + str(age)
    response = requests.request("GET", url)
    jsonStr = convertJsonMonthly(response)
    #print(jsonStr)
    return jsonStr

def PlusRiderPremium(age,plan):
    url = "http://dev.bambu.life:8081/api/PlusRiderPremiumCalculator/" + str(age) + "/" + plan
    response = requests.request("GET", url)
    jsonStr = convertJsonMonthly(response)
    #print(jsonStr)
    return jsonStr

def AssistRiderPremium(age,plan):
    url = "http://dev.bambu.life:8081/api/AssistRiderPremiumCalculator/" + str(age) + "/" + plan
    response = requests.request("GET", url)
    jsonStr = convertJsonMonthly(response)
    #print(jsonStr)
    return jsonStr

def CashRiderPremium(age,plan):
    url = "http://dev.bambu.life:8081/api/CashRiderPremiumCalculator/" + str(age) + "/" + plan
    response = requests.request("GET", url)
    jsonStr = convertJsonMonthly(response)
    #print(jsonStr)
    return jsonStr

#term must be at least 10 years
#gender must be male or female
def TermLifePremium(age,gender,term,sum_assured):
    url = "http://dev.bambu.life:8081/api/TermLifePremiumCalculator/" + str(age) + "/" + gender + "/" + str(term) + "/" + str(sum_assured)
    response = requests.request("GET", url)
    jsonStr = convertJsonPremium(response)
    #print(jsonStr)
    return jsonStr

#term must be at least 10 years
#gender must be male or female
def TermCIPremium(age,gender,term,sum_assured):
    url = "http://dev.bambu.life:8081/api/TermCIPremiumCalculator/" + str(age) + "/" + gender + "/" + str(term) + "/" + str(sum_assured)
    response = requests.request("GET", url)
    jsonStr = convertJsonPremium(response)
    #print(jsonStr)
    return jsonStr

def convertJsonMonthly(response):
    jsonData = json.loads(response.text)
    jsonData = jsonData[0]
    monthly_premium = jsonData['MonthlyPremium']
    return monthly_premium

def convertJsonPremium(response):
    jsonData = json.loads(response.text)
    print (jsonData)
    monthly_premium = jsonData['Premium']
    return monthly_premium

def countTotalPremiumAmount(age,gender,goalAge,plan,sum_assured,list):
    term = goalAge - age
    dictionary = {}
    for x in range(age,goalAge+1):
        totalAmount = 0
        if 1 in list:
            totalAmount += MedisaveLifePremium(x)
        if 2 in list:
            totalAmount += PlusRiderPremium(x,plan)
        if 3 in list:
            totalAmount += AssistRiderPremium(x,plan)
        if 4 in list:
            totalAmount += CashRiderPremium(x,plan)
        if 5 in list and term > 9 and term < 36:
                totalAmount += TermLifePremium(x,gender,term,sum_assured)
        if 6 in list and term > 9 and term < 36:
                totalAmount += TermCIPremium(x,gender,term,sum_assured)
        totalAmount *= 12
        dictionary[x] = totalAmount

    return dictionary


#MedisaveLifePremium(18)
#PlusRiderPremium(18,'Preferred')
#AssistRiderPremium(23,'Basic')
#CashRiderPremium(23,'Advantage')
#TermLifePremium(42,'Female',20,20000)
#TermCIPremium(52,'Male',20,20000)
# print(countTotalPremiumAmount(25, 'Male', 45, 'Preferred', 100000, [1, 3, 5]))
