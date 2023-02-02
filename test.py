import os
import pulsar
import time
import random
import string
import logging
import sys
import tweepy
import numpy
from tweepy import StreamingClient, StreamRule
from producer_test import Producer, IDPrinter

"""
Create a producer and printer object from the respective classes to be used to ingest raw tweets from Twitter API.
"""
producer = Producer()
printer = IDPrinter(producer, "API key")

"""
Add new rules and delete previous rules from previous runs.
"""
rule_ids = []
result = printer.get_rules()
for rule in result.data:
    rule_ids.append(rule.id)
print(rule_ids)
if (len(rule_ids) > 0):
    printer.delete_rules(rule_ids)

"""
Add rules to identify certain key words, remove tweets with certain features, and keep tweets with other ones.
"""
printer.add_rules(StreamRule('"pandemic" '))
printer.add_rules(StreamRule('"remote work" '))
printer.add_rules(StreamRule('lang:en'))
printer.add_rules(StreamRule('-is:quote'))
printer.add_rules(StreamRule('-has:cashtags'))
printer.add_rules(StreamRule('-has:media'))
printer.add_rules(StreamRule('has:hashtags'))
printer.add_rules(StreamRule('-is:retweet'))

printer.filter()
printer.sample()
