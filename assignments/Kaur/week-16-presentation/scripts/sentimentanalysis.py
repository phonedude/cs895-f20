import json 
import re 
from textblob import TextBlob 

def clean_tweet(tweet): 
        
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())


def get_tweet_sentiment(tweet): 
        
        analysis = TextBlob(clean_tweet(tweet)) 
        if analysis.sentiment.polarity > 0: 
            return 'positive' 
        elif analysis.sentiment.polarity == 0: 
            return 'neutral'
        else: 
            return 'negative'

def get_tweet_polarityt(tweet): 
        
        analysis = TextBlob(clean_tweet(tweet)) 
        return analysis.sentiment.polarity 
 
f = open('tweets.json',)   
tweetsAll = []
data = json.load(f) 
print(len(data))
for tweet in data: 
    parsed_tweet = {} 
    parsed_tweet['tweet_id'] = tweet[0]
    parsed_tweet['tweet_text'] = tweet[1]
    parsed_tweet['sentiment'] = get_tweet_sentiment(tweet[1])
    parsed_tweet['polarity'] = get_tweet_polarityt(tweet[1])

    tweetsAll.append(parsed_tweet) 
print(len(tweetsAll))

f = open("sentimentOfTweet.json", "a")
f.write(str(tweetsAll))
f.close()




