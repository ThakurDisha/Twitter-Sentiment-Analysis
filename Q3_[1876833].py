import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from textblob import TextBlob
import sqlite3
import secret_keys



#Authentication
auth = tweepy.OAuthHandler(secret_keys.consumer_key, secret_keys.consumer_secret)

auth.set_access_token(secret_keys.access_token, secret_keys.access_secret)

api = tweepy.API(auth)


conn=sqlite3.connect('Q3_sqlite_[1876833].sqlite')
a=conn.cursor()

class Stream_data(tweepy.StreamListener):

	def on_status(self, status):

		#creating a table in the database
		a.execute("""CREATE TABLE IF NOT EXISTS tweet_data (user_id INTEGER,
			tweet_text TEXT,
			creation_date DATETIME,
			user_location INTEGER,
			user_follower INTEGER,
			user_friends INTEGER,
			sentiment_analysis_polarity REAL,
			sentiment_analysis_subjectivity REAL)""")
		
		#Defining variables to be inserted in the table
		user_id=status.user.id
		tweet_text=status.text 
		date_created=status.created_at
		user_location=status.user.location
		user_follower=status.user.followers_count
		user_friends=status.user.friends_count
		tweets_data=TextBlob(tweet_text)
		sentiment_analysis=tweets_data.sentiment

		#Inserting values in the database
		a.execute("""INSERT INTO tweet_data(user_id,
			tweet_text,
			creation_date,
			user_location,
			user_follower,
			user_friends,
			sentiment_analysis_polarity,
			sentiment_analysis_subjectivity) VALUES (?,?,?,?,?,?,?,?)""",(user_id,
				tweet_text,
				date_created,
				user_location,
				user_follower,
				user_friends,
				sentiment_analysis.polarity,
				sentiment_analysis.subjectivity))
		conn.commit()



	def on_error(self, status_code):
		#Prints the status code in the event of an error
		print(status_code)


Stream_listener = Stream_data()
twitter_tweets = tweepy.Stream(auth=api.auth, listener=Stream_listener, lang=["en"])
#Tracking the keyword to be analyzed
twitter_tweets.filter(track=["Trump"])

conn.close()
