# id l4d2freeweekend
# pw ********************************
import requests
from requests_oauthlib import OAuth1Session
import json
import datetime

consumer_key = "---your consumer key ---"
consumer_secret = "---your consumer secret key ---"
access_token="---your access token ---"
access_token_secret="---your access token secret key ---"

payload = {"text": ""}

now = datetime.datetime.now()
nowDate = now.strftime('%Y-%m-%d')

url = 'https://store.steampowered.com/app/550/Left_4_Dead_2/'
cookies = {"wants_mature_content":"1"}

res = requests.get(url,cookies=cookies)
if (res.text.find('game_area_purchase_game free_weekend') == -1) :
    payload['text'] = nowDate+' No'
else :
    payload['text'] = nowDate+' Yes https://store.steampowered.com/app/550/Left_4_Dead_2/'

# Make the request
oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret,
)

# Making the request
response = oauth.post(
    "https://api.twitter.com/2/tweets",
    json=payload,
)

if response.status_code != 201:
    raise Exception(
        "Request returned an error: {} {}".format(response.status_code, response.text)
    )

print("Response code: {}".format(response.status_code))

# Saving the response as JSON
json_response = response.json()
print(json.dumps(json_response, indent=4, sort_keys=True))
