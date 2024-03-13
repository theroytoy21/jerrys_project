from flask import Flask, jsonify
from google.cloud.storage import blob
from firebase_admin import credentials, initialize_app, storage, auth, firestore

import datetime
import csv
from sentiment_2 import prediction

app = Flask(__name__)

cred = credentials.Certificate("fbkeys.json")
initialize_app(cred, {'storageBucket': 'esg-project-2c7e3.appspot.com'})
bucket = storage.bucket()
db = firestore.client()

@app.route('/upload')
def upload_file():
  # Put your local file path
  fileName = "training_data.csv"
  blob = bucket.blob(str((datetime.datetime.utcnow()).strftime("%Y-%m-%d")))
  blob.upload_from_filename(fileName)

  x = [10, "neutral", 1, 1, 8, "AAPL"]
  pred = prediction(x)
  return jsonify(str(pred))


# this will download csv files
@app.route('/dl')
def dl():
  target = bucket.list_blobs()
  blobList = list(iter(target))
  for x in blobList:
    x.download_to_filename("training_data" + ".csv")
  return "File has been downloaded."


@app.route('/hello')
def test_method():
  company_ref = db.collection("output").stream()
  list = []
  for doc in company_ref:
    # print(f"{doc.id} => {doc.to_dict()}")
    print(doc.to_dict())
    x = doc.to_dict()
    list.append(x['ESG'])
  return jsonify(list)


@app.route('/hello2')
def test_method2():
  company_ref = db.collection("output").stream()
  str = ""
  for doc in company_ref:
    # print(f"{doc.id} => {doc.to_dict()}")
    str += doc.id + ","
  return jsonify(str)


# writes to firebase DB
@app.route('/write')
def write():
  company_names = ["AAPL", "AMZN", "MSFT", "TSLA", "GOOG"]

  # creating documents
  for company in company_names:
    a = db.collection("output").document(company)
    a.set({
        "Name": 1234,
        "Date": "date goes here",
        "ESG": "ESG goes here",
        "Last_Update": "blah"
    })
  # READING / WRITING to documents
  date = str((datetime.datetime.utcnow()).strftime("%Y-%m-%d"))
  for company in company_names:
    with open("training_data.csv", 'r') as file:
      csvFile = csv.reader(file)
      a = db.collection("output").document(company)
      b = a.get().to_dict()  # reading portion
      print("{Company}'s".format(Company=company), b['ESG'])
      for row in csvFile:
        if row[6] == company:
          a.update({  # writing portion
              "Name": row[6],
              "Date": row[5],
              "ESG": row[7],
              "Last_Update": date
          })
        else:
          print("Company name dont match")

  return jsonify("Wrote to database.")


if __name__ == '__main__':
  app.run(host='0.0.0.0')
