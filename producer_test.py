import os
import pulsar
import time
import random
import string
import logging
import sys
import tweepy
from tweepy import StreamingClient, StreamRule
import csv
from transformers import pipeline
import tensorflow

class IDPrinter(tweepy.StreamingClient):

    def __init__(self, producer, key):
        self.producer = producer
        super().__init__(key)


    def on_tweet(self, tweet):
        self.producer.send(tweet.text)
        print(tweet.text)
        time.sleep(3)

class Producer(object):
    """
    Create a pulsar producer that writes random messages to a topic
    """
    def __init__(self):
        self.token = os.getenv("ASTRA_STREAMING_TOKEN")
        self.service_url = os.getenv("ASTRA_STREAMING_URL")
        self.topic = os.getenv("ASTRA_TOPIC")
        self.client = pulsar.Client(self.service_url,
                                    authentication=pulsar.AuthenticationToken(self.token))
        self.producer = self.client.create_producer(self.topic)

    def send(self, message):
        self.producer.send(message.encode('utf-8'))

    def produce_messages(self):
        """
        Create and send random messages
        """
        streaming_client = tweepy.StreamingClient("API key")
        printer = IDPrinter("API key")
        time.sleep(1)





def produce_messages():
    """
    Create an instance of the producer and fire it up to send messages until the program is terminated
    """
    producer = Producer()
    producer.produce_messages()
    producer.client.close()


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout,
                        level=logging.INFO)
    produce_messages()
