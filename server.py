import eventlet
eventlet.monkey_patch()

import os
from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'
CORS(app,resources={r"/*":{"origins":"*"}})
socketio = SocketIO(app)
rabbit = SocketIO(message_queue='amqp://guest:guest@localhost:5672//', channel='jobs')


@socketio.on("task:start")
def task_start(data):
    print('in socket:task:start')
    socketio.emit('task:started', "Hang tight, working in it.")
    rabbit.emit('task:start', "Process this.")


# If I use threading instead of eventlet, then socketio.emit is tied to a different thread and the client never receives
@rabbit.on("task:complete")
def task_complete(data):
    print('in rabbit:task:complete')
    socketio.emit('task:complete', "All done, here you go: ___")


# At this point, pika starts, server starts - but server isn't receiving any 'emit's from client.
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
