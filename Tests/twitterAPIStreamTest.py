import json, urllib, urllib2, requests
from authAPI import generateOAuth

streamFilterURL = "https://stream.twitter.com/1.1/statuses/filter.json"

# generates Twitter statuses from a filter stream
def filterStreamGenerator(*args, **kwargs):
    postReqs = {}
    postReqs['track'] = kwargs.get('track')

    s = requests.Session()
    headers = {"Authorization": generateOAuth("POST", streamFilterURL, postReqs)}
    req = requests.Request("POST", streamFilterURL, headers=headers, data=postReqs).prepare()

    resp = s.send(req, stream=True)

    for status in resp.iter_lines():
        if status:
            yield status


def printStream(*args, **kwargs):
    for line in filterStreamGenerator(*args, **kwargs):
        print line


if __name__ == '__main__':   
    import sys
    trackParams = '{searchTerms}' #gets random tweets
    if len(sys.argv) >= 2:
        trackParams = str(sys.argv[1])
    printStream(track=trackParams)