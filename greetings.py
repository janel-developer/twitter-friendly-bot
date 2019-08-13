import os
from psycopg2 import Error
import twitter_auth
import db_connect
import friendly

# Constants
MY_SCREEN_NAME = os.getenv("TWITTER_NAME")


def say_hi(recent_followers):
    # Says hi and thanks to new followers

    for follower in recent_followers:
        message = f'Hi @{follower.screen_name}, thanks for following me!'
        api.update_status(message)


def collect_follower_ids(records):
    # Creates a list of follower ids from records returned from the database query on acknowledged_followers

    follower_ids = []
    for record in records:
        follower_ids.append(record[0])

    return follower_ids


def get_acked_followers():
    # Returns a list of follower ids for already acknowledged followers

    connection = db_connect.connect_to_db()
    cursor = connection.cursor()
    follower_records = []
    get_acked_followers_query = '''SELECT "follower_id" FROM acknowledged_followers order by date_sent desc;'''
    try:
        cursor.execute(get_acked_followers_query)
        follower_records = cursor.fetchall()

    except (Exception, Error) as error:
        print("Error while fetching data from PostgreSQL", error)
    finally:
        # closing database connection.
        db_connect.close_db(connection)
    return collect_follower_ids(follower_records)


def get_new_followers(followers):
    # Collects the list of new followers that have not been acknowledged

    new_followers = []
    acked_followers = get_acked_followers()
    for follower in followers:
        if not follower.id in acked_followers:
            new_followers.append(follower)
    return new_followers


def add_acknowledged_follower(connection, follower):
    # Adds information for a new follower to the acknowledged_followers table

    id = follower.id
    screen_name = follower.screen_name
    cursor = connection.cursor()
    postgres_insert_query = """ INSERT INTO acknowledged_followers (FOLLOWER_ID, SCREEN_NAME, DATE_SENT) VALUES (%s,%s,%s)"""
    record_to_insert = (id, screen_name, "now")
    try:
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
        count = cursor.rowcount
        print(count, "Added to acknowledged:", screen_name)
    except (Exception, Error) as error:
        print("Failed to insert record into acknowledged_followers table", error)
        raise (error)


def update_acknowledged_followers_in_db(followers):
    # Updates acknowledged_followers with all new followers

    connection = db_connect.connect_to_db()
    try:
        for follower in followers:
            add_acknowledged_follower(connection, follower)

    except (Exception, Error) as error:
        print("Failed to update acknowledged followers in db", error)
    finally:
        # closing database connection.
        db_connect.close_db(connection)


# Main

# Authenticate to Twitter
# Keys, tokens and secrets come from env
api = twitter_auth.auth()


# Get most recent 50 followers
recent_followers = api.followers(count=50)

# Use twitterbot_dev db to only send hello to new followers
new_followers = get_new_followers(recent_followers)
# To avoid flooding anyone's notifications, only post a status message to 10 people
new_followers = new_followers[0:4]

# Say hi to new followers
say_hi(new_followers)

# Update acknowledged_followers table
update_acknowledged_followers_in_db(new_followers)

# If we have new followers, make friends
if len(recent_followers) > 0:
    # me and my id
    # Used to get my friends from twitter api
    me = api.get_user(screen_name=MY_SCREEN_NAME)
    my_id = me.id

    # Make new friends with the friendly module
    friends = friendly.make_new_friends(api, my_id, recent_followers)
