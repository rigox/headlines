from flask import Flask
import feedparser
from  flask import  render_template
from flask import  request
import json

import requests as re
from sphinx.addnodes import toctree

app =  Flask(__name__)

DEFAULTS = {
    'publication':'bbc',
    'city':'Miami,USA',
    'currency_from': 'USD',
    'currency_to': 'GBP'
}


CURRENCY_URL = "https://openexchangerates.org//api/latest.json?app_id=070cf08a56b14e45bf1065fe8599eb18"

RSS_FEED  ={
     "bbc": "http://feeds.bbci.co.uk/news/rss.xml",
     'cnn':   'http://rss.cnn.com/rss/edition.rss',
     'fox':   'http://feeds.foxnews.com/foxnews/latest',
     'iol':    'http://www.iol.co.za/cmlink/1.640'
}


def get_rate(frm,to):
    all_currency =  re.get(CURRENCY_URL)
    parsed = all_currency.json()
    rates =  parsed.get('rates')
    frm_rate =  rates.get(frm.upper())
    to_rate  = rates.get(to.upper())

    return  (to_rate/frm_rate, rates.keys())

def get_weather(query):
    api_url = "http://api.openweathermap.org/data/2.5/weather?&units=imperial&appid=6e2070ce120ca894727ce65ce75b6c46"
    payload  = {'q':query}
    r =  re.get(api_url, params= payload)
    a = r.json()
    weather= {
        'description': a['weather'][0]["description"],
         'temp': a['main']['temp'],
         'name':a['name'],
         'country':a['sys']['country']

    }
    return weather

def get_news(query):
    if not query or query.lower() not in RSS_FEED:
        publication  = DEFAULTS['publication']
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEED[publication])
    return  feed['entries']



@app.route("/")
def home():
 publication = request.args.get("publication")
 if not publication:
     publication = DEFAULTS['publication']
 articles = get_news(publication)
 #### get weather data
 city =  request.args.get('city')
 if not city:
     city = DEFAULTS['city']
 weather = get_weather(city)
 ## get  currency data a
 currency_from = request.args.get("currency_from")
 if not currency_from:
     currency_from = DEFAULTS['currency_from']
 currency_to =  request.args.get("currency_to")
 if not currency_to:
     currency_to = DEFAULTS['currency_to']
 rate , currencies = get_rate(currency_from,currency_to)
 print(currencies)

 return  render_template("home.html" , articles = articles,
                         weather = weather,
                         currency_from = currency_from , currency_to = currency_to,
                         rate = rate,
                         currencies  = sorted(currencies)
                         )






if __name__  == "__main__":
    app.run(port= 5000  , debug= True)




