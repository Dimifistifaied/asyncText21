from flask import Flask, render_template, request, abort, jsonify, Response
from Infrastructure import Runnable as rn
app = Flask(__name__, static_folder='', static_url_path='')
app.ls = []
app.message = None
app.previous_message = None

@app.route('/')
def init():
    return render_template('guz.html')


@app.route('/post', methods=['POST'])
def set_tasks():
    if not request.json or 'text' not in request.json:
        abort(400)
    else:
        app.ls = request.json['text']
        app.message = app.ls
    return "str(rn.createFile(app.ls))"


@app.route('/get', methods=['GET'])
def get_task():
    print(app.ls[:])
    return app.ls[:]


@app.route('/stream', methods=['GET'])
def stream():

    def eventstream():
        while True:
            # Poll data from the database
            # and see if there's a new message
                yield "event:'ping'\ndata:{}\n\n".format(app.ls)

    return Response(eventstream(), mimetype="text/event-stream")


if __name__ == "__main__":
    app.run()
