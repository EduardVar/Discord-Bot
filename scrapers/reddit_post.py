import praw

async def initPraw(c_id, c_se, u_ag):
    reddit = praw.Reddit(client_id=c_id, client_secret=c_se, user_agent=u_ag)
    print(type(reddit))
