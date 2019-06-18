import sqlite3
import csv
import io
import datetime
from textblob import TextBlob
import matplotlib.pyplot as plt
import csv
from collections import defaultdict
import sqlite3
from matplotlib.dates import date2num





conn=sqlite3.connect('Q3_sqlite_[1876833].sqlite')
cursor=conn.cursor()
 #selecting all the data in the table
db="SELECT * FROM tweet_data;"
cursor.execute(db)
columns = [i[0] for i in cursor.description]
#fetching all the data in tweets variable
tweets=cursor.fetchall()


#There was an error of charmap encoding, so I goggled the solution to it and
#therefore added encoding utf-8 and imported io.The soultion to it,I found on the link below.  
#https://stackoverflow.com/questions/27092833/unicodeencodeerror-charmap-codec-cant-encode-characters
with io.open("Q3_csv_[1876833].csv", "w",newline='',encoding="utf-8") as csvwriter:
	#writing all the fetched data in csv file
	writer = csv.writer(csvwriter)
	writer.writerow(columns)
	for row in tweets:
		writer.writerow(row)



count=0
with open('Q3_csv_[1876833].csv','r',encoding="utf-8") as csvfile:
	#reading from the csv file
	reader = csv.reader(csvfile, delimiter=",")
	alist=[]
	alist_1=[]
	negative_tweeets=[]
	alist2=[]
	alist3=[]
	dates_list=[]
	dates=[]
	dates1=[]
	dates2=[]

	tweets_text=[]

	positive_tweets=[]
	neutral_tweets=[]
	negative_tweets=[]

	count=0
	next(csvfile)
	for row in reader:
		#storing all the sentiments polarity contained in row 6
		r=row[6]
		alist.append(float(r))
		# storing all the tweets contained in row 1
		tweet=row[1]
		alist2.append(tweet)
		#storing all the date&time contained in row 2
		time=row[2]
		alist3.append(time)


		for date in alist3:
			#converting the dates and time from 'string' type to python datetime module format
			dt=datetime.datetime.strptime(date,'%Y-%m-%d %H:%M:%S')
		dates_list.append(dt)
	# print(dates)



	alist_1.extend(alist)
	for i in alist_1:
		if i>=0.0:
			positive_tweets.append(i)
		else:
			negative_tweets.append(i)
			dates2.append(time)

mapped=zip(positive_tweets,dates_list)
mapped=set(mapped)
pos,date1=zip(*mapped)
date1=sorted(date1)

x=zip(negative_tweets,dates_list)
x=set(x)
neg,date3=zip(*x)
date3=sorted(date3)

t=zip(alist2,dates_list)
t=set(t)
tweets,date2=zip(*t)
date2=sorted(date2)

# plotting the graph of the sentiment versus time
plt.plot(date1,pos,'g',label='Positive')
plt.plot(date3,neg,'r',label='Negative')
plt.title("Tweets Sentiments Display")
plt.xlabel("Time Period")
plt.ylabel("Sentiment ranging from -1 to 1")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("Q4_graphs_sentiment[1876833]")
plt.show()



# plotting the graph of the frequency of tweets versus time
plt.plot(date2,tweets)
plt.yticks([])
plt.ylabel("Frequency Of Tweets")
plt.xlabel("Time Period")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("Q4_graphs_frequency[1876833]")
plt.show()




