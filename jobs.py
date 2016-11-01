import time
from kombu import Connection, Exchange, Queue, Producer, Consumer
from kombu.async import Hub

hub = Hub()
exchange = Exchange('jobs')
queue = Queue('task:start', exchange, 'task:start')
conn = Connection('amqp://')
conn.register_with_event_loop(hub)
producer = Producer(conn)


def task_start(data):
    print('in jobs:task_start')
    time.sleep(10)
    producer.publish('All done.', exchange=exchange, routing_key='task:complete')


with Consumer(conn, [queue], on_message=task_start):
    hub.run_forever()
print(' [*] Waiting for messages. To exit press CTRL+C')