#-*- coding: utf-8 -*-

import pika
import sys

parameters = pika.URLParameters("amqp://fenomenlog:fenomenlogpass9@"
                                "localhost:5672/fenomenlog")

connection = pika.BlockingConnection(parameters)

channel = connection.channel()

text = 'message body value'
try:
    text = sys.argv[1]
except:
    pass

channel.basic_publish('fenomen',
                      'fenomen.log',
                      text,
                      pika.BasicProperties(content_type='text/plain',
                                           delivery_mode=1))

connection.close()
