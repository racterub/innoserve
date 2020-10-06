#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020-09-21 15:29:38
# @Author  : Racter Liu (racterub) (racterub@gmail.com)
# @Link    : https://racterub.me
# @License : MIT


'''
[-] check domain list
[-] check analytics
[] check fb profile (username)
[] check fb profile (creation date)
'''

'''
API

Endpoint: /
Method: POST
Data:
    - payload (urlencoded-json format)
        - storeUrl # External Link
        - fbUrl # Facebook Profile
'''

# Misc
# import time
import re
from urllib.parse import urlparse
import json
from bs4 import BeautifulSoup as BS


# Flask
from flask import Flask, request, Response
from flask_cors import CORS


# Selenium
from selenium import webdriver


# For Demo Purpose
GA_LIST = [
    'UA-138308314-1',
]
FB_LIST = [
    '799174287180703',
]
STATIC_LIST = [
    'www.benbdsuper.online',
]
FBUSER_LIST = [
]


# MonthMap
MONTHMAP = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12
}


# Identified scam sites
def checkStatic(parsed):
    domain = parsed.netloc

    # MySQL or MongoDB?
    if (domain in STATIC_LIST):
        return True
    return False


# Google Analytics & Facebook Pixel
def checkAnalytics(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    prefs = {'profile.default_content_setting_values': {'notifications': 2}}
    options.add_experimental_option('prefs', prefs)
    browser = webdriver.Chrome(options=options, executable_path='./chromedriver')
    browser.get(url)
    source = browser.page_source
    browser.quit()
    GA = re.search("UA-[0-9]{9}-[0-9]", source)
    soup = BS(source, "lxml")
    FB = soup.find("meta", property="fb:app_id")

    # MySQL or MongoDB?
    if (GA):
        if (GA.group() in GA_LIST):
            return True
    if (FB):
        if (FB['content'] in FB_LIST):
            return True
    return False


def checkFBUser(url):
    parsedUrl = urlparse(url)
    userId = parsedUrl.path[1:-1]
    if (userId in FBUSER_LIST):
        return True
    return False


# String offset depends on facebook's language
def checkFBCreate(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    prefs = {'profile.default_content_setting_values': {'notifications': 2}}
    options.add_experimental_option('prefs', prefs)
    browser = webdriver.Chrome(options=options, executable_path='./chromedriver')
    #browser.set_window_size(1024, 768)
    browser.get(url)
    source = browser.page_source
    # browser.quit()
    soup = BS(source, "lxml")

    # Facebook Sucks :(
    try:
        '''
        Old Facebook UI
        '''
        dateDivBlock = soup.find("div", class_="_3qn7 _61-0 _2fyi _3qnf _2pi9 _3-95")
        date = dateDivBlock.find("span").string
    except AttributeError:
        '''
        New Facebook UI
        '''
        dateDivBlock = soup.find("div", class_="d2edcug0 hpfvmrgz qv66sw1b c1et5uql oi732d6d ik7dh3pa fgxwclzu a8c37x1j keod5gw0 nxhoafnm aigsh9s9 d9wwppkn fe6kdd0r mau55g9w c8b282yb iv3no6db jq4qci2q a3bd9o3v lrazzd5p oo9gr5id")
        date = dateDivBlock.find("span").string

    # Languages
    if date[0] == "粉":
        date = date[11:].split('年')
        year = date[0]
        date = date[1].split('月')
        month = date[0]
        date = date[1].split('日')
        day = date[0]
    else:
        date = date[15:].split(' ')
        month = date[0]
        date = ''.join(date[1:]).split(',')
        day, year = date
        month = MONTHMAP[month]

    return False


def checkPost(fburl, url):


    if (not url):
        if (checkFBUser(fburl)):
            return True
        #if (checkFBCreate(fburl)):


            return True
    else:
        if (checkStatic(urlparse(url)) or checkFBUser(fburl)):  # Make it faster
            return True

        #if (checkAnalytics(url) or checkFBCreate(fburl)):
            #return True

    return False


# Flask app
app = Flask(__name__)
app.config.from_object("config")

CORS(app)
"""
def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return resp
app.after_request(after_request)
"""


@app.route("/", methods=["GET", "POST"])
def index():
    print('===')
    if request.method == "GET":
        return "scamblock app"
    else:

        payload = request.get_json()
        print(payload)
        if ('fbUrl' in payload):
            fbUrl = payload['fbUrl']
        else:
            return json.dumps({"status": "false"})
        if ('storeUrl' in payload):
            storeUrl = payload['storeUrl']

        else:
            storeUrl = None
        status = checkPost(fbUrl, storeUrl)
        resp = Response(json.dumps({"status": status}), mimetype='application/json')
        return resp


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=6000)
