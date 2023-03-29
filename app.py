from __future__ import print_function  # In python 2.7

import json
import sys
import threading
import time
from multiprocessing import Value, Process

from flask import Flask, jsonify, send_from_directory, abort, send_file
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
output = {}
DOWNLOAD_DIRECTORY = "/visualization_BE"


@app.route("/")
# @cross_origin()
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/get-file/')
def get_file():
    """Download a file."""
    try:
        return send_file('office_space_dynamic.pcd')
    except FileNotFoundError:
        abort(404)
    return "success"


def data_thread():
    # x = []
    # y = []
    # z = []
    # with open('office.txt') as obj:
    #     for line in obj:
    #         row = line.split(",")
    #         x.append(row[0].strip())
    #         y.append(row[1].strip())
    #         z.append(row[2].strip())
    #         output['x'] = x
    #         output['y'] = y
    #         output['z'] = z
    #         print(output, file=sys.stderr)
    #         # time.sleep(2)
    fr = open("office_space.pcd", "r")
    fw = open("office_space_dynamic.pcd", "w")
    points = fr.readlines()
    for i in range(len(points)):
        time.sleep(.007)
        fw.write(points[i])
        print(points[i], file=sys.stderr)


@app.route("/get_data/")
@cross_origin()
def get_data():
    return jsonify(output)


@app.route("/start_thread/")
@cross_origin()
def start_thread():
    if output == {}:
        threading.Thread(target=data_thread).start()
    return jsonify("started thread")

# if __name__ == '__main__':
#     recording_on = Value('b', True)
#     p = Process(target=data_thread, args=(recording_on,))
#     p.start()
#     app.run(debug=True, use_reloader=False)
#     # p.join()
