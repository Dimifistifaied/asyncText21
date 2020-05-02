from flask import Flask, render_template, request, abort, jsonify, Response
from Infrastructure import Runnable as rn
import uuid

app = Flask(__name__, static_folder='', static_url_path='')
app.ls = []
app.message = None
app.previous_message = None
app.bufferText = []
app.userDict = {}


@app.route('/')
def init():
    return render_template('guz.html')


@app.route('/generateUUID')
def generate_uuid():
    uniqueID = str(uuid.uuid1())
    app.userDict.update({uniqueID: ''})
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
    app.bufferText = request.json['text']
    app.userDict.update({request.json['user']: app.bufferText})
    return 'OK'


@app.route('/stream/<UUID>', methods=['GET'])
def stream(UUID):

    def eventstream(UUID):
        while True:
            # Poll data from the database
            # and see if there's a new message
            if UUID in app.userDict and app.userDict.get(UUID) != app.bufferText:
                print(app.userDict.get(UUID), app.bufferText)
                app.userDict.update({UUID: app.bufferText})
                yield "event:'ping'\ndata:{}\n\n".format(app.bufferText)

    return Response(eventstream(UUID), mimetype="text/event-stream")


if __name__ == "__main__":
    app.run()
