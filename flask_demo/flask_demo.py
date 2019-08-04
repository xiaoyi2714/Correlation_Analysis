# -*- coding:utf-8 -*-
import os

from flask import Flask, render_template, request
import csv
import pandas as pd
import alarm_association
from flask_restful import Api, Resource

#创建Flask对象接收一个参数__name__，它会指向程序所在的包
app = Flask(__name__)
api = Api(app)

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
print(ROOT_PATH)
PATH = ROOT_PATH + '/association_analysis/data/'
print(PATH)
@app.route('/api', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file1 = request.files['file1']
        file2 = request.files['file2']

        file1.save(os.path.join(PATH, file1.filename))
        event = csv.reader(open(os.path.join(PATH,file1.filename), 'r'))
        file2.save(os.path.join(PATH, file2.filename))
        alldata = csv.reader(open(os.path.join(PATH, file2.filename), 'r'))

        print('event', event)
        print('alldata', alldata)
    flag = alarm_association.association_analysis(event, alldata)
    return str(flag), 404


#Flask应用程序实例的run方法,启动WEB服务器
if __name__ == '__main__':
    app.run(debug=True)