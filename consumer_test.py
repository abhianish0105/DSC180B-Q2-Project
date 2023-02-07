import pulsar
import time
import os
import logging
import sys
import tweepy
import csv
import transformers
from transformers import pipeline
import numpy

class Consumer(object):
    """
    Create a pulsar producer that writes random messages to a topic
    """
    def __init__(self):
        self.token = os.getenv("ASTRA_STREAMING_TOKEN")
        self.service_url = os.getenv("ASTRA_STREAMING_URL")
        self.subscription = "persistent://twitter-abhi/default/counter-abhi-topic"
        self.client = pulsar.Client(self.service_url,
                                    authentication=pulsar.AuthenticationToken(self.token))
        self.consumer = self.client.subscribe(self.subscription, 'my-subscription')

    def read_messages(self):
        """
        Create and send random messages
        """
        neutrals = 0
        negatives = 0
        positives = 0
        total = 0
        while True:
            try:
                msg = self.consumer.receive(2000)

                """
                Take pipeline from pre-trained model to send tweets through to be given a label and score pased on sentiment and polarity, respectively.
                """
                sentiment_pipeline = pipeline("sentiment-analysis", model = 'cardiffnlp/twitter-roberta-base-sentiment-latest')
                logging.info('{}'.format(sentiment_pipeline(msg.data().decode("utf-8"))))
                logging.info('{}'.format(msg.data().decode("utf-8")))

                with open('tweet_output.txt', 'w') as f:
                    """
                    Update count of total sentiments as tweets are streamed.
                    """
                    writer = csv.writer(f)
                    if sentiment_pipeline(msg.data().decode("utf-8"))[0]['label'] == "neutral":
                        neutrals += 1
                    else:
                        if sentiment_pipeline(msg.data().decode("utf-8"))[0]['label'] == "negative":
                            negatives += 1
                        else:
                            positives += 1
                    total += 1

                    writer.writerow(['neutral: ' + str(neutrals)])
                    writer.writerow(['negative: ' + str(negatives)])
                    writer.writerow(['positive: ' + str(positives)])
                    writer.writerow([''])
                    writer.writerow(['total: ' + str(total)])

                print('Sentiment written to CSV successfully!')
                # Acknowledging the message to remove from message backlog
                self.consumer.acknowledge(msg)

            except:
                logging.info("Still waiting for a message...");
            time.sleep(1)


def read_messages():
    """
    Create an instance of the consumer and
    Fire it up to read messages until the program is terminated
    """
    consumer = Consumer()
    consumer.read_messages()
    consumer.client.close()


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout,
                        level=logging.INFO)
    read_messages()
