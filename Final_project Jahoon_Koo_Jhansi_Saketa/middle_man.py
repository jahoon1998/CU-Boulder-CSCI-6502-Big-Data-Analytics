################################################################
# CSCI 6502 - Jahoon Koo, Jhansi Saketa
# middle_man.py
# This file receives stock quotes and Twitter polarity from Google Cloud PubSub.
# Once it receives incoming data, it normalizes data first and sends nomalized data 
# to AI platform to get predicted stock price. Then, it appends predicted stock price
# to a BigQuery table.  
################################################################

import os
import pytz
import time
import datetime
from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from google.api_core.client_options import ClientOptions
from oauth2client.client import GoogleCredentials
import googleapiclient.discovery
from google.cloud import bigquery

timeout = 5.0                                                                       # timeout in seconds
subscriber = pubsub_v1.SubscriberClient()
subscription_path = 'projects/noble-airport-343004/subscriptions/stock_market_prediction-sub'

endpoint = 'https://us-central1-ml.googleapis.com'
client_options = ClientOptions(api_endpoint=endpoint)
service = googleapiclient.discovery.build('ml', 'v1', client_options=client_options)

def predict_json(instances):
    """Send json data to a deployed model for prediction.

    Args:
        project (str): project where the AI Platform Model is deployed.
        model (str): model name.
        instances ([Mapping[str: Any]]): Keys should be the names of Tensors
            your deployed model expects as inputs. Values should be datatypes
            convertible to Tensors, or (potentially nested) lists of datatypes
            convertible to tensors.
        version: str, version of the model to target.
    Returns:
        Mapping[str: any]: dictionary of prediction results defined by the
            model.
    """
    project="noble-airport-343004"
    model="lstm"
    version="first_version"
    name = 'projects/{}/models/{}'.format(project, model)
    if version is not None:
        name += '/versions/{}'.format(version)

    response = service.projects().predict(
        name=name,
        body={'instances': instances}
    ).execute()
    # print(response['predictions'])
    if 'error' in response:
        raise RuntimeError(response['error'])

    return response['predictions']

def bigquery_insert(date, price):
    # Construct a BigQuery client object.
    client = bigquery.Client()
    table_id = "noble-airport-343004.stock_prediction.apple"
    rows_to_insert = [
        {"date": date, "price": price}
    ]
    errors = client.insert_rows_json(table_id, rows_to_insert)  # Make an API request.
    if errors == []:
        print("New rows have been added.")
    else:
        print("Encountered errors while inserting rows: {}".format(errors))
        
def min_max_nomalization (date, open, high, low, close, adj_close, ts_polarity):
    features = ["Open", "High",	"Low",	"Adj Close", "Close",	"ts_polarity"]

    hourly_data =  {'Date': [date], 'Open': [open], 'High':[high], 'Low':[low], 
                'Close':[close], 'Adj Close':[adj_close],'ts_polarity': [ts_polarity]}  
    hourly_data = pd.DataFrame(hourly_data)  

    # min max value needed for normalization
    min_max_data =  {'Date': ['1/1/2022 11:30 - 12:30', '1/1/2022 12:30 - 13:30'], 'Open': [71.325, 200], 'High':[72.64848, 200], 'Low':[70.90498, 200], 
                  'Close':[71.59445,200], 'Adj Close':[66.60023,200], 'ts_polarity': [-0.108, 0.4]}
    min_max_data = pd.DataFrame(min_max_data) 

    input_data = hourly_data.append(min_max_data, ignore_index=True)
    hourly_data = input_data

    scaler = MinMaxScaler()
    feature_transform = scaler.fit_transform(hourly_data[features])
    feature_transform= pd.DataFrame(columns=features, data=feature_transform, index=hourly_data.index)
    feature_transform

    X_test=feature_transform.iloc[0:1 , :]

    testX =np.array(X_test)
    X_test = testX.reshape(X_test.shape[0], 1, X_test.shape[1])
    return X_test

def callback(message):
    #print(f'Received message: {message}')
    #print(f'data: {message.data}')

    if message.attributes:
        date = message.attributes.get("date")
        open = message.attributes.get("open")
        high = message.attributes.get("high")
        low = message.attributes.get("low")
        close = message.attributes.get("close")
        adj_close = message.attributes.get("adj_close")
        ts_polarity = message.attributes.get("ts_polarity")
        processed_data = min_max_nomalization(date, open, high, low, close, adj_close, ts_polarity)
        result = predict_json(processed_data.tolist())
        print("date: {}".format(date))
        print("predicted price: {}".format(str(result[0][0])))
        bigquery_insert(date, result[0][0])
        print(datetime.datetime.now(pytz.timezone("US/Mountain")).strftime('%Y-%m-%d %H:%M:%S'))
        
    message.ack()           


streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f'Listening for messages on {subscription_path}')


with subscriber:                                                # wrap subscriber in a 'with' block to automatically call close() when done
    try:
        # streaming_pull_future.result(timeout=timeout)
        streaming_pull_future.result()                          # going without a timeout will wait & block indefinitely
    except TimeoutError:
        streaming_pull_future.cancel()                          # trigger the shutdown
        streaming_pull_future.result()                          # block until the shutdown is complete
