import time, pika

def task_start():
    print('in job:task:start')
    time.sleep(10)
    channel.basic_publish(routing_key='task:complete', body="Done")

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel(exchange='jobs', )
channel.queue_declare(queue='task:start')
channel.queue_declare(queue='task:complete')
channel.basic_consume(task_start, queue='task:start', no_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()