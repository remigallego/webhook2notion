
# -*- coding: utf-8 -*-
import os
import json
from datetime import datetime, date
from notion.collection import NotionDate
from notion.client import NotionClient
from flask import Flask
from flask import request
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

def get_property_value_in_row(row, prop):
    if(prop['type'] == 'relation'):
            value = ''
            block = row.get_property(prop['slug'])
            for index, item in enumerate(block):
                if(item is None):
                    print('none')
                else:
                    if(hasattr(item, 'get_property')):
                        if(index == 0):
                            print(item)
                            value = item.get_property('title')
                        else:
                            value = value + ', ' + item.get_property('title')
                    
    else:
        value = row.get_property(prop['slug'])
        if(type(value) == NotionDate):
            dateFormatted = {
                "start": value.start.isoformat(),
            }
            value = dateFormatted
    return value

@app.route('/get_collection', methods=['GET'])
def get_collection():
   

    token = request.args.get("token")
    client = NotionClient(token)
    url = request.args.get('url')

    obj = {
        "properties": [],
        "data": []
    }

    cv = client.get_collection_view(url)
    cProperties = cv.collection.get_schema_properties()
    obj['properties'] = cProperties
    cRows = cv.collection.get_rows()

    data = []
    for row in cRows:
        thisRow = {}
        for prop in cProperties:
            thisRow[prop['slug']] = get_property_value_in_row(row,prop)
        data.append(thisRow)

    obj['data'] = data

    print(obj)
    response = app.response_class(
        response=json.dumps(obj),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/get_collection_rows', methods=['GET'])
def get_collection_rows():
    token = request.args.get("token")
    client = NotionClient(token)
    url = request.args.get('url')
    cv = client.get_collection_view(url)
    rows = []
    props = cv.collection.get_rows()
    for row in props:
        rows.append(row)

    response = app.response_class(
        response=json.dumps(rows),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/create_todo', methods=['POST'])
def create_todo():
    token = request.args.get("token")
    client = NotionClient(token)
    url = request.args.get('url')
    cv = client.get_collection_view(url)
    props = cv.collection.get_rows()
    return json.dumps(props)

""" @app.route('/create_todo', methods=['POST'])
def create_todo():

    values = request.values
    for key in values.keys():
        print(values.get(key))
    return f"{values}"
 """
if __name__ == '__main__':  
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, threaded=True)

