
# -*- coding: utf-8 -*-
import os
from datetime import datetime, date
from notion.collection import NotionDate
from notion.client import NotionClient
from math import pi
from flask import Flask
from flask import request

app = Flask(__name__)

class Todo:
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
    
@app.route('/create_todo', methods=['GET'])
def create_todo():
    todo = construct_todo(request.args.get('todo'), request.args.get('date'))
    token_v2 = request.args.get('token')
    url = os.environ.get("URL")
    createNotionTask(token_v2, url, todo)
    return f'✅ Added {todo.title} to Notion!'



if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
