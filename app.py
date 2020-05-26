
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

@app.route('/create_entry', methods=['POST'])
def create_entry():
    token = request.args.get("token")
    content = request.get_json(silent=True)
    print(content)
    ## [{ value, slug, type }]

    client = NotionClient(token)
    url = request.args.get('url')
    cv = client.get_collection_view(url)
    row = cv.collection.add_row()

    ## Types:
    ##      date => NotionDate ✅
    ##      relation => ????
    ##      title => string ✅
    ##      select => string ✅

    for prop in content:
        val = prop['value']
        if(prop['type'] == 'date'):
            datet = datetime.fromtimestamp(prop['value'])
            val = NotionDate(datet)
        row.set_property(prop['slug'], val)

    response = app.response_class(
        status=200,
        mimetype='application/json'
    )
    return response
   
   

if __name__ == '__main__':  
    app.debug = True
    port = int(os.environ.get("PORT", 4000))
    app.run(host='localhost', port=port, threaded=True)
