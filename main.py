from constants import API_KEY,CHAT_ID
from telebot import TeleBot
from datetime import date
import requests
import json

# Setup telegram bot
bot = TeleBot(API_KEY)

# Extract data from medium recommendor
url = "https://medium.com/_/graphql"

payload = json.dumps([
  {
    "operationName": "WebInlineRecommendedFeedQuery",
    "variables": {
      "forceRank": False,
      "paging": {
        "to": "30",
        "limit": 25,
        "source": ""
      }
    },
    "query": ""
  }
])
headers = {
  'authority': 'medium.com',
  'accept': '*/*',
  'accept-language': '',
  'apollographql-client-name': '',
  'apollographql-client-version': '',
  'content-type': '',
  'cookie': '',
  'graphql-operation': '',
  'medium-frontend-app': '',
  'medium-frontend-path': '',
  'medium-frontend-route': '',
  'origin': 'https://medium.com',
  'ot-tracer-sampled': '',
  'ot-tracer-spanid': '',
  'ot-tracer-traceid': '',
  'referer': 'https://medium.com/',
  'sec-ch-ua': '""',
  'sec-ch-ua-mobile': '',
  'sec-ch-ua-platform': '""',
  'sec-fetch-dest': '',
  'sec-fetch-mode': '',
  'sec-fetch-site': '',
  'user-agent': ''
}
date = date.today()
date_show = f"Blogs -  Date : {date}"


response = requests.request("POST", url, headers=headers, data=payload)
data = response.json()[0]['data']['webRecommendedFeed']['items']

# send date
requests.get(f"https://api.telegram.org/bot{API_KEY}/sendMessage?chat_id={CHAT_ID}&text={date_show}")

# list of topics that im interested
list_of_intrests = ['data science','machine learning','deep learning','computer vision','sql','artificial intelligence','deep learning']
for i in data:
    tag_datas = []
    for  j in i['post']['tags']:
        tag_datas.append(j['displayTitle'].lower())
    # if blog was realted to my interested topics send it
    if set(list_of_intrests).intersection(set(tag_datas)) != set():
        tags = " - ".join(tag_datas)
        blog=f"🔴⚪⚪🔴 \n\n  {tags}  \n\n ------------------------------------ \n\n TITLE : \n\n {i['post']['title']} \n\n URL : \n\n {i['post']['mediumUrl']}  \n\n --------------------------------------------------------"
        requests.get(f"https://api.telegram.org/bot{API_KEY}/sendMessage?chat_id={CHAT_ID}&text={blog}")
