from flask import Flask, render_template, request, abort, jsonify
#from Infrastructure import Runnable as rn

app = Flask(__name__, static_folder='', static_url_path='')
app.ls = []


@app.route('/')
def init():
    return render_template('guz.html')


"""@app.route('/post', methods=['POST'])
def set_tasks():
    if not request.json or 'text' not in request.json:
        abort(400)
    else:
        app.ls = request.json['text']
    return str(rn.createFile(app.ls))
"""

@app.route('/get', methods=['GET'])
def get_task():
    print(app.ls[:])
    return app.ls[:]


if __name__ == "__main__":
    app.run()
