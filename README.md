# MSDS-434
Final Project for MSDS-434

## Overview
This is a cloud-native analytics application that is hosted on the Google Cloud Platform (GCP) to provide users with up-to-date statistics of COVID-19 confirmed cases and deaths statistics for the United States as well as a prediction of confirmed cases and deaths in the upcoming week. Using python, a flask application is developed to directly query from Google BigQuery (holds two ARIMA models and ETL of New York Time COVID-19 Dataset). Using this application, users can get the latest statistic of confirmed cases and deaths of COVID-19 in the US. In addition to that, through BigQuery ML, predictions of confirmed COVID-19 cases and deaths in the next 7 days are provided to the users.


## Source Data
Source data is derived from the The New York Times US Coronavirus Database (https://console.cloud.google.com/projectselector2/bigquery?p=bigquery-public-data&d=covid19_nyt&page=dataset&supportedpurview=project)

[![Python application test with Github Actions](https://github.com/szhang12345/MSDS-434/actions/workflows/main.yml/badge.svg)](https://github.com/szhang12345/MSDS-434/actions/workflows/main.yml)
