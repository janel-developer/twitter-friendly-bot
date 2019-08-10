import tweepy


def process_page(page):
  # Process page sums the likes on the tweets on this page of results
    sum = 0
    for tweet in page:
        sum += tweet.favorite_count
    return sum


def get_popularity(api, follower):
  # Popularity score is the sum of all likes on the last 100 tweets by the person

    sum = 0
    for page in tweepy.Cursor(api.user_timeline, id=follower.id).pages(5):
        sum += process_page(page)
    return sum


def selective_get_strangers(api, friends, followers):
  # Returns list of popular strangers. Popular strangers have at least 50 likes(total) on their last 100 tweets

    strangers = []
    for follower in followers:
        if get_popularity(api, follower) > 50 and not follower.id in friends:
            strangers.append(follower)
    return strangers


def get_all_strangers(friends, followers):
  # get_all_strangers returns all unfollowed followers

    strangers = []
    for follower in followers:
        if not follower.id in friends:
            strangers.append(follower)
    return strangers


def make_friends(api, strangers):
  # follows list of followers
    friends = []
    for stranger in strangers:
        friend = api.create_friendship(stranger.id)
        if friend:
            friends.append(friend)
            print("New friend: ", friend.screen_name)
    return friends


def make_new_friends(api, my_id, recent_followers):
  # Follows popular new followers

    # Get list of friends ids
    friend_ids = api.friends_ids(user_id=my_id)
    # Get popular strangers
    strangers = selective_get_strangers(api, friend_ids, recent_followers)
    # Friend popular strangers
    return make_friends(api, strangers)
