import json
from datetime import date
from typing import List, Dict, Any
import os
import requests
from datetime import datetime
import pandas as pd

#CCR_API_KEY = "d_ca0b908cf06a267ca06acbd5feb4465c"
#AVR_API_KEY = "d_af61b90018b8fabecabe8e93950e0223"
#Unemployment_API_KEY = "d_e3598914c86699a9a36e68190f78c59a"


#checking if the inputed age is an integer
while True:
    age = input("How old are you (in years, decimal points are not accepted)? ")
    try:
        #if age is an integer break and continue with the program
        age = int(age)
        break
    except ValueError:
        #if it is not an integer ask again
        print("Please enter only positive integer values. ")

print(" ")

#this is the main url for all datasets from data.gov.sg
url = "https://data.gov.sg/api/action/datastore_search?resource_id="

#Average Life Expectancy Finder (from data.gov.sg, using an api key)
def averageLifeExpectancy(url):
    datasetId = "d_af61b90018b8fabecabe8e93950e0223"
    avr_life_e_url = url + datasetId
    avr_life_e = requests.get(avr_life_e_url)
    avr_life_e = avr_life_e.json()
    #obtaining value from the data, the path was found using a function (the one below)
    life_e = avr_life_e['result']['records'][1]['2022']
    return life_e


#assignment of remaining_years to the average life expectancy, which will be changed
remaining_years = int(float(averageLifeExpectancy(url))) - age


############################################################
#function used to find values and its path inside a dictionary
def find_value(avr_life_e, value):
    #combing through the multiple parts of the dictionary to find the value needed
    for record in avr_life_e['result']['records']:
        for key, val in record.items():
            if val == value:
                #if the value is found, return the key
                return f"The value '{value}' is located at data['result']['records'][{avr_life_e['result']['records'].index(record)}]['{key}']"
    #if the value is not found, return "not found"
    return f"The value '{value}' is not found in the dataset"


############################################################
#unemployment rate process

#using a function to access the data from api key
def unemploymentRate(url):
    datasetId = "d_e3598914c86699a9a36e68190f78c59a"
    unemployment_rate_url = url + datasetId
    unemployment_rate = requests.get(unemployment_rate_url)
    unemployment_rate = unemployment_rate.json()
    #obtaining value from the data, combing through the dictionary for the required item using a for loop
    for item in unemployment_rate['result']['records']:
        # Check if the year is 2023
        if item['year'] == '2023':
            # Print the unemployment rate
            ur = item['unemployment_rate']
            return ur


ur = unemploymentRate(url)
print(" ")

#user personal input if they are employed or not
while True:
    useru = input("Are you employed right now? (yes or no, lowcase) ")
    #checking if it is in the required format
    if useru == "yes" or useru == "no":
        #if it is, then continue on
        break
    else:
        #if it is not, ask again and tell user to input either yes or no
        print("Please enter either 'yes' or 'no'.")
        print(" ")

print(" ")

#conversion of api data returned to float (might be a decimal)
ur = float(ur)

#changing remaining_years based on the ur and useru values
if ur < 10 and ur > 5:
    remaining_years -= 1
elif ur > 10:
    remaining_years -= 2
elif ur < 5:
    remaining_years += 2

if useru == 'no':
    remaining_years -= 1

if useru == 'yes':
    remaining_years += 1
#############################################################smoke and drink process
#user input

#checking if smoke_time input is an integer, and if not, retrying
while True:
    smoke_time = input(
        "How many times do you smoke in a week (no. of sessions)? ")
    try:
        #if smoke_time is an integer break and continue with the program
        smoke_time = int(smoke_time)
        break
    except ValueError:
        #if it is not an integer ask again
        print("Please enter only positive integer values. ")

print(" ")
#converting to integer
smoke_time = int(smoke_time)

#changing remaining_years based on smoke_time
if smoke_time > 4:
    remaining_years -= 8
elif smoke_time < 4 and smoke_time > 2:
    remaining_years -= 4
elif smoke_time <= 2:
    remaining_years += 2

#input from user, converted to an integer
while True:
    drink_time = input(
        "How many times do you drink in a week (no. of sessions)? ")
    try:
        #if drink_time is an integer break and continue with the program
        drink_time = int(drink_time)
        break
    except ValueError:
        #if it is not an integer ask again
        print("Please enter only positive integer values. ")

print(" ")

#changing remaining_years based on drink_time
if drink_time == 0:
    remaining_years += 1
elif drink_time > 3:
    remaining_years -= 5
elif drink_time <= 3 and drink_time > 0:
    remaining_years -= 2
elif drink_time == 0:
    remaining_years += 1
##############################################################workout times process

#input from user, converted to an integer
while True:
    workout = input(
        "How many times do you workout in a week (no. of sessions)? ")
    try:
        #if workout is an integer break and continue with the program
        workout = int(workout)
        break
    except ValueError:
        #if it is not an integer ask again
        print("Please enter only positive integer values. ")

print(" ")

#adjusting remaining_years based on workout
if workout > 5:
    remaining_years += 4
elif workout <= 2 and smoke_time > 0:
    remaining_years += 1
elif workout <= 5 and workout > 2:
    remaining_years += 2
##############################################################ccr (crime and corruption)

#acquiring the data using an api key
datasetId = "d_ca0b908cf06a267ca06acbd5feb4465c"
url = "https://data.gov.sg/api/action/datastore_search?resource_id=" + datasetId

#getting the json dictionary
ccr_json = requests.get(url)
ccr_json = ccr_json.json()

#obtaining value from the data
#ccr means Crime and Corruption Rate
ccr = int(ccr_json['result']['records'][0]['2023'])

#finds the number of crimes divided by the total population, which allows me to find the per person rate of crime
ccr = ccr / 6040000

#finds crime rate per 10000 people
ccr = ccr * 10000

if ccr < 25:
    remaining_years += 3
if ccr > 25 and ccr < 50:
    remaining_years += 1
if ccr > 50:
    remaining_years -= 2
#############################################################

#input from user till where they have finished their education
while True:
    #el stands for education level
    el = input(
        "Education level: 1 - less than high school; 2 - high school diploma; 3 - university degree; 4 - post-graduate degree? "
    )
    try:
        #if el is an integer and in the range break and continue with the program
        el = int(el)
        if el == 1 or el == 2 or el == 3 or el == 4:
            break
    except ValueError:
        #if it is not an integer ask again
        print("Please enter only positive integer values. ")

print(" ")

#conversion to integer
el = int(el)

#adjusting remaining_years based on el
if el == 1:
    remaining_years -= 2
if el == 3:
    remaining_years += 2
if el == 4:
    remaining_years += 4

#############################################################
#input from user for percentage income they save every month

while True:
    per_inc = input(
        "Percentage of income you or your parents save every month (approximate); 1 - 20% or more, 2 - 15% to 20%, 3 - 5% to 15%, 4 - 0% - 5%: "
    )
    try:
        #if el is an integer and in the range break and continue with the program
        per_inc = int(per_inc)
        if per_inc == 1 or per_inc == 2 or per_inc == 3 or per_inc == 4:
            break
    except ValueError:
        #if it is not an integer ask again
        print("Please enter only positive integer values. ")

print(" ")

#conversion to integer
per_inc = int(per_inc)

#adjusting remaining_years based on per_inc
if per_inc == 1:
    remaining_years += 3
if per_inc == 2:
    remaining_years += 1
if per_inc == 4:
    remaining_years -= 2

#############################################################
#input from user for their height in meters and weight in kg
#input from user about their weight
while True:
    weight = input("What is your weight (in kg)? ")
    try:
        #if it is a float, then continue
        weight = float(weight)
        break
    except ValueError:
        #if it is not a float, ask again
        print("Please enter a valid weight. Use decimal point if needed.")

print(" ")

#input from user about their height
while True:
    height = input("What is your height (in metres)? ")
    try:
        height = float(height)
        break
    except ValueError:
        print("Please enter a valid height. Use decimal point if needed.")

print(" ")

#finding bmi using universally accepted formula
bmi = weight / (height * height)

#adjusting remaining_years based on bmi
if bmi < 18.5:
    remaining_years -= 3
if bmi > 18.5 and bmi < 25:
    remaining_years += 2
if bmi > 25 and bmi < 30:
    remaining_years -= 2
if bmi > 30:
    remaining_years -= 5

#############################################################
#input from user about their view on their general health

while True:
    health = input(
        "How do you view your general health? 1 - Terrible, 2 - Bad, 3 - Decent, 4 - Good, 5 - No issues at all: "
    )
    try:
        #if health is an integer and in the range break and continue with the program
        health = int(health)
        if health == 1 or health == 2 or health == 3 or health == 4 or health == 5:
            health = int(health)
            break
    except ValueError:
        #if it is not an integer ask again
        print("Please enter only positive integer values. ")

print(" ")

#conversion to integer
health = int(health)

#adusting remaining_years based on health
if health == 1:
    remaining_years -= 4
if health == 2:
    remaining_years -= 2
if health == 3:
    remaining_years += 1
if health == 4:
    remaining_years += 2
if health == 5:
    remaining_years += 4
#############################################################
print("\033[1m" + "----------------------------------")

print("You will live for,", remaining_years, "more years")

if remaining_years <= 0:
    print("You should be dead right now bro")

print(" ")
print("Your total life expectancy is, ", (remaining_years + age))
print(" ")
print("Please share if you enjoyed!")
print(" ")
print(
    "\033[1m" + "Disclaimer:" +
    "This life expectancy calculator is intended for informational and educational purposes only."
)
print(" ")
print(
    "The calculations provided are based on general statistical data and may not accurately predict individual outcomes. Numerous factors, such as genetics, lifestyle, and unforeseen events, can influence life expectancy and may not be fully accounted for in this tool. Please consult a healthcare professional for a comprehensive and personalized assessment."
)