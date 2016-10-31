import time, pika

def heavy_task():
    time.sleep(10)
    channel.basic_publish(exchange='', routing_key='task_complete', body="Done")

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='heavy_task')
channel.queue_declare(queue='task_complete')
channel.basic_consume(heavy_task, queue='heavy_task', no_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()