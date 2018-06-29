from __future__ import unicode_literals
from __future__ import absolute_import, print_function
import youtube_dl
# author=rhnvrm<hello@rohanverma.net>
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import key
global api
import os
import datetime
import lone_feed_gen
import random
import string
import re
from urllib import parse


class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def parse_tweet(self, tweet_text):
        url_regex = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        link = url_regex.findall(tweet_text)[0]
        title = tweet_text.strip("#personal-feed")
        title2 = title.strip("link")
        return {'title':title2, 'link':link}


    def on_data(self, data):
        d = json.loads(data)
        print(d)
        parsed_tweet = self.parse_tweet(d['text'])
        screen_name = d['user']['screen_name']
        tweetId = d['id']
        print(parsed_tweet)
#       self.download_aud(parsed_tweet['link'], parsed_tweet'title', screen_name, tweetId)
        return True

    def on_direct_message(self, data):
        print(data)

    def on_error(self, status):
        print(status)

    def download_aud(self, urll, title, screen_name, tweet_id):
        os.mkdir(title)
        os.chdir(title)
        ydl_opts = {
            'format':
            'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': '%(playlist_index)s---%(title)s-%(id)s.%(ext)s'
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([urll])
        os.chdir('../')
        file_string = lone_feed_gen.generate_feed(title).split('/')[1]
        os.chdir('../')
        self.reply(file_string, screen_name, tweet_id)

    def reply(self, file_string, screen_name, tweet_id):
        link_text = parse.quote("http://sailor.pictures/{}".format(file_string))
        api.update_status("@{} {}".format(tweet_id, link_text), tweet_id)
        


def start():
    stream.filter(track=["#personal-feed"])

nolonger = StdOutListener()
auth = OAuthHandler(key.consumer_key, key.consumer_secret)
auth.set_access_token(key.access_token, key.access_token_secret)
api = tweepy.API(auth)
stream = Stream(auth, nolonger)
 
start()
