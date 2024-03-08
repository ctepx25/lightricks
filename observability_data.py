import sys
import os
import requests
import time
from influxdb_client_3 import InfluxDBClient3

#Data endpoint
observability_endpoint = os.environ["OBSERVABILITY_ENDPOINT"]

#Coralogix 
coralogix_api_key = os.environ["CORALOGIX_API_KEY"]
coralogix_endpoint = os.environ["CORALOGIX_ENDPOINT"]
subsystemName = os.environ["CORALOGIX_SUBSYSTEM_NAME"]

#Influxdb 
influxdb_api_token = os.environ["INFLUXDB_API_TOKEN"]
influxdb_endpoint = os.environ["INFULXDB_ENDPOINT"]
influxdb_database = os.environ["INFLUXDB_DATABASE"]


def get_observability_data():
    headers = {'Accept': 'application/json'}
    try:
        r = requests.get(observability_endpoint, headers=headers)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    data = r.json()[0]
    print("Extracted data:\n", data,'\n')
    return data


def collect_log_entries(observability_data):
    severity_level = {"Debug": 1, "Verbose": 2, "Info": 3, "Warn": 4, "Error": 5, "Critical": 6}
    severity = None
    logEntries = []
    if observability_data["exceptions"]:
        for exception in observability_data["exceptions"]:
            json = {}
            json["severity"] = severity_level[exception["name"]]
            json["text"] = exception["message"]
            #json["timestamp"] = exception["timestamp"]
            logEntries.append(json)

    if observability_data["logs"]:
        for log in observability_data["logs"]:
            json = {}
            json["severity"]  = 3
            json["text"] = str(log["message"])
            #json["timestamp"] = log["timestamp"]
            logEntries.append(json)
    return logEntries


def send_logs(logs_data):
    #This is to comply with api limitation of max packet size of 2MB
    logs_data_chunk = []
    x = 0
    while x < len(logs_data):
        while sys.getsizeof(logs_data_chunk) < 2097152 and x < len(logs_data):
            logs_data_chunk.append(logs_data[x])
            x += 1

        payload = {"applicationName": observability_data["scriptName"], "subsystemName": subsystemName}
        payload["logEntries"] = logs_data_chunk
        print("Sending logs to coralogix endpoint:\n", payload)
        headers = {'Authorization': 'Bearer '+ coralogix_api_key, 'Content-Type': 'application/json'}
        try:
            r = requests.post(coralogix_endpoint, json=payload, headers=headers)
            r.raise_for_status()
            print(r.status_code, r.reason, '\n')
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        logs_data_chunk = []


def collect_metrics(observability_data):
    lines = []
    if observability_data["diagnosticsChannelEvents"]:
        for metric in observability_data["diagnosticsChannelEvents"]:
            line = observability_data["scriptName"]+",env="+metric["message"]["env"]+",endpoint="+metric["message"]["endpoint"]+" price="+str(metric["message"]["value"])+" "+str(time.time())[:10]
            lines.append(line)
    return lines


def send_metrics(metrics_data):
    try:
        client = InfluxDBClient3(host=influxdb_endpoint, token=influxdb_api_token, database=influxdb_database)
        client.write(metrics_data,write_precision='s')
        print("Sending metrics to influxdb:\n", metrics_data,'\n')
        client.close()
    except Exception as e:
        print(e)
        raise


observability_data = get_observability_data()
logs_data = collect_log_entries(observability_data)
metrics_data = collect_metrics(observability_data)
send_logs(logs_data)
send_metrics(metrics_data)
