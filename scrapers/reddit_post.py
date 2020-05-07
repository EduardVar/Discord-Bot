import praw

reddit = praw.reddit.Reddit

# Need to call this!
def initPraw(c_id, c_se, u_ag):
    reddit = praw.Reddit(client_id=c_id, client_secret=c_se, user_agent=u_ag)
