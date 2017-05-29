import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import cPickle as pickle
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from string import punctuation

def prep_data(df_fraud):

    df_fraud['event_duration'] = (df_fraud.event_end - df_fraud.event_start)/3600.

    with open('pickle/top_domains.pkl', 'rb') as f:
        top_domains = pickle.load(f)
    for i,row in enumerate(df_fraud.email_domain):
        if row not in top_domains:
            df_fraud.ix[i, 'email_domain'] = 'other'

    for index, row in df_fraud.iterrows():
        if len(row['payee_name']) == 0:
            df_fraud.ix[index, 'payee_name'] = 0
        else:
            df_fraud.ix[index, 'payee_name'] = 1
        if len(row['payout_type']) == 0:
            df_fraud.ix[index, 'payout_type'] = 'not_available'
    df_fraud['payee_name'] = df_fraud['payee_name'].astype(float)

    for index, row in df_fraud.iterrows():
        df_fraud.ix[index,'types_count'] = len(row['ticket_types'])
        df_fraud.ix[index,'min_price'] = min([j['cost'] for j in row['ticket_types']] or [0])
        df_fraud.ix[index,'max_price'] = max([j['cost'] for j in row['ticket_types']] or [0])
        df_fraud.ix[index,'quantity_sold'] = sum([j['quantity_sold'] for j in row['ticket_types']] or [0])
        df_fraud.ix[index,'quantity_total'] = sum([j['quantity_total'] for j in row['ticket_types']] or [0])
        df_fraud.ix[index,'value_sold'] = sum([j['quantity_sold']*j['cost'] for j in row['ticket_types']] or [0])
        df_fraud.ix[index,'value_total'] = sum([j['quantity_total']*j['cost'] for j in row['ticket_types']] or [0])

        df_fraud.ix[index,'payout_count'] = len(row['previous_payouts'])
        try:
            df_fraud.ix[index,'avg_payout'] = sum([j['amount'] for j in row['previous_payouts']] or [0]) / len(row['previous_payouts'])
        except:
            df_fraud.ix[index,'avg_payout'] = 0


    for index, row in df_fraud.iterrows():
        try:
            df_fraud.ix[index,'weighted_price'] = row['value_total'] / row['quantity_total']
        except:
            df_fraud.ix[index,'weighted_price'] = 0

    df_fraud = df_fraud.drop(['event_end', 'event_start', 'object_id',
                          'venue_name','venue_address', 'user_created',
                         'venue_latitude', 'venue_longitude', 'ticket_types',
                         'previous_payouts'],axis=1)

    with open('pickle/encode.pkl') as f:
        encode = pickle.load(f)
    for column in ['country', 'currency', 'email_domain', 'listed', 'payout_type',
              'venue_country', 'venue_state']:
        df_fraud[column] = encode[column].transform(df_fraud[column])

    with open('pickle/tfidf-description.pkl') as f:
        tfidf_description = pickle.load(f)
    with open('pickle/rfmodel-description.pkl') as f:
        rf_description = pickle.load(f)
    df_fraud['description']= rf_description.predict_proba(tfidf_description.transform(df_fraud['description']))[:,1]

    with open('pickle/tfidf-name.pkl') as f:
        tfidf_name = pickle.load(f)
    with open('pickle/rfmodel-name.pkl') as f:
        rf_name = pickle.load(f)
    df_fraud['name']= rf_name.predict_proba(tfidf_name.transform(df_fraud['name']))[:,1]

    with open('pickle/tfidf-org_name.pkl') as f:
        tfidf_org_name = pickle.load(f)
    with open('pickle/rfmodel-org_name.pkl') as f:
        rf_org_name = pickle.load(f)
    df_fraud['org_name']= rf_org_name.predict_proba(tfidf_org_name.transform(df_fraud['org_name']))[:,1]

    with open('pickle/tfidf-org_desc.pkl') as f:
        tfidf_org_desc = pickle.load(f)
    with open('pickle/rfmodel-org_desc.pkl') as f:
        rf_org_desc = pickle.load(f)
    df_fraud['org_desc']= rf_org_desc.predict_proba(tfidf_org_desc.transform(df_fraud['org_desc']))[:,1]

    return df_fraud, df_fraud.values

def tokenize(doc):
    bs = BeautifulSoup(doc.encode('ascii','ignore'))
    document = bs.text
    wordnet_lemmatizer = WordNetLemmatizer()
    stops = stopwords.words('english')
    sp = set(punctuation)
    sp.add('``')
    sp.add("''")
    texts = [word for word in document.lower().split() if word not in sp]
    texts = [word for word in texts if word not in stops]
    texts = [wordnet_lemmatizer.lemmatize(word) for word in texts]
    return texts
