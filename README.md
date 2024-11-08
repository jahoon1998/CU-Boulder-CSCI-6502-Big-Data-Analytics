# 2022 CSCI 6502 Big Data Analytics Final Project
## Stock Market Analysis and Prediction 
## Team Members 
Jahoon Koo         CSCI 6502 - 001 B  
Jhansi Saketa B V  CSCI 6502 - 001

### About the Project
Stock Market Analysis and Prediction using Big Data processing tools and Deep Learning algorithms. Our project has three main stages:
1. **Data Streaming**
2. **Data Processing**
3. **Analysis/Prediction of Big Data**

In **Data Streaming**, we use two real-time data sources: social media and stock market quotes. The data is pre-processed, and the Deep Learning model leverages both numerical and text features from these sources to predict stock market rates.


## Methodology
Our workflow for stock market prediction and analysis comprises five general steps, with some flexibility in the specific cloud tools based on application needs and cost considerations.

1. **Data Scraping**  
   This initial step involves defining the technologies and methods to ingest source data, including scraping data from Twitter and a finance website. The scraped data is fed into a deep learning model during the analysis and inference stage. This requires Cloud VMs to run Twitter and Finance API scripts for continuous data collection. *Google Cloud Compute Engine* is an ideal choice for hosting these VMs.

2. **Data Streaming**  
   In this stage, we stream data from the two sources into a cloud data processing tool, focusing on performance and scalability to handle simultaneous data streams. *Google Cloud PubSub* is our selected tool for this purpose.

3. **Data Processing**  
   This stage involves transforming input data for use by the application and deep learning model. Depending on data complexity, separate Cloud Data processing systems may be necessary for each source. *Google Cloud Dataflow* is a suitable processing tool for this project.

4. **Analysis and Inference**  
   This stage houses the application's core processing and deep learning model. Here, we define deep learning algorithms and other complex processes for stock market price prediction. The model incorporates both textual (Tweets) and numerical (stock quotes) data, simplifying yet strengthening the model.

5. **Storage**  
   Finally, the storage stage saves predicted stock prices in a *Google BigQuery* table. The model’s accuracy will be evaluated by comparing predicted prices to actual stock prices.


## Architecture 
![image](https://github.com/jahoon1998/CU-Boulder-CSCI-6502-Big-Data-Analytics-Final-Project/blob/main/Final_project%20Jahoon_Koo_Jhansi_Saketa/images/architecture.png)
<br>The architecture of the project involves several data tools. In the first stage, a Data Scraping VM collects tweets and stock quotes from the Twitter API and Yahoo Finance, respectively. The VM runs a program for one hour to collect Twitter data, after which it calculates the polarity of all tweets by performing sentiment analysis using the TextBlob Python library. The polarity is then combined with stock quotes, and in the second stage, Pub/Sub sends the data to the MiddleMan VM. The trained deep learning model (LSTM) is deployed on the AI Platform of Google Cloud Platform. After receiving the data from Pub/Sub, the MiddleMan VM predicts the stock rate of Apple using the deployed model on the AI Platform. Following the prediction, the data is sent to a BigQuery table.
## Prediction by LSTM
![image](https://github.com/jahoon1998/CU-Boulder-CSCI-6502-Big-Data-Analytics-Final-Project/blob/main/Final_project%20Jahoon_Koo_Jhansi_Saketa/images/prediction_by_lstm.png)
## Final Results 
![image](https://github.com/jahoon1998/CU-Boulder-CSCI-6502-Big-Data-Analytics-Final-Project/blob/main/Final_project%20Jahoon_Koo_Jhansi_Saketa/images/bigquery_results.png)
