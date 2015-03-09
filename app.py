from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
import os
import pickle

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)
loan_accept_rfc_model = pickle.load(open('data/loan_accept_rfc.pkl', 'r'))
loan_quality_rfc_model = pickle.load(open('data/loan_quality_rfc.pkl', 'r'))

from models import *

@app.route('/')
def hello():
    print loan_accept_rfc_model
    print loan_quality_rfc_model
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
