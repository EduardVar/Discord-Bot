import praw
import random

reddit = praw.reddit.Reddit

# Need to call this!
def initPraw(c_id, c_se, u_ag):
    global reddit
    reddit = praw.Reddit(client_id=c_id, client_secret=c_se, user_agent=u_ag)

def getImagePost(sub):
    subreddit = reddit.subreddit(sub)

    while True:
        submission = subreddit.random()
        
        try:   
            flairText = submission.link_flair_text

            if flairText is None:
                flairText = ""
     
            if flairText.lower() != "announcement":
                return submission.url
        except Exception as e:
            print("Failed post", submission)
            
            try:
                print("Trying getPicLink")
                return getPicLink(sub)
            except:
                print("Didn't work for either")
            

def getPicLink(sub):
    subreddit = reddit.subreddit(sub)
    listingGen = subreddit.hot()

    whichPost = random.randint(1, 101)
    counter = 1

    for post in listingGen:
        if counter == whichPost:
            return post.url
        else:
            counter += 1
