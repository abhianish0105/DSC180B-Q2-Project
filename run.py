import sys
import os
import json
import transformers
from transformers import pipeline
import logging

def main(targets):

    if 'test' in targets: 
      #reads tweets from txt file line by line and adds them to list
      with open('test_data.txt') as file:
        tweets = [line.rstrip() for line in file]

      negatives = 0
      positives = 0
      neutrals = 0

      #apply sentiment model
      for i in tweets:
        sentiment = pipeline("sentiment-analysis", model = 'cardiffnlp/twitter-roberta-base-sentiment-latest')
        if sentiment(i)[0]['label'] == "negative":
          negatives += 1
        if sentiment(i)[0]['label'] == "positive":
          positives += 1
        if sentiment(i)[0]['label'] == "neutral":
          neutrals += 1

      #output
      print("Positives: " + str(positives))
      print("Negatives: " + str(negatives))
      print("Neutrals: " + str(neutrals))


if __name__ == '__main__':
    targets = sys.argv[1:]
    main(targets)
