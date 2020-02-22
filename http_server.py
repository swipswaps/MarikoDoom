from flask import Flask, request, render_template
import socket
import sys
import logging

app = Flask(__name__)
app.debug = False

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

#fps = 1 # 1 = 15fps, 2 = 20fps

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

    if fps == 1:
        return render_template("index_15fps.html")
    elif fps == 2:
        return render_template("index_20fps.html")
    else:
        return render_template("index_20fps.html")

if __name__=="__main__":
    port = sys.argv[1]
    fps = int(sys.argv[2])
    app.run(host="0.0.0.0", port=port)
