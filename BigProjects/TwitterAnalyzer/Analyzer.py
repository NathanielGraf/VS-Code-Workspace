#Package for Regex
from multiprocessing.connection import Client
import re
#Twitter API
import tweepy
from tweepy import OAuthHandler
#Python text processing library
from textblob import TextBlob


class TwitterClient(object):
	def __init__(self):
		#Twitter Dev Keys
        #Access Token 1458197860135079946-i5D4OFonTnzpaALXEafh2i9JKbPD3l
        #Access Secret b7KxEUkvMXo0eIaSCgPnjRCF76MPNgPwhZ5I8urbkLeYA
        #API Key dend4NlGsURVZrjwBH8ihiLj9
        #API Key Secret 1ifBfL2lvltWlnD6lJMXoqW4acU8PCJVW0vDN3K1mPgZR4Mk1m
        #Bearer Token AAAAAAAAAAAAAAAAAAAAADM2hQEAAAAAW79WcF5KNhY7YZjE9FbG859jia4%3DUwV4e0CaPiytmkuWxzkIlhp7UAjY2CXdlCepa48LhZo1lL9yFw
		consumer_key = 'dend4NlGsURVZrjwBH8ihiLj9'
		consumer_secret = '1ifBfL2lvltWlnD6lJMXoqW4acU8PCJVW0vDN3K1mPgZR4Mk1m'
		access_token = '1458197860135079946-i5D4OFonTnzpaALXEafh2i9JKbPD3l'
		access_token_secret = 'b7KxEUkvMXo0eIaSCgPnjRCF76MPNgPwhZ5I8urbkLeYA'

		# attempt authentication
		try:
			# create OAuthHandler object
			self.auth = OAuthHandler(consumer_key, consumer_secret)
			# set access token and secret
			self.auth.set_access_token(access_token, access_token_secret)
			# create tweepy API object to fetch tweets
			self.api = tweepy.API(self.auth)
		except:
			print("Error: Authentication Failed")

	def clean_tweet(self, tweet):
		'''
		Utility function to clean tweet text by removing links, special characters
		using simple regex statements.
		'''
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
									

	def get_tweet_sentiment(self, tweet):
		'''
		Utility function to classify sentiment of passed tweet
		using textblob's sentiment method
		'''
		# create TextBlob object of passed tweet text
		analysis = TextBlob(self.clean_tweet(tweet))
		# set sentiment
		if analysis.sentiment.polarity > 0:
			return 'positive'
		elif analysis.sentiment.polarity == 0:
			return 'neutral'
		else:
			return 'negative'

	def get_tweets(self, query, count):
		'''
		Main function to fetch tweets and parse them.
		'''
		# empty list to store parsed tweets
		tweets = []

		try:
			# call twitter api to fetch tweets
			fetched_tweets = self.api.search_tweets(q = query, count = count)

			# parsing tweets one by one
			for tweet in fetched_tweets:
				# empty dictionary to store required params of a tweet
				parsed_tweet = {}

				# saving text of tweet
				parsed_tweet['text'] = tweet.text
				# saving sentiment of tweet
				parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

				# appending parsed tweet to tweets list
				if tweet.retweet_count > 0:
					# if tweet has retweets, ensure that it is appended only once
					if parsed_tweet not in tweets:
						tweets.append(parsed_tweet)
				else:
					tweets.append(parsed_tweet)

			# return parsed tweets
			return tweets
		#Commented 1st and 3rd line
		except tweepy.errors.TweepyException as e:
		# print error (if any)
			print("Error : " + str(e))

def main():
	# creating object of TwitterClient Class
	api = TwitterClient()
	# calling function to get tweets
	tweets = api.get_tweets(query = 'Donald Trump', count = 200)

	# picking positive tweets from tweets
	ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
	# percentage of positive tweets
	print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
	# picking negative tweets from tweets
	ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
	# percentage of negative tweets
	print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
	# percentage of neutral tweets
	print("Neutral tweets percentage: {} % \
		".format(100*(len(tweets) -(len( ntweets )+len( ptweets)))/len(tweets)))

	# printing first 5 positive tweets
	print("\n\nPositive tweets:")
	for tweet in ptweets[:10]:
		print(tweet['text'])

	# printing first 5 negative tweets
	print("\n\nNegative tweets:")
	for tweet in ntweets[:10]:
		print(tweet['text'])

if __name__ == "__main__":
	# calling main function
	main()
