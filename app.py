from flask import Flask
from flask import render_template, request
import cPickle as pickle
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from string import punctuation
from xgboost import XGBClassifier
from sklearn.cross_validation import train_test_split
import pymongo
from pymongo import MongoClient
from fraud_detection_feature_eng import tokenize, prep_data
import requests
import json
from prediction_script import feed_db, prediction
import ast
from datetime import date
from plots import make_plot_code

app = Flask(__name__)

@app.route('/')
def index():
    json_output, df = prediction()
    div, script, css, js = make_plot_code(df)
    return render_template('index.html',output=json_output, div_code=div, script_code=script, css_code=css, js_code=js)

if __name__ == '__main__':
    client = MongoClient()
    db = client.fraud_detector
    table = db.fraud_table
    app.run(host='0.0.0.0', debug=True, port=8080)
