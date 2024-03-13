import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
import csv
import datetime

cred = credentials.Certificate("fbkeys.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
# db.collection("output").document("First_Name").set({"Name": "Gary"})

company_names = ["AAPL","AMZN","MSFT","TSLA","GOOG"]

# creating documents
for company in company_names:
    a = db.collection("output").document(company)
    a.set({
        "Name": 1234,
        "Date": "date goes here",
        "ESG": "ESG goes here",
        "Last_Update(UTC)": "blah"
    })
# READING / WRITING to documents
date = str((datetime.datetime.utcnow()).strftime("%Y-%m-%d"))
for company in company_names:
    with open("training_data.csv", 'r') as file:
        csvFile = csv.reader(file)
        a = db.collection("output").document(company)
        b = a.get().to_dict() # reading portion
        print("{Company}'s".format(Company = company),b['ESG'])
        for row in csvFile:
            if row[6] == company:
                a.update({ # writing portion
                    "Name": row[6],
                    "Date": row[5],
                    "ESG": row[7],
                    "Last_Update(UTC)": date
                })
            else:
                print("Company name dont match")

# 11/10/23
# write an algo to fetch each value of the CSV training 
# data file and write it to the DB