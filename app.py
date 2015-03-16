from flask import Flask, render_template, request, redirect, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
import os
import pickle
from sklearn.feature_extraction import DictVectorizer

app = Flask(__name__)
db = SQLAlchemy(app)

loan_accept_rfc_model = pickle.load(open('data/loan_accept_rfc.pkl', 'r'))
vect = pickle.load(open('data/dict_vectorizer.pkl', 'r'))

from models import *

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/predict', methods=['GET'])
def predict():
  if request.method == 'GET':
    sample = {}
    sample[0] = float(request.args.get('loan_amount'))
    sample[1] = float(request.args.get('debt_to_income'))
    sample['3=' + request.args.get('address_state')] = 1.0
    sample['2=' + request.args.get('zip_code') + "xx"] = 1.0
    sample[4] = float(request.args.get('employment_length'))
    sample = [sample]

    print sample

    sample = vect.transform(sample)

    print sample

    pred = loan_accept_rfc_model.predict(sample)

    if pred[0] == None:
        res = 'N/A'
    elif pred[0] == 1:
        res = 'Accepted'
    else:
        res = 'Rejected'

    return jsonify(result=res)



if __name__ == '__main__':
    app.run()
