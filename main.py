import requests
import json
from datetime import date
import requests
from config import API_KEY
from textblob import TextBlob


#ensure data quality
#contents are often just aggressive information that the api has been blocked

today = date.today().strftime("%Y-%m-%d")
topic = "Bitcoin"

url = f'https://newsapi.org/v2/everything?q={topic}&from={today}&to=2023-03-13&sortBy=popularity&apiKey={API_KEY}'

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    data = json.dumps(data, indent=4) #indent to make it more readable

    articles = response.json()["articles"]
    headlines = []
    description = []
    contents = []

    for article in articles:
        headlines.append(article["title"])
        description.append(article["description"])
        contents.append(article["content"])
    # Do something with the response data
else:
    print(f'Request failed with status code: {response.status_code}')


def score_check(*args):
    positive, negative, neutral = 0, 0, 0
    for arg in args:
        for content in arg:
            analysis = TextBlob(content)
            polarity = analysis.sentiment.polarity

            if polarity > 0:
                positive +=1
            elif polarity < 0:
                negative +=1
            else:
                neutral += 1

    return positive, negative, neutral

pos, neg, neu = score_check(headlines) #, description, contents can use all contents bc of args 

print(pos, neg, neu)

