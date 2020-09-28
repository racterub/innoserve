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


# Misc
# import time
import re
from urllib.parse import urlparse
import json
from bs4 import BeautifulSoup as BS
import time
import requests

# Flask
from flask import Flask, request


# Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


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
    prefs = {'profile.default_content_setting_values': {'notifications': 2}}
    options.add_experimental_option('prefs', prefs)
    browser = webdriver.Chrome(options=options, executable_path='./chromedriver')
    browser.get(url)
    source = browser.page_source
    browser.quit()
    soup = BS(source, "lxml")

    dateDivBlock = soup.find("div", class_="_3qn7 _61-0 _2fyi _3qnf _2pi9 _3-95")
    date = dateDivBlock.find("span").string
    print(date)


def checkPost(url):
    if (checkStatic(urlparse(url))):  # Make it faster
        return True
    if (checkAnalytics(url)):
        return True
    return False


# Flask app
app = Flask(__name__)
app.config.from_object("config")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return "scamblock app"
    else:
        # payload = request.form.get('payload')
        # try:
        #     exPayload = json.loads(payload)
        # except JSONDecodeError:
        #     return json.dumps({"status": "false"})
        # fbUrl = exPayload['fbUrl']
        # storeUrl = exPayload['storeUrl']

        url = request.form.get('url')
        if not url:
            return json.dumps({"status": "false"})
        else:
            status = checkPost(url)
            return json.dumps({"status": status})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
