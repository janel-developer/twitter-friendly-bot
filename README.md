# Twitter bot series - friendly bot

Friendly bot checks for new followers, and sends them a greeting. If the new follower is popular (trying to distinguish 'real' accounts), then friendly bot will also follow the new follower.

## Dependencies - what to install

This bot uses the following third party modules:

- tweepy (for access to Twitter api)
- psycopg2 (for interaction with postgresql)

Install these with pip in your virtual environment or globally. To learn how to work in virtual environments with python, you can read my [blog post here.](https://medium.com/@janelgbrandon/setting-up-a-python-development-environment-2e18447cbc24)

## Dependencies - database and enviroment variables

### Database requirements

This bot uses a postgresql db instance. It assumes that the following environment variables are exported (see db_connect.py):

- DBUSER (your postgresql user name)
- DBPW (your postgresql password)
- TWITTERDB (the database you are using for this bot)

This assumes you have a postgresql server instance running on port 5432 on localhost. You will have to modify the db_connect.py if you are using a non-default port or an external server.

You can create a database in your postgresql instance with a simple CREATE DATABASE command. You will have to do this before you use this bot, and specify the database name for the TWITTERDB environment variable. You can use an existing database if desired. I've created a database for all of my twitter bots called "twitterbot_dev", but you can do as you please.

### Authorization requirements

This bot authenticates with Twitter, and requires that you have a [developer account](https://developer.twitter.com/en/apply-for-access.html)

The bot assumes the following environment variables are set for authentication (see twitter_auth.py module). These values will be shown when you apply for a developer account, or when you view your developer account information in Twitter (at developer.twitter.com):

- TWITTER_CONSUMER_KEY
- TWITTER_CONSUMER_SECRET
- TWITTER_ACCESS_TOKEN_KEY
- TWITTER_ACCESS_TOKEN_SECRET

Additionally, this bot will retrieve information from your account, specifically your current list of friends (people you follow). This requires that you also set this environment variable (set it to your screen name):

- TWITTER_NAME

## Setting up the database

The create_db.py module is included to create the 'acknowledged_followers' table. This table will store the id, screen name for the new followers to whom you send a greeting. It will also store the date the acknowledgement was sent. When the bot runs, it will check this table to filter out new followers that haven't been sent a greeting yet. When it sends a greeting, that new followers information will be added to the table.

Run `python create_db.py` to create the table before you run the bot.

## Running the bot

Run the bot with `python greetings.py`
It will print messages to show connection and disconnect from the database, and to print a list of newly acknowledged followers and friends.

## The friend algorithm

The algorithm to choose who to follow back is simple at the moment. You can play with it to make it smarter. The friend algorithm and methods are implemented in the `friendly.py` module.

Currently, the bot gets the last 100 tweets for the new follower, and counts the number of likes on those 100 tweets. If the likes is greater than 50, it makes the new follower a friend.
