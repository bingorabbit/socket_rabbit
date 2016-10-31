import eventlet
eventlet.monkey_patch()

import os, pika
from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS

SECRET_KEY = 'super-secret'
app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = SECRET_KEY
socketio = SocketIO(app)


@socketio.on("heavy_task")
def heavy_task():
    socketio.emit('task_initiated', "Hang tight, working in it.")
    channel.basic_publish(exchange='', routing_key='heavy_task', body="Process this.")


def task_complete():
    socketio.emit('task_complete', "All done, here you go: ___")


channel = None
def start_pika():
    global channel
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='heavy_task')
    channel.queue_declare(queue='task_complete')
    channel.basic_consume(task_complete, queue='task_complete', no_ack=True)
    channel.start_consuming()


if __name__ == '__main__':
    eventlet.spawn(start_pika)
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=True)