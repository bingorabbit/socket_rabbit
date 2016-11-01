import eventlet
eventlet.monkey_patch()

from kombu import Connection, Exchange, Queue, Producer, Consumer
from kombu.async import Hub

from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'
CORS(app,resources={r"/*":{"origins":"*"}})
socketio = SocketIO(app)


hub = Hub()
exchange = Exchange('jobs')
queue = Queue('task:complete', exchange, 'task:complete')
conn = Connection('amqp://')
conn.register_with_event_loop(hub)
producer = Producer(conn)



@socketio.on("task:start")
def task_start(data):
    print('in socket:task:start')
    socketio.emit('task:started', "Hang tight, working in it.")
    producer.publish('Process this.', exchange=exchange, routing_key='task:start')


# If I use threading instead of eventlet, then socketio.emit is tied to a different thread and the client never receives
def task_complete(message):
    print('in rabbit:task:complete')
    socketio.emit('task:complete', "All done, here you go: ___")


def start_hub():
    with Consumer(conn, [queue], on_message=task_complete):
        hub.run_forever()


# At this point, pika starts, server starts - but server isn't receiving any 'emit's from client.
if __name__ == '__main__':
    eventlet.spawn(start_hub)
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
