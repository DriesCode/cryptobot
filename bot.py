#!/usr/bin/env python

import sys
import time
import keys
from twython import Twython
from random import randint

api = Twython(keys.apiKey, keys.apiSecret, keys.accessToken, keys.accessTokenSecret)
auth = api.get_authentication_tokens()

oauthToken = auth['oauth_token']
oauthTokenSecret = auth['oauth_token_secret']

def search(text):
	results = api.cursor(api.search, q=text, count=1)
	return results

def bot_tweet(text):
	tweet_text = "$ " + text
	api.update_status(status = tweet_text)
	print "Bot: " + tweet_text


def reply(client, tweet, reply):
	tid = tweet['id']
	author = tweet['user']['screen_name']
	r = client.update_status(status=reply, in_reply_to_status_id=tid)
	return r

def mentions(sid):
	m = '@_cryptobot'
	ment = api.get_mentions_timeline(since_id=sid)
	for mnt in ment:
		if (mnt['in_reply_to_status_id'] is None):
			if m in mnt['text']:
				yield mnt

def parse_list(dict, list):
	for h in range(0, (len(list))):
		print "Removed item num " + str(h) + ": " + str(list[h])
		list.remove(list[h])

	for x in dict:
		list.append(x)

def delay(secs):
	for l in range(0, secs):
		print l
		time.sleep(1)

# main loop
global mts
global mtsT
global n
global lastTweet

mts = []
mtsT = []
n = 1
lastTweet = None

while True:
	start = 1
	if (n == 1):
		lt = api.get_user_timeline(screen_name='_cryptobot', count=1)[0]['id']
		print "Init edge: " + str(lt)
		parse_list(mentions(lt), mts)
	elif (n == 0):
		parse_list(mentions(lastTweet), mts)

	print "Listed mentions..."
	print "mst: " + str(len(mts))
	print "n: " + str(n)

	delay(30)

	if ((len(mts)>0) and (start == 1)):
		print "Inside loop 1"
		start = 0
		n = 0
		for i in mts:
			reply(api, i, "@"+i['user']['screen_name']+" OK: " + str(randint(0, 100000)))
			lastTweet = i['id']
			print lastTweet
			print str(n) + " Replied to " + i['user']['screen_name']
			delay(60)
