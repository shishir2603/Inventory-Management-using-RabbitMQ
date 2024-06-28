#!/usr/bin/env python
import pika, sys, os
import json
import logging
import pymongo

# Connect to MongoDB database
client = pymongo.MongoClient("<your mongodb connection string>")
db = client["CCRabitMQ"]
collection = db["Item"]

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='stock_management')

    def callback(ch, method, properties, body):
        body = body.decode()
        body = json.loads(body)

        item_id = body['id']
        order_quantity = int(body['quantity'])

        # Fetch item from the database
        item = collection.find_one({"id": item_id})

        if item:
            current_quantity = int(item['quantity'])  # Ensure int
            new_quantity = current_quantity - order_quantity

            if new_quantity <= 0:
                # delete the item if the quantity is zero
                collection.delete_one({"id": item_id})
            else:
                # else update quantity
                collection.update_one({"id": item_id}, {"$set": {"quantity": new_quantity}})

        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue='stock_management', on_message_callback=callback, auto_ack=False)

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
