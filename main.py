from flask import Flask, render_template, request, redirect, url_for
import socket
import json
from datetime import datetime
from threading import Thread

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/message.html')
def message():
    return render_template('message.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html'), 404

@app.route('/message', methods=['POST'])
def handle_message():
    username = request.form['username']
    message = request.form['message']
    
    UDP_IP = "127.0.0.1"
    UDP_PORT = 5000
    MESSAGE = json.dumps({
        "username": username,
        "message": message,
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    }).encode()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

    return redirect(url_for('index'))

def socket_server():
    UDP_IP = "127.0.0.1"
    UDP_PORT = 5000

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    while True:
        data, addr = sock.recvfrom(1024)
        message_data = json.loads(data.decode())
        
        with open('storage/data.json', 'r') as file:
            messages = json.load(file)
        
        messages[message_data['timestamp']] = {
            'username': message_data['username'],
            'message': message_data['message']
        }
        
        with open('storage/data.json', 'w') as file:
            json.dump(messages, file)

if __name__ == '__main__':
    socket_thread = Thread(target=socket_server)
    socket_thread.start()

    app.run(port=3000)
