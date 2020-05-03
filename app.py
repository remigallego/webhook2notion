
import os
from notion.client import NotionClient
from flask import Flask
from flask import request

app = Flask(__name__)

def createNotionTask(token, collectionURL, content):
    # notion
    client = NotionClient(token)
    cv = client.get_collection_view(collectionURL)
    row = cv.collection.add_row()
    row.title = content.title
    row['Due Date'] = content.date


@app.route('/create_todo', methods=['GET'])
def create_todo():

    todo.title = request.args.get('todo')
    todo.date = request.args.get('date')
    token_v2 = request.args.get('token')
    url = os.environ.get("URL")
    createNotionTask(token_v2, url, todo)
    return f'added {todo} to Notion!!! Yeah'


if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
