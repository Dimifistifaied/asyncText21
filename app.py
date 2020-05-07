from flask import Flask, render_template, request, abort, jsonify, Response
from Infrastructure import Runnable as rn
from collections import deque
import uuid,json

app = Flask(__name__, static_folder='', static_url_path='')
app.ls = []
app.bufferText = ''
app.userDict = {}
app.compiled = ''
app.currentID = ''

@app.route('/')
def init():
    return render_template('guz.html')


@app.route('/generateUUID')
def generate_uuid():
    uniqueID = str(uuid.uuid1())
    app.userDict.update({uniqueID: deque()})
    return uniqueID


@app.route('/post', methods=['POST'])
def set_tasks():
    if not request.json or 'text' not in request.json:
        abort(400)
    else:
        app.ls = request.json['text']
        app.message = app.ls
    return str(rn.createFile(app.ls))


@app.route('/get', methods=['GET'])
def get_task():
    print(app.ls[:])
    return app.ls[:]


@app.route('/load', methods=['GET'])
def load_text():
    if app.bufferText is not None:
        return app.bufferText


@app.route('/save', methods=['POST'])
def save_text():
    app.userDict.get(request.json['user']).append(request.json['text'])
    for item in app.userDict.items():
        if item[0] != request.json['user']:
            item[1].append(request.json['text'])

    return 'OK'

@app.route('/stream/<UUID>', methods=['GET'])
def stream(UUID):
    def eventstream(UUID):
        while True:
            # Poll data from the database
            # and see if there's a new message
            # if app.userDict.get(UUID)[1] == 'subscriber' and app.currentID is not UUID:
            #     if app.currentID is not '' and app.userDict.get(UUID)[0] != app.userDict.get(app.currentID)[0]:

            # elif app.userDict.get(UUID)[1] == 'writer':
            #     if app.userDict.get(UUID)[0] is not '':
            #         app.userDict.update({UUID: (app.userDict.get(UUID)[0], 'subscriber')})

            #         app.currentID = UUID
            #     else:
            #         app.currentID = UUID
            if len(app.userDict.get(UUID)) > 0:
                dataJSON = json.dumps({"text": app.userDict.get(UUID).popleft()})
                yield "event: ping\ndata:{}\n\n".format(dataJSON)

    return Response(eventstream(UUID), mimetype="text/event-stream")


if __name__ == "__main__":
    app.run()
