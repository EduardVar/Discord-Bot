import praw

reddit = praw.reddit.Reddit

# Need to call this!
def initPraw(c_id, c_se, u_ag):
    global reddit
    reddit = praw.Reddit(client_id=c_id, client_secret=c_se, user_agent=u_ag)

def getImagePost(sub):
    subreddit = reddit.subreddit(sub)

    while True:
        submission = subreddit.random()
        flairText = submission.link_flair_text

        if ((flairText == None and flairText is not type(None))
            or flairText.lower() != "announcement"):
            return submission.url
