import time
import praw
import urllib
import re
import os

# Add - Gifv remover; If multiple links in one comment, ignore

def getsize(url):
    file = urllib.urlopen(url)
    size = file.headers.get("content-length")
    file.close()
    return int(size)


print 'Starting...'
r = praw.Reddit('imgur Link Fixer by _Ned')
print 'Logging In...'
r.login('GIFV_FIXER', 'Omgwtfbbq0', disable_warning=True)
print 'Logged In!\n'
# multi_reddits = r.get_subreddit('pics')

UserIgnoreList = ["Snuggle-Ninja", "AutoModerator", "The_Motivated_Man"]

print 'Searching for 1st link...'
while True:
    # Get Already Posted Comments
    if not os.path.isfile("posts_replied_to.txt"):
        posts_replied_to = []
    else:
        with open("posts_replied_to.txt", "r") as f:
            posts_replied_to = f.read()
            posts_replied_to = posts_replied_to.split("\n")
            posts_replied_to = filter(None, posts_replied_to)

    # Check Commments
    all_comments = r.get_comments('all', limit=None)
    # all_comments = r.get_comments('all')
    for comment in all_comments:
        # print "CommentID = ", comment.body
        match = re.search(r'gur.com/.+\.gif', comment.body)
        if match and comment.id not in posts_replied_to and comment.author.name not in UserIgnoreList:  # Found imgur.com/*.gif
            link = 'https://i.im'+match.group(0)
            gifSize = getsize(link)+0.0  # Allows for decimals
            gifvSize = getsize(link+'v')
            percent = (round(((1-(gifvSize/gifSize))*100), 2)-100)*-1
            if not re.search(r'gur.com/.+\.gifv', comment.body) and (gifSize-gifvSize) >= 1500000:  # No 'v' & Diff in file size
                try:
                    comment.reply('[GIFV Link](' + link + 'v)')  # \n\n^^This ^^image\'s ^^size ^^is ^^' + str(percent) + '% ^^of ^^the ^^original ^^gif!')
                    posts_replied_to.append(comment.id)

                    # Save Commment ID
                    with open("posts_replied_to.txt", "w") as f:
                        for post_id in posts_replied_to:
                            f.write(post_id + "\n")

                    print '\n', time.asctime(time.localtime(time.time()))
                    print 'Link:', link + 'v'
                    print '% Diff:', percent
                    print 'Sleeping for 1m...'
                except Exception as e:
                    print '\n>>>Error: ', e

    # Loop Sleep 10s
    time.sleep(10)
    print '-', # 0149
