from flask import Flask, render_template, request, redirect
from flask.ext.sqlalchemy import SQLAlchemy
import os
import pickle
from sklearn.feature_extraction import DictVectorizer

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)
loan_accept_rfc_model = pickle.load(open('data/loan_accept_rfc.pkl', 'r'))
vect = pickle.load(open('data/dict_vectorizer.pkl', 'r'))

from models import *

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
  if request.method == 'POST':
    sample = {}
    # sample['loan_amount'] = float(request.form['loan_amount'])
    # sample['debt_to_income'] = float(request.form['debt_to_income'])
    # sample['zip_code'] = request.form['zip_code']
    # sample['address_state'] = request.form['address_state']
    # sample['employment_length'] = float(request.form['employment_length'])

    sample[0] = float(request.form['loan_amount'])
    sample[1] = float(request.form['debt_to_income'])
    sample['3=' + request.form['address_state']] = 1.0
    sample['2=' + request.form['zip_code']] = 1.0
    sample[4] = float(request.form['employment_length'])
    sample = [sample]
    print sample
    sample = vect.transform(sample)

    print sample

    print loan_accept_rfc_model.predict(sample)

    return redirect('/')



if __name__ == '__main__':
    app.run()
