import flask
from datetime import datetime, timedelta

app = flask.Flask(__name__)
#app.config["DEBUG"] = True

servers = {}

@app.route('/', methods=['GET'])
def serverList():
    return flask.jsonify(servers)

@app.route('/add', methods=['POST'])
def addServer():
    data = flask.request.form

    name = data["name"]
    ip = flask.request.remote_addr
    port = data["port"]

    servers[ip + ":" + port] = {
        "name" : name,
        "ip": ip,
        "port": port,
        "lastHearbeat": datetime.now()
    }

    return ""

@app.route('/remove', methods=['POST'])
def removeServer():
    data = flask.request.form

    ip = flask.request.remote_addr
    port = data["port"]

    if (ip + ":" + port) in servers:
        del servers[ip + ":" + port]

    return ""

@app.route('/heartbeat', methods=['POST'])
def heartbeat():
    port = data["port"]

    servers[ip + ":" + port]["lastHearbeat"] = datetime.now()

import threading
import time

def heartbeatCheck():
    while True:
        time.sleep(1)

        for server_ipport in list(servers.keys()):
            if servers[server_ipport]["lastHearbeat"] < (datetime.now() - timedelta(minutes=5)):
                del servers[server_ipport]

t1 = threading.Thread(target=heartbeatCheck)
t1.start()

app.run()