import uuid,json
from flask import *
from collections import deque
from Infrastructure import Runnable as rn

app = Flask(__name__, static_folder='', static_url_path='')
app.userDict = {}

@app.route('/')
def init():
    return render_template('guz.html')


@app.route('/generateUUID')
def generate_uuid():
    uniqueID = str(uuid.uuid1())
    app.userDict.update({uniqueID: deque()})
    return uniqueID


@app.route('/exec', methods=['POST'])
def exec_pycode():
    if not request.json or 'text' not in request.json:
        abort(400)
    else:
        return str(rn.createFile(request.json['text']))


@app.route('/save', methods=['POST'])
def save():
    for item in app.userDict.items():
        if item[0] != request.json['user']:
            item[1].append(request.json['text'])
    return 'OK'

@app.route('/stream/<UUID>', methods=['GET'])
def stream(UUID):
    def eventstream(UUID):
        while True:
            if len(app.userDict.get(UUID)) > 0:
                dataJSON = json.dumps({"text": app.userDict.get(UUID).popleft()})
                yield "event: ping\ndata:{}\n\n".format(dataJSON)
    return Response(eventstream(UUID), mimetype="text/event-stream")



if __name__ == "__main__":
    app.run()
