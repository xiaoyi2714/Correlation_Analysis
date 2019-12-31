# -*- coding:utf-8 -*-
import os
import sys
sys.path.append('./')
from flask import Flask, request, jsonify, send_file
import json
from src.control import *
from flask_cors import CORS
from src.granger_causality import granger_test

#创建Flask对象接收一个参数__name__，它会指向程序所在的包

app = Flask(__name__)

CORS(app)

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
PATH = ROOT_PATH + '/association_analysis/data/'


@app.route('/correlation', methods=['GET', 'POST'])
def correlation():
    if request.method == 'POST':
        data = request.data
        j_data = json.loads(data)
        events = j_data["events"]
        kpi_series = j_data["kpi_series"]
        correlation_list = association_control(kpi_series, events)
        result = {
            'correlation_list': correlation_list
        }
        result = jsonify(result)
        return result
    else:
        return 'success'


@app.route('/sst', methods=['GET', 'POST'])
def sst():
    if request.method == 'POST':
        data = request.data
        j_data = json.loads(data)
        kpi_series = j_data["kpi_series"]
        sst_series = sst_control(kpi_series)
        result = {
            'sst': sst_series
        }
        result = jsonify(result)
        return result
    else:
        return 'success'


@app.route('/detect', methods=['GET', 'POST'])
def detect():
    if request.method == 'POST':
        data = request.data
        j_data = json.loads(data)
        kpi_series = j_data["kpi_series"]
        alarm_line = j_data["alarm_line"]
        range = detect_control(kpi_series, alarm_line)
        result = {
            'alarm_range': range
        }
        result = jsonify(result)
        return result
    else:
        return 'success'


@app.route('/distance', methods=['GET', 'POST'])
def distance():
    if request.method == 'POST':
        data = request.data
        j_data = json.loads(data)
        kpi_series_normal = j_data["kpi_series_normal"]
        kpi_series_abnormal = j_data["kpi_series_abnormal"]
        distance_result = distance_control(kpi_series_normal, kpi_series_abnormal)
        result = {
            'distance': distance_result
        }
        print(result)
        result = jsonify(result)
        print(result)
        return result
    else:
        return 'success'


@app.route('/cluster', methods=['GET', 'POST'])
def cluster():
    if request.method == 'POST':
        data = request.data
        j_data = json.loads(data)
        kpi_series = j_data["kpi_series"]
        name = j_data["name"]
        if cluster_control(kpi_series, name):
            return 'success'
        else:
            return 'failure'
    else:
        return 'success'


@app.route('/get_image')
def get_image():
    return send_file('../static/hierarchy.png')


@app.route('/granger', methods=['GET', 'POST'])
def granger():
    if request.method == 'POST':
        data = request.data
        j_data = json.loads(data)
        kpi_series_first = j_data["kpi_series_first"]
        kpi_series_second = j_data["kpi_series_second"]
        granger_result = granger_test(kpi_series_first, kpi_series_second)
        result = {
            'granger': granger_result
        }
        result = jsonify(result)
        return result
    else:
        return 'success'


# httpserver.serve(app, host='0.0.0.0', port=8080)


# Flask应用程序实例的run方法,启动WEB服务器
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
