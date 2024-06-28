#!/usr/bin/env python
import pika
import sys
import os
import pymongo
import json

# Connect to MongoDB database
client = pymongo.MongoClient("<your mongodb connection string>")
db = client["CCRabitMQ"]
collection = db["Item"]
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()
channel.queue_declare(queue='order_processing')
channel.queue_declare(queue='return_order_processing')


def read_orders_from_database():
    orders = collection.find({})
    orders_list = []
    for order in orders:
        orders_list.append(order)
    return json.dumps(orders_list, default=str)  # Convert list of orders to JSON

def callback(ch, method, properties, body):
    orders_json = read_orders_from_database()
    print(orders_json)
    channel.basic_publish(exchange='', routing_key='return_order_processing', body=orders_json)
    #ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    channel.basic_consume(queue='order_processing', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
