import json, urllib, urllib2

consumerKey = "A09ADIWm5ObRfrzwlJTQ"
consumerSecret = "JlFOVERuOvmX6tHOl9SKyVjwAiCKz0Kn7hXN4bnSnrk"

reqBearerTokenURL = "https://api.twitter.com/oauth2/token"
searchURL = "https://api.twitter.com/1.1/search/tweets.json"

# returns access_token
def authRequest():
    import base64

    bearerToken = consumerKey+":"+consumerSecret
    b64BearerToken = base64.b64encode(bearerToken)

    data = {}
    headers = {}
    headers['Authorization'] = 'Basic '+b64BearerToken
    headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF8'

    data['grant_type'] = 'client_credentials'
    data = urllib.urlencode(data)

    req = urllib2.Request(reqBearerTokenURL, data, headers)
    try: 
        response = urllib2.urlopen(req)
    except urllib2.HTTPError as e:
        print e
        return

    jsonResp = json.loads(response.read())
    return jsonResp.get('access_token')

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

