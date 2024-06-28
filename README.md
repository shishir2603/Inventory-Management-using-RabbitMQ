## Inventory Management using RabbitMQ for interprocess communication

The application contains Micro-serviced based inventory management system built using Flask (python) , mongodb and rabbitmq .

## Features

- <b>RabbitMQ</b>  - makes use of RabbitMQ as message broker for interprocess communication
- <b>Docker Containerization</b>  - makes use of Docker compose for multi-container management 
- <b>MongoDB</b> - uses MongoDB as a database for storage of the user inputs.


## Before running the application

- Make Sure your system has docker installed and is running.

- Before running the application , make sure to add your MongoDB connection string in the files insertion.py , order_processing.py and stock_management.py

## To execute the application

To execute the application , first run 

```
docker compose build
```

Then execute ,

```
docker compose up
```

and open localhost:5000 to view the page

## To stop the application
To stop the execution , press Ctrl+c and then run 

```
docker compose down
```
