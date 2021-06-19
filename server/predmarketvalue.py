import csv
import os
import pandas as pd
from collections import defaultdict
import random as rd
def getPAIRS():
    data = pd.read_csv("stockmarket.csv")
    data=data.dropna(axis=1,how='all')
    #print(data.head())

    predpair = {}
    itemhead = data.columns.values
    companytype=['Commercial Services','Communications','Consumer Durables','Consumer Non-Durables','Consumer Services','Distribution Services',
        'Electronic Technology','Energy Minerals','Finance','Health Services','Health Technology','Industrial Services','Miscellaneous',
        'Non-Energy Minerals','Process Industries','Producer Manufacturing','Retail Trade','Technology Services','Transportation','Utilities']
    #print(itemhead[15])

    #print(data[itemhead[0]])
    result = ['Risky','Normal','Potential']
    count = 0
    for x in data[itemhead[15]]:
        if(count < 20):
            # print(x)
            predpair[companytype[count]] = x
            count+=1

    return predpair


def VerifyMarket(companyType):
    companytype=['Commercial Services','Communications','Consumer Durables','Consumer Non-Durables','Consumer Services','Distribution Services',
    'Electronic Technology','Energy Minerals','Finance','Health Services','Health Technology','Industrial Services','Miscellaneous',
    'Non-Energy Minerals','Process Industries','Producer Manufacturing','Retail Trade','Technology Services','Transportation','Utilities']

    mypair = getPAIRS()
    
    return evaluate(mypair[companyType])


def evaluate(results):
    risk = 0
    if(results == 'Risky'):
        risk = 90
    elif(results == 'Normal '):
        risk = 60
    elif(results == 'Potential'):
        risk = 10
    return risk





