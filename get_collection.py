# -*- coding: utf-8 -*-
import os
import json
from datetime import datetime, date
from notion.collection import NotionDate
from notion.client import NotionClient
from flask import Flask
from flask import request
from flask_cors import CORS
from __main__ import app

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
    for prop in cProperties:
        if(prop['type'] == 'relation'):
            print("here")
            options = []
            relation = {
                "slug": prop["slug"],
                "options": []
            }
            ## list all options
            collection = client.get_collection(prop['collection_id'])
            project_rows = collection.get_rows()
            print(project_rows)
            for project_row in project_rows:
                title = project_row.get_property("title")
                id = project_row.id
                options.append({
                    "title": title,
                    "id": id
                })
            prop["options"] = options
                
    obj['properties'] = cProperties

    cRows = cv.collection.get_rows()

    data = []
    for row in cRows:
        thisRow = {}
        for prop in cProperties:
            thisRow[prop['slug']] = get_property_value_in_row(row,prop)
        data.append(thisRow)

    obj['data'] = data

    response = app.response_class(
        response=json.dumps(obj),
        status=200,
        mimetype='application/json'
    )
    return response