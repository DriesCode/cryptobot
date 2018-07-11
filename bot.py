#!/usr/bin/env python

import sys
import time
import keys
import binascii
import hashlib
from twython import Twython
from random import randint

api = Twython(keys.apiKey, keys.apiSecret, keys.accessToken, keys.accessTokenSecret)
auth = api.get_authentication_tokens()

oauthToken = auth['oauth_token']
oauthTokenSecret = auth['oauth_token_secret']

# twitter functions
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
	del list[:]
	for x in dict:
		list.append(x)

def delay(secs):
	for l in range(0, secs):
		print l
		time.sleep(1)

def send_dm(userid, text):
	api.send_direct_message(user_id=userid, text=text)

# cryptography functions

abcNMin = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h', 9: 'i', 10: 'j', 11: 'k',
		12: 'l', 13: 'm', 14: 'n', 15: 'o', 16: 'p', 17: 'q', 18: 'r', 19: 's', 20: 't', 21: 'u',
		22: 'v', 23: 'w', 24: 'x', 25: 'y', 26: 'z'}

abcNMay = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H', 9: 'I', 10: 'J', 11: 'K',
		12: 'L', 13: 'M', 14: 'N', 15: 'O', 16: 'P', 17: 'Q', 18: 'R', 19: 'S', 20: 'T', 21: 'U',
		22: 'V', 23: 'W', 24: 'X', 25: 'Y', 26: 'Z'}

abcLMin = {v: k for k, v in abcNMin.iteritems()}
abcLMay = {v: k for k, v in abcNMay.iteritems()}

nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

techs = {1: 'caesar', 2: 'binary', 3: 'ROT13', 4: 'MD5'}

def shiftText(text_c, n, tech):
	crypto_c = []

	for x in range(0, (len(text_c))):
			if (text_c[x] in abcLMin):
				enc_ch = None
				if ((abcLMin[text_c[x]] + n) > 26):
					enc_ch = abcNMin[(abcLMin[text_c[x]] + n) - 26]
				else:
					enc_ch = abcNMin[abcLMin[text_c[x]] + n]
				crypto_c.append(enc_ch)
			elif (text_c[x] in abcLMay):
				enc_ch = None
				if ((abcLMay[text_c[x]] + n) > 26):
					enc_ch = abcNMay[(abcLMay[text_c[x]] + n) - 26]
				else:
					enc_ch = abcNMay[abcLMay[text_c[x]] + n]
				crypto_c.append(enc_ch)
			elif (text_c[x] in nums):
				if (tech == 1):
					if (n >= 20):
						enc_ch = ((text_c[x] + (n-20))-10)
					elif (n >= 10):
						enc_ch = ((text_c[x] + (n-10))-10)
					else:
						enc_ch = ((text_c[x] + n)-10)
				if (tech == 3):
					if (text_c[x] + 3 > len(nums)):
						enc_ch = (text_c[x] + 3) - 10
					else:
						enc_ch = text_c[x] + 3
				crypto_c.append(enc_ch)
			else:
				crypto_c.append(text_c[x])
				
	return ''.join(crypto_c).encode('utf-8').strip()


def encrypt(tech, plain_text):
	pt_c = []
	
	for c in plain_text:
			pt_c.append(c)

	if (tech == 1): # Caesar
		key = randint(1, 26)
		return shiftText(pt_c, key, tech)
	if (tech == 2): # Binary
		return str(bin(int(binascii.hexlify(plain_text), 16))).replace('b', '')
	if (tech == 3): # ROT13
		return shiftText(pt_c, 13, tech)
	if (tech == 4):
		m = hashlib.md5()
		m.update(plain_text)
		return m.hexdigest()


def chooseEncrypt(tweet):
	tweetText = tweet['text']
	ri = randint(1, len(techs))

	if (len(tweetText) <= 30):
		if ri == 1:
			return 1
		elif ri == 2:
			return 2
		elif ri == 3:
			return 3
		elif ri == 4:
			return 4
	if ri == 2:
		ri2 = randint(1, len(techs)-1)
		if ri2 == 1:
			ri+=1
		elif ri2 == 2:
			ri-=1
	if ri == 1:
		return 1
	elif ri == 3:
		return 3
	elif ri == 4:
		return 4


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
		print lt
		parse_list(mentions(lt), mts)
	elif (n == 0):
		parse_list(mentions(lastTweet), mts)

	print "mts: " + str(len(mts))
	print "n: " + str(n)

	delay(30)
	#time.sleep(30)

	if ((len(mts)>0) and (start == 1)):
		#print "Inside loop 1"
		start = 0
		n = 0
		for i in mts:
			t = chooseEncrypt(i)
			replyTweet = reply(api, i, "@"+i['user']['screen_name']+" "+str(encrypt(t, str(i['text'].replace('@_cryptobot', '')))))
			reply(api, replyTweet, "@"+i['user']['screen_name']+" "+"Technique used is: " + techs[t])
			#send_dm(i['user']['id'], "Technique used for: '" + i['text'] + "' is " + techs[t])
			lastTweet = i['id']
			#print lastTweet
			print str(n) + " Replied to " + i['user']['screen_name']
			#time.sleep(60)
			delay(30)