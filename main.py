#!/usr/bin/env python
# -- coding: utf-8 --

"""
description
"""
#import json
import webbrowser
import requests
import io
import flask

from zipfile import ZipFile
from flask import Flask
from flask import request
from flask import render_template
#from flask_cors import CORS, cross_origin

import pytreedb.pytreedb as pytreedb

app = Flask(__name__)
#CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
#@cross_origin(origin='*',headers=['Content- Type'])
def index():
    return render_template(r'newIndex.html', server=request.remote_addr)

@app.route('/about')
def about():
    return render_template(r'about.html')

mydb = pytreedb.PyTreeDB(dbfile=r'E:\tmp\SYSSIFOSS\syssifoss.db') # instantiate pytreedb
mydb.load_db(r'E:\tmp\SYSSIFOSS\syssifoss.db') # Jiani: loading local db file
# mydb.import_data(r'https://heibox.uni-heidelberg.de/f/05969694cbed4c41bcb8/?dl=1', overwrite=True) # download data

# automatically open in a new browser tab on start
if __name__ == 'main':
    webbrowser.open_new_tab('http://127.0.0.1:5000/')

@app.route('/stats')
def getStats():
    return mydb.get_stats()

@app.route('/listspecies')
def getListSpecies():
    return {'species': mydb.get_list_species()}

@app.route('/sharedproperties')
def getSharedProperties():
    return {'properties': mydb.get_shared_properties()}

@app.route('/trees')
def query():
    field = request.args.get('field')
    value = request.args.get('value')
    if field == '' or value == '':
        return dict()
    return {'query': mydb.query(field, value)}

@app.route('/getitem')
def getItem():
    index = request.args.get('index')
    if index == '':
        return dict()
    print(mydb[int(index)]['_json'])
    return {'item': mydb[int(index)]['_json']}
    # print({'item': json.loads(mydb[int(index)]['_json'])})
    # return {'item': json.loads(mydb[int(index)]['_json'])}

@app.route('/downloadpointclouds')
def downloadPointClouds():
    # urls = ['https://downloads.raspberrypi.org/raspios_lite_armhf/images/raspios_lite_armhf-2021-05-28/2021-05-07-raspios-buster-armhf-lite.zip']
    urls = ['https://heibox.uni-heidelberg.de/f/3e52b2c164b247fe85ec/?dl=1',
            'https://heibox.uni-heidelberg.de/f/ad707892be7e41dcabe3/?dl=1',
            'https://heibox.uni-heidelberg.de/f/7d45579bd93d4b6080c2/?dl=1']
    o = io.BytesIO()
    
    with ZipFile(o, 'w') as zf:
        for i in range(len(urls)):
            res = requests.get(urls[i]).content
            zf.writestr('file_{:02d}.laz'.format(i), res)
    zf.close()
    o.seek(0)
    
    return flask.send_file(
        o,
        mimetype='application/zip',
        as_attachment=True,
        attachment_filename='pointcloud.zip'
    )
    
    