
# -*- coding: utf-8 -*-
import os
import json
from datetime import datetime, date
from notion.collection import NotionDate
from notion.client import NotionClient
from math import pi
from flask import Flask
from flask import request

app = Flask(__name__)

"""https://www.notion.so/remigallego/be7420b21a814bdeb93dcd2f1f99615e?v=772f2dabaac541c38761e3b288f163d3"""

""" class Todo:
  title = ''
  date = ''

def construct_todo(title, date):
    todo = Todo()
    todo.title = title
    todo.date = datetime.strptime(date, "%d-%m-%Y")
    return todo

def createNotionTask(token, collectionURL, content):
    # notion
    client = NotionClient(token)
    cv = client.get_collection_view(collectionURL)
    row = cv.collection.add_row()
    row.title = content.title
    row.Date = NotionDate(content.date)
    row.Status = "Not Started"
     """

@app.route('/get_collection', methods=['GET'])
def get_collection():
    token = request.args.get("token")
    client = NotionClient(token)
    url = request.args.get('url')
    cv = client.get_collection_view(url)
    props = cv.collection.get_schema_properties()
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
    app.run(host='localhost', port=port, threaded=True)
