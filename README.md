### Project Description
A good way for fraudsters to convert stolen credit cards to cash is to create fake events on an events website, pay for all tickets to that event with stolen credit cards and then receive the payout.

My goal was to create a model to flag which transactions need further review. I essentially built a triage model of what the most pressing (and costly) transaction we have seen. I also deployed a web app to dynamically pull in live data, make predictions on the new data and present potentially fraudulent transactions with their probability scores from our model. The transactions were segmented into 3 groups: low risk, medium risk, or high risk (based on the probabilities).

#### Steps taken:
Exploratory data analysis to get a feel for the data (see fraud_detection_EDA.ipynb)

Feature engineering, NLP (Tfidf vecotrizing + random forest) on textual features and modeling of overall data (XGBoost). (See fraud_detection_feature_eng.ipynb)

Wrote a prediction script to dynamically pull in new data from a website, make predictions on the new data and add the new data point with its associated prediction to a MongoDb database. (see prediction_script.ipynb)

Deployed the web app to display results and be updated with new data points as they become available. (see app.py and templates/index.html)

Deployed the project on an Amazon Web Services EC2 instance

#### Screenshots of web app:

![Dashboard](/images/web_app1?raw=true "Dashboard")

![Dashboard](/images/web_app2?raw=true "Dashboard")

![Dashboard](/images/web_app3?raw=true "Dashboard")
