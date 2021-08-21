import logging
import os
import time

import requests
import tweepy
from dotenv import load_dotenv, set_key

# logging stuff #

# create a logger object with the filename's name
log = logging.getLogger(__name__)
# set its level to DEBUG (logs every event)
log.setLevel(logging.DEBUG)
# create a StreamHandler, this is used to handle streaming logs
handler = logging.StreamHandler()
# create a Formatter, this contains the log message format and date format
formatter = logging.Formatter(
    "[%(loglevel)s] [%(asctime)s] %(message)s",
    "%d/%m/%Y %H:%M:%S",
)
# add the formatter to the handler
handler.setFormatter(formatter)
# add the handler to the Logger
log.addHandler(handler)
log.info("Started")
load_dotenv()


auth = tweepy.OAuthHandler(os.environ["API_KEY"], os.environ["API_SECRET"])
auth.set_access_token(os.environ["USER_TOKEN"], os.environ["USER_SECRET"])

api = tweepy.API(auth)

user = api.get_user(int(os.environ["USER_ID"]))
log.debug("User %s (%s) retrieved", user.name, user.screen_name)


# repeat every 30 minutes from here
while True:
    tl = user.timeline()

    log.debug("User timeline retrieved")

    for tweet in tl:
        tweet: tweepy.Status
        # tweets are ordered by time, most recent ones first

        if tweet.id <= int(os.environ["LAST_STATUS_ID"]):
            # first tweet on tl is the same as before
            # could also be a rt
            log.debug("Tweets are stale")
            break

        # tweet is newer than the last one, set new ID
        os.environ["LAST_STATUS_ID"] = tweet.id_str
        set_key(".env", "LAST_STATUS_ID", tweet.id_str, quote_mode="auto")
        log.debug("last_status_id updated to %s", tweet.id_str)
        if tweet.author.id != int(os.environ["USER_ID"]):
            # this is a retweet from someone else, ignore
            log.debug("Tweet is not by specified user")
            break

        if tweet.in_reply_to_status_id:
            # tweet is a reply tweet, ignore
            log.debug("Tweet is a reply post")
            break

        # tweet is a new status, not a rt or reply, now post
        tweet_url = (
            f"https://twitter.com/{tweet.author.screen_name}/status/{tweet.id_str}"
        )
        log.debug("Posting %s to discord...", tweet_url)
        requests.post(
            os.environ["WEBHOOK_URL"],
            json={"content": tweet_url},
        )
        log.debug("Successfully posted!")

    time.sleep(60 * 30)
    # wait 30 mins to check for the next update, that seems reasonable
