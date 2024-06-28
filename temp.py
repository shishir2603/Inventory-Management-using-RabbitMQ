import pika
import json
import logging
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='health_check')
channel.queue_declare(queue='item_creation')
channel.queue_declare(queue='order_processing')
channel.queue_declare(queue='stock_management')
id = 1
quantity = 10
message = json.dumps({'id': id})
logging.info(message)
# Publish message to insert_record queue
channel.basic_publish(exchange='', routing_key='stock_management', body=message)
