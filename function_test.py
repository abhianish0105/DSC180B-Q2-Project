from pulsar import Function
import re


class CounterFunction(Function):
    def __init__(self):
        self.output_topic = 'persistent://twitter-abhi/default/counter-abhi-topic'

    def process(self, input, context):
        try:
            """
            Pre processing of tweets by removing links from tweets that have already been filtered and sent from producer.
            """
            tweet = str(input)
            context.publish(self.output_topic, re.sub(r'https?://\S*', '', tweet))

        except:
            warning = "Negaaahtive Ghostrider. {}".format(input)
            context.get_logger().warn(warning)
