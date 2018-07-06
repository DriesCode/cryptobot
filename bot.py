#!/usr/bin/env python

import sys
from twython import Twython

apiKey = 'iOhKEwNSrR4GTytmjmDGm1c0D'
apiSecret = 'SWS2KlcaJCWeVbVwpaF2tCGFZLu7fWAQS7P540E5ltQXUTvflw'
accessToken = '1015314683690213381-LlAi54CflV3X8MuV9RfU9J2fguUeTi'
accessTokenSecret = 'VPuDrvQdQBeUlV4uPafYh08rs1dJqzF0M0NUw37rwp1Jm'

api = Twython(apiKey, apiSecret, accessToken, accessTokenSecret)

def bot_tweet(text):
	tweet_text = "$ " + text
	api.update_status(status = tweet_text)
	print "Bot: " + tweet_text

bot_tweet('Hello World')
