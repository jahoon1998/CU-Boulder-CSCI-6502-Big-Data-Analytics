# 2022 CSCI 6502 Big Data Analytics Final Project
## Stock Market Analysis and Prediction 
## Team Members 
Jahoon Koo         CSCI 6502 - 001 B  
Jhansi Saketa B V  CSCI 6502 - 001

## About Project 
Stock Market Analysis and Prediction using Big Data
processing tools, and Deep Learning algorithms. Our project
has three main stages:
1. Data streaming
2. Data processing
3. Analysis/Prediction of big data.

In data streaming, we are going to work on two data sources
which are real time streaming data. The first data source is
social media and the second data source is stock market quotes.
The Data is then going to be pre-processed and the Deep
learning model is going to use numerical and text features
extracted from data sources to predict the stock market rates.

## Methodology
The workflow we have designed for our stock market prediction and analysis application. There are five steps present at the general-level of this workflow. There is some degree of variability within this workflow because the specific cloud tools can be varied based on the need of the application and the cost of cloud tools.

The workflow begins with data scraping. This step encapsulates the definition of technologies and methods used for taking in the source data. This includes data scraping from both Twitter and a Finance website. This incoming data will be applied to the deep learning model during the analysis and inference stage. This step requires Cloud VMs to run Twitter API and Finance API scripts to continuously scrape data from sources. Google Cloud Compute Engine is a considerable service to host VMs.  

The Data Scraping stage passes forward into the Data Streaming. This stage encapsulates the technologies and methods used for streaming the input data from two data sources to a cloud data processing tool. This stage requires the ability to stream data from multiple sources simultaneously. Also, the scalability and performance of the data streaming tool are important.  Google Cloud PubSub is a good candidate for now.  

The data streaming stage then flows forward, delivering incoming data into the data processing stage. This stage encapsulates the technologies and methods used for transforming the input data and the data used for training models before the application and deep learning model respectively are able to operate. This stage may need two separate Cloud Data processing systems depending on the complexity of data coming from two sources. Google Cloud Dataflow is a suitable data processing tool for our project.

The data processing stage then flows forward, passing its completed resources into the Analysis and Inference stage. This stage specifies the “brains” of the application. It encapsulates the deep learning trained model information, as well as any supporting technologies needed for the model to operate. Within this stage is where the technical aspects of the application’s brain are used. This stage will define deep learning algorithms and other complex internal processes used to predict stock market prices. Since two data sources have distinct types of data (Tweets are textual data, but stock quotes are numerical data), training a model with a combination of textual features and numerical features will keep the project simple and solid.

Finally, the Inference and analysis stage flows into the storage stage. This step stores predicted stock prices from the inference and analysis stage in a Google BigQuery table. Then, the deep learning model will be evaluated based on the accuracy of these predicted stock prices compared to real stock prices.


## Architecture 
![image](https://github.com/jahoon1998/CU-Boulder-CSCI-6502-Big-Data-Analytics-Final-Project/blob/main/Final_project%20Jahoon_Koo_Jhansi_Saketa/images/architecture.png)
<br>The architecture of the project with the data
tools. In the first stage, Data Scraping VM will collect the data
tweets and stock quotes from the twitter API and Yahoo
Finance respectively. The VM will run the program for an hour
and collect the twitter tweets for an hour. After an hour it
calculates the polarity for all tweets by performing sentiment
analysis using the textblob python library. The polarity is then
combined with the stock quotes and then in the second stage
using Pub/Sub it sends the data to the MiddleMan VM.
The trained deep learning model (LSTM) is deployed in the AI
Platform of the Google Cloud Platform. The MiddleMan VM,
after receiving the data from the Pub/Sub, predicts the stock
rate of the Apple organization using the deployed model in the
AI Platform. After the prediction, the data is sent to the Big
Query table. 
## Prediction by LSTM
![image](https://github.com/jahoon1998/CU-Boulder-CSCI-6502-Big-Data-Analytics-Final-Project/blob/main/Final_project%20Jahoon_Koo_Jhansi_Saketa/images/prediction_by_lstm.png)
## Final Results 
![image](https://github.com/jahoon1998/CU-Boulder-CSCI-6502-Big-Data-Analytics-Final-Project/blob/main/Final_project%20Jahoon_Koo_Jhansi_Saketa/images/bigquery_results.png)
