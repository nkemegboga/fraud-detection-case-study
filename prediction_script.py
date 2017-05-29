import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import cPickle as pickle
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
import ast
from datetime import date

client = MongoClient()
db = client.fraud_detector
table = db.fraud_table

def feed_db(df, probabilities, table):
    df_data = pd.concat(objs = [df, pd.DataFrame(probabilities, columns=['fraud_probability'])], axis=1)
    df_data = df_data.T.to_dict().values()
    table.insert(df_data)
def prediction():
    col_names = [u'approx_payout_date',u'body_length',u'channels',u'country',u'currency',u'delivery_method',u'description',u'email_domain',u'event_created',u'event_end',u'event_published',u'event_start',u'fb_published',u'gts',u'has_analytics',u'has_header'
    ,u'has_logo',u'listed',u'name',
    u'name_length',u'num_order',u'num_payouts',u'object_id',u'org_desc',u'org_facebook',u'org_name',u'org_twitter',u'payee_name',u'payout_type',u'previous_payouts',u'sale_duration',u'sale_duration2',u'show_map',u'ticket_types',u'user_age',u'user_created',u'user_type',u'venue_address',u'venue_country'
    ,u'venue_latitude',u'venue_longitude',u'venue_name',u'venue_state']

    html = requests.get('http://galvanize-case-study-on-fraud.herokuapp.com/data_point')
    fraud_dict = html.json()

    df = pd.DataFrame(columns=col_names)
    df = df.append(fraud_dict, ignore_index=True)

    df_, X_data = prep_data(df)
    with open('pickle/model.pkl') as f:
        model = pickle.load(f)
    probabilities = model.predict_proba(X_data)[:,1]
    feed_db(df, probabilities, table)

    lisst_ = []
    for i in db.fraud_table.find( {}, { 'org_name': 1, 'name': 1, 'event_start' : 1, 'event_created':1, 'country' : 1 ,'object_id':1, '_id':0, 'fraud_probability':1 }):
        i = ast.literal_eval(json.dumps(i))
        i['event_created'] = date.fromtimestamp(int(i['event_created'])).__str__()
        i['event_start'] = date.fromtimestamp(int(i['event_start'])).__str__()
        if i['fraud_probability'] > 0.9:
            i['risk'] = 'High'
            i['style'] = "<td style='background-color: #FF9999'>"
        elif i['fraud_probability'] < 0.01:
            i['risk'] = 'Low'
            i['style'] = "<td style='background-color: #ADDEAD'>"
        else:
            i['risk'] = 'Medium'
            i['style'] = "<td style='background-color: #b0eaf6'>"
        lisst_.append(i)

    lisst_1 = []
    return lisst_[::-1], pd.concat(objs = [df_, pd.DataFrame(probabilities, columns=['fraud_probability'])], axis=1)
