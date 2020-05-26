
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

import get_collection

cors = CORS(app, resources={r"/*": {"origins": "*"}})

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

if __name__ == '__main__':  
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, threaded=True)

