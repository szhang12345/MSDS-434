from flask import Flask, render_template
#from flask import jsonify
import google.auth
from google.cloud import bigquery

app = Flask(__name__)
@app.route('/')
def predict():
 


    credentials, project_id = google.auth.default(
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    project_id = 'qwiklabs-gcp-01-bcc4bb884279'
    bqclient = bigquery.Client(credentials= credentials,project=project_id)

    #get predicted cases
    query_string= """
    SELECT
    DATE(forecast_timestamp) as PredDate, round(m.forecast_value) as Cases
    FROM
    ML.FORECAST(MODEL Covid19NYT.cases_arima_model,
                STRUCT(30 AS horizon, 0.8 AS confidence_level)) m
    where m.forecast_timestamp = (select max(forecast_timestamp)
    FROM
    ML.FORECAST(MODEL Covid19NYT.cases_arima_model,
                STRUCT(30 AS horizon, 0.8 AS confidence_level))
    )
    """
    query_job = bqclient.query(query_string)
    results = query_job.result()
    for row in results:
        CasesPredictionDate = row.PredDate
        PredCases = row.Cases

        
    #get predicted deaths
    query_string= """
    SELECT
    DATE(forecast_timestamp) as PredDate, round(m.forecast_value) as Deaths
    FROM
    ML.FORECAST(MODEL Covid19NYT.deaths_arima_model,
                STRUCT(30 AS horizon, 0.8 AS confidence_level)) m
    where m.forecast_timestamp = (select max(forecast_timestamp)
    FROM
    ML.FORECAST(MODEL Covid19NYT.deaths_arima_model,
                STRUCT(30 AS horizon, 0.8 AS confidence_level))
    )
    """
    query_job = bqclient.query(query_string)
    results = query_job.result()
    for row in results:
        DeathsPredictionDate = row.PredDate
        PredDeaths = row.Deaths

    #get most recent deaths
    query_string= """
    SELECT
    cast(deaths_date_history as TIMESTAMP) AS deaths_date_history,
    total_deaths_history as deaths_history_value,
    FROM
    (
    SELECT
    date as deaths_date_history,
    SUM(daily_deaths) AS total_deaths_history
    FROM
    `qwiklabs-gcp-01-bcc4bb884279.Covid19NYT.DailyCasesDeaths`
    GROUP BY date
    ORDER BY date ASC
    ) dcd
    where dcd.deaths_date_history = (select max(date)
    FROM `qwiklabs-gcp-01-bcc4bb884279.Covid19NYT.DailyCasesDeaths`)
    """
    query_job = bqclient.query(query_string)
    results = query_job.result()
    for row in results:
        DeathsDate = row.deaths_date_history
        QtyDeaths = row.deaths_history_value

    #get most recent cases
    query_string= """
    SELECT
    cast(cases_date_history as TIMESTAMP) AS cases_date_history,
    total_cases_history as cases_history_value,
    FROM
    (
    SELECT
    date as cases_date_history,
    SUM(daily_confirmed_cases) AS total_cases_history
    FROM
    `qwiklabs-gcp-01-bcc4bb884279.Covid19NYT.DailyCasesDeaths`
    GROUP BY date
    ORDER BY date ASC
    ) dcd
    where dcd.cases_date_history = (select max(date)
    FROM `qwiklabs-gcp-01-bcc4bb884279.Covid19NYT.DailyCasesDeaths`)
    """
    query_job = bqclient.query(query_string)
    results = query_job.result()
    for row in results:
        CasesDate = row.cases_date_history
        QtyCases = row.cases_history_value

    
    # this would not present the data, want to debug later
    #val2 = jsonify(CasesPredictionDate=CasesPredictionDate.strftime('%m/%d/%Y'),
    #              PredictedCases=PredCases,
    #              DeathsPredictionDate=DeathsPredictionDate.strftime('%m/%d/%Y'),
    #              PredictedDeaths=PredDeaths,
    #              DeathsDate=DeathsDate.strftime('%m/%d/%Y'),
    #              MostRecentDeathCount=QtyDeaths,
    #              CasesDate=CasesDate.strftime('%m/%d/%Y'),
    #              MostRecentCasesCount=QtyCases)

    val = {"CasesPredictionDate":CasesPredictionDate.strftime('%m/%d/%Y'), "PredictedCases":PredCases,
            "DeathsPredictionDate":DeathsPredictionDate.strftime('%m/%d/%Y'),"PredictedDeaths":PredDeaths,
           "DeathsDate":DeathsDate.strftime('%m/%d/%Y'),"MostRecentDeathCount":QtyDeaths,
           "CasesDate":CasesDate.strftime('%m/%d/%Y'),"MostRecentCasesCount":QtyCases}


    return render_template("page.html", title="COVID19: Current Stats and Predictions",jsonfile = val )

  
if __name__ == '__main__':

    #predict()
 
    #app.run(host='127.0.0.1', port=8080, debug = True)
    app.run(host='0.0.0.0')
