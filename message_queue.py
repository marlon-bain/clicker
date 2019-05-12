import pika
import config
import time


class MessageQueue:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=config.RABBITMQ_CHANNEL)

    def drain(self):
        messages = self.get_messages()
        print("Drained {0} messages from queue".format(len(messages)))

    def get_messages(self):
        messages = []
        method_frame, header_frame, body = self.channel.basic_get(config.RABBITMQ_CHANNEL, auto_ack=True)

        while method_frame is not None:
            messages.append(body)
            time.sleep(0.01)
            method_frame, header_frame, body = self.channel.basic_get(config.RABBITMQ_CHANNEL, auto_ack=True)

        return messages
