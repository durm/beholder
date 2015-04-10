#-*- coding: utf-8 -*-

import pika

parameters = pika.URLParameters('amqp://fenomenlog:fenomenlogpass9@localhost:5672/fenomenlog')

connection = pika.BlockingConnection(parameters)

channel = connection.channel()

channel.basic_publish('fenomen',
                      'fenomen.log',
                      'message body value',
                      pika.BasicProperties(content_type='text/plain',
                                           delivery_mode=1))

connection.close()
