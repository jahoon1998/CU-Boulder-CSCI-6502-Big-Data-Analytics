################################################################
# CSCI 6502 - Jahoon Koo, Jhansi Saketa
# main.py
# This file uses Twitter API and Yahoo Finance API to receive data 
# for a certain amount of time and calculates average polarity of 
# tweets and publishes average polarity and stock quotes to Google Cloud PubSub 
# 
################################################################

import requests
import os
import json
import ast
import csv
import re
import pytz
from textblob import TextBlob
import time
import threading
from multiprocessing import Process
import stocks
from google.cloud import pubsub_v1
import datetime
import time

pol=[]
startTime = time.time()


# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAFZbZwEAAAAASSbWf5XMPp%2B4SgkY8N5gc1Ya63w%3DZHotq26FBd3h6n5JIMPeGNp28iCZekXtzW3PT3dY5IwsyJdS4Z'


# PUBSUB project
YOUR_PROJECT = "noble-airport-343004"
YOUR_PUBSUB_TOPIC = "stock_market_prediction"


# Configure the connection
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(YOUR_PROJECT, YOUR_PUBSUB_TOPIC)


def write_to_pubsub(incoming_data):
    try:
        data = "real-time stock quotes and twitter polarity"  
        data = data.encode('utf-8')
        attributes = {
            'date': datetime.datetime.now(pytz.timezone("US/Mountain")).strftime('%Y-%m-%d %H:%M'),
            'open': str(incoming_data[1][0]),
            'high': str(incoming_data[1][1]),
            'low': str(incoming_data[1][2]),
            'close': str(incoming_data[1][3]),
            'adj_close': str(incoming_data[1][4]),
            'ts_polarity': str(incoming_data[1][5])
        }
        # publish to the topic, don't forget to encode everything at utf8!
        print(datetime.datetime.now(pytz.timezone("US/Mountain")).strftime('%Y-%m-%d %H:%M:%S'))
        future = publisher.publish(topic_path, data, **attributes)
        print("published message: {}".format(future.result()))
            
    except Exception as e:
        print(e)
        raise

def remove_url(txt):
    """Replace URLs found in a text string with nothing
    (i.e. it will remove the URL from the string).

    Parameters
    ----------
    txt : string
        A text string that you want to parse and remove urls.

    Returns
    -------
    The same txt string with url's removed.
    """

    return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt).split())
def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FilteredStreamPython"
    return r

def get_rules():
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", auth=bearer_oauth
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    return response.json()


def delete_all_rules(rules):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )

def set_rules(delete):
    # You can adjust the rules if needed
    sample_rules = [
        {"value": "AAPL" }
    ]
    payload = {"add": sample_rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )


def get_stream(set):
    # global writer
    response = requests.get("https://api.twitter.com/2/tweets/search/stream", auth=bearer_oauth, stream=True,
    )
    # print(response.status_code)
    if response.status_code != 200:
            raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    
    try:
        for response_line in response.iter_lines():
            if response_line:
                json_response = json.loads(response_line)
                k = json.dumps(json_response, indent=4, sort_keys=True)
                p = ast.literal_eval(k)
                l = [remove_url(p['data']['text'])]
                sentiment_objects = TextBlob(l[0])
                pol.append(sentiment_objects.polarity)
                executionTime = (time.time() - startTime)
                print('Execution time in seconds: ' + str(executionTime))
            if executionTime >= 60 * 60:
                exec(open("stocks.py").read())
                stocks.l[0].append("ts_polarity")
                stocks.l[1].append(sum(pol) / len(pol))
                print("stocks l printing")
                print("________________________")
                print(stocks.l)
                write_to_pubsub(stocks.l)
                exit();
    except Exception as ex:
       pass

def main():
    global listt
    listt = []
    global l
    l = []
    rules = get_rules()
    delete = delete_all_rules(rules)
    set = set_rules(delete)
    get_stream(set)
if __name__ == "__main__":
    main()
