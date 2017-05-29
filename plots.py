import pandas as pd
import numpy as np
import json
import ast

from bokeh.plotting import figure, show
from bokeh.embed import components
from bokeh.resources import CDN
import cPickle as pickle

def make_plot_code(df):
    fraud_file = pd.read_csv('plots/graphfraud.csv')
    not_fraud_file = pd.read_csv('plots/graphnotfraud.csv')
    df = df.drop(['has_header'],axis=1)
    with open('plots/pca.pkl') as f:
        pca = pickle.load(f)

    with open('plots/scaler.pkl') as f:
        scaler = pickle.load(f)
    print df.values
    try:
        df_ = df.fillna(0.)
        x = pca.transform(scaler.transform(df_.values))
    except:
        try:
            df_ = df.fillna(0)
            x = pca.transform(scaler.transform(df_.values))
        except:
            df_ = df.fillna(str(0))
            x = pca.transform(scaler.transform(df_.values))

    p = figure(title="Fraud Visualization", plot_width=400, plot_height=400)
    p.background_fill_color = "#eeeeee"

    p.scatter(not_fraud_file.values[:,0],not_fraud_file.values[:,1],marker='triangle',color='orange',legend='Not Fraud')
    p.scatter(fraud_file.values[:,0],fraud_file.values[:,1],marker='circle',color='red',legend='Fraud')
    p.scatter(x[0,0],x[0,1],color='blue',legend='Most recent event',marker='square',size=10)

    script, div = components(p)

    div = ast.literal_eval(json.dumps(div)).replace('\n', "")
    script = ast.literal_eval(json.dumps(script)).replace('\n', "")
    css = CDN.render_css()
    css = ast.literal_eval(json.dumps(css)).replace('\n', "")
    js = CDN.render_js()
    js = ast.literal_eval(json.dumps(js)).replace('\n', "")
    return div, script, css, js
