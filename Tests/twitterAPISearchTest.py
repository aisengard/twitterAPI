import json, urllib, urllib2
from authAPI import authRequest

searchURL = "https://api.twitter.com/1.1/search/tweets.json"

# returns JSON of search results
def processSearch(*args, **kwargs):
    bearerToken = authRequest()
    headers = {'Authorization':'Bearer '+bearerToken}

    getReqs = {}
    getReqs['q'] = kwargs.get('q')

    req = urllib2.Request(url=searchURL+'?'+urllib.urlencode(getReqs), headers=headers)
    try:
        response = urllib2.urlopen(req)
    except urllib2.HTTPError as e:
        print e
        return

    jsonResp = json.loads(response.read())
    return jsonResp

def printSearch(*args, **kwargs):
    jsonResp = processSearch(*args, **kwargs)
    statuses = jsonResp.get('statuses')

    for tweet in statuses:
        print u"{0} tweeted at {1}: {2}\n".format(
            tweet.get('user').get('screen_name') 
            ,tweet.get('created_at')
            ,tweet.get('text')
        )

if __name__ == '__main__':   
    import sys
    searchParams = '{searchTerms}' #gets random tweets
    if len(sys.argv) >= 2:
        searchParams = str(sys.argv[1])
    printSearch(q=searchParams, result_type='recent')

