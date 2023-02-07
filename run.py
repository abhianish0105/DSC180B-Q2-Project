import sys
import os
import json

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
        sentiment = len(i)
        if sentiment == "negative":
          negatives += 1
        if sentiment == "positive":
          positives += 1
        if sentiment == "neutral":
          neutrals += 1

      #output
      print("Positives: " + str(positives))
      print("Negatives: " + str(negatives))
      print("Neutrals: " + str(neutrals))


if __name__ == '__main__':
    targets = sys.argv[1:]
    main(targets)
