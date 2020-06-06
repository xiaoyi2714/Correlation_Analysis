# -*- coding:utf-8 -*-
import os
from flask import Flask, request, jsonify, send_file
import json
import csv
from flask_cors import CORS
from main import cg_cause

app = Flask(__name__)

CORS(app)

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
PATH = ROOT_PATH + '/datasets/'


@app.route('/root_cause', methods=['GET', 'POST'])
def root_cause():
    if request.method == 'POST':
        data = request.data
        j_data = json.loads(data)
        exception = j_data["exception"]
        print(exception)
        kpi_series = j_data["kpi_series"]
        print(kpi_series)
        with open("../datasets/all_data.csv", 'w') as file:
            writer = csv.writer(file)
            for row in kpi_series:
                writer.writerow(row)
        test = cg_cause()
        test.load_data()
        test.cluster()
        test.cluster_sst()
        test.granger()
        test.find_relation(exception)
        result = test.cause(exception)
        return result
    else:
        return 'Successful'


# httpserver.serve(app, host='0.0.0.0', port=8080)


# Flask应用程序实例的run方法,启动WEB服务器
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=12345)
