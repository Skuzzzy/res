from twython import TwythonStreamer
from time import time as epochtime_s
import uuid
import ujson as json
import os
import codecs
import sqlite3
import ConfigParser

# remove this
import requests
requests.packages.urllib3.disable_warnings()
# end remove this


def current_ms():
    return int(epochtime_s() * 1000)

def get_n_minutes_ago(minutes):
    return current_ms() - (60000 * minutes)

class MongoStreamer(TwythonStreamer):
    def __init__(self):
        pass

    def on_success(self, data):
        if "text" in data:
            data["timestamp_ms"] = int(data.get("timestamp_ms")) # I receive data as unicode, I want to use this to select posts in a time range
            pp.pprint(data)

    def on_error(self, status_code, data):
        print "\n".join([status_code, data])
        # self.disconnect()

def obtain_authinfo(filename):
    conf = ConfigParser.RawConfigParser()
    conf.read("secret.cfg")

    info = {}
    info["consumer_key"] = conf.get("consumer", "consumer_key")
    info["consumer_secret"] = conf.get("consumer", "consumer_secret")
    info["access_token"] = conf.get("access", "access_token")
    info["access_token_secret"] = conf.get("access", "access_token_secret")
    return info

def obtain_streamer(auth):
    return MongoStreamer(auth["consumer_key"], auth["consumer_secret"],
                      auth["access_token"], auth["access_token_secret"])

if __name__ == "__main__":
    stream = obtain_streamer(obtain_authinfo("secret.cfg"))
    while True:
        try:
            stream.statuses.sample()
        except Exception as e:
            print str(e) # Ignore all exceptions
