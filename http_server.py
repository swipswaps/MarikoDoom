from flask import Flask, request, render_template
import socket
import sys

app = Flask(__name__)
app.debug = False

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

def send(key):
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 1312)
    message = str.encode(key)

    # Send data
    sent = sock.sendto(message, server_address)
    sock.close()

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        key = request.form["key"]
        send(key)
    return render_template("index.html")

if __name__=="__main__":
    port = sys.argv[1]
    app.run(host="0.0.0.0", port=port)
