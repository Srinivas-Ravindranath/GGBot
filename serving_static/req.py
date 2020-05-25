from flask import Flask, request, jsonify, make_response
from flask import render_template, Response
from flask_socketio import SocketIO, send, emit
import processor
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345abcd'
socketio = SocketIO(app)


@app.route("/", methods=['GET', 'POST'])
def next_web():   
    return render_template("index.html")


@socketio.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})


@socketio.on('message')
def handle_message(message):
    f = open('answers.txt','w')
    f.write(message)
    f.close()
    handle_my_custom_event()

@socketio.on('test')
def handle_my_custom_event():
    time.sleep(2)
    f = open('answers.txt','r')
    reads = f.read()
    
    f.close()
    response = processor.chat(reads)
    print(response)
    emit('my responses', {'data': response})

if __name__ == "__main__":
    socketio.run(app)
