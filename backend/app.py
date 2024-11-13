# Import libraries
from flask import Flask
from flask_cors import CORS
import json
from json import loads, dumps
import pandas as pd

app = Flask(__name__)
cors = CORS(app)

def init_routes(app):
    @app.route("/")
    def start():
        file_path = 'meat_consumption_worldwide.csv'
        df = pd.read_csv(file_path)
        result = df.to_json(orient="records")
        parsed = loads(result)
        return parsed
    
    @app.route("/change_in_meat_consumption")
    def change_in_comsumption():
        df = pd.read_csv('meat_consumption_worldwide.csv')
        results_consumption = [] 
        for (location, subject), group in df.groupby(['LOCATION', 'SUBJECT']):
            first_year = group['TIME'].min()
            last_year = group['TIME'].max()
            first_value = group[group['TIME'] == first_year]['Value'].values[0]
            last_value = group[group['TIME'] == last_year]['Value'].values[0]
            #first_value = first_value.item() if isinstance(first_value, pd.Series) else first_value
            #last_value = last_value.item() if isinstance(last_value, pd.Series) else last_value
            value_increase = last_value - first_value
            results_consumption.append({
                'LOCATION': location,
                'SUBJECT': subject,
                'First Year': first_year,
                'Last Year': last_year,
                'First Value': first_value,
                'Last Value': last_value,
                'Increase in Consumption': value_increase
            })
        results_consumption_df = pd.DataFrame(results_consumption)
        results_consumption_df_json = loads(results_consumption_df.to_json(orient="records"))
        #return loads(results_consumption_df.to_json(orient="records"))
        return results_consumption_df_json
    
init_routes(app)