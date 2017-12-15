import requests
import json
import os

from bs4 import BeautifulSoup

from collections import Counter

from clarifai.rest import ClarifaiApp

app = ClarifaiApp(api_key='c8e59e90bb1f473e851f688f49b3e4df')

model = app.models.get("general-v1.3")

# predict with the model
temp = model.predict_by_url(url='https://samples.clarifai.com/metro-north.jpg')

data = temp['outputs'][0]["data"]["concepts"]

all_words = []
tweet_list = ''

common_words = json.load(open('commonWords.json'))

def fetchTweets(tweets):
    global all_words, tweet_list

    tmp = [p['data-tweet-id'] for p in tweets]

    nextPage = u'https://twitter.com/i/profiles/show/EmmanuelMacron/timeline/tweets?include_available_features=1&include_entities=1&lang=fr&max_position='+tmp[-1]+'&oldest_unread_id=0&reset_error_state=false'

    r = requests.get(nextPage)

    data = json.loads(str(r.text))

    soup = BeautifulSoup(data["items_html"], 'html.parser')
    # last_id = data["min_position"]

    tweet_list = [p for p in soup.find_all('div', class_="tweet")]

    res = [p.text for p in soup.find_all('p', class_="tweet-text")]

    for tweet in res:
        temp = tweet.split()
        for t in temp :
            if t.lower() not in common_words:
                all_words.append(t.lower())


url = u'https://twitter.com/EmmanuelMacron'

r = requests.get(url)

soup = BeautifulSoup(r.text, 'html.parser')

tweets = [p for p in soup.find_all('div', class_="tweet")]

fetchTweets(tweets)

for _ in range(1):
    fetchTweets(tweet_list)


counts = Counter(all_words).most_common(100)
for c in counts :
    print(c[0], c[1])
