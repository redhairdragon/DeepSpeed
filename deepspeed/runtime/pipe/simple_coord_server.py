import sys
import os
from flask import json
from flask import Flask
app = Flask("coord server")

remapping = False
# return if there is layer remapping happening


@app.route('/status', methods=['GET'])
def status():
    return str(remapping)


@app.route('/yes', methods=['POST', 'GET'])
def setYes():
    global remapping
    remapping = True
    return 'OK'


@app.route('/no', methods=['POST', 'GET'])
def setNo():
    global remapping
    remapping = False
    return 'OK'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
