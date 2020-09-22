#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020-09-21 15:29:38
# @Author  : Racter Liu (racterub) (racterub@gmail.com)
# @Link    : https://racterub.me
# @License : MIT


# Misc
# import time
import re
from urllib.parse import urlparse

# Flask
from flask import Flask, request
import json

# Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# For Demo Purpose
GA_LIST = [
    'UA-138308314-1',
]
STATIC_LIST = [
    'www.benbdsuper.online',
]


# Identified scam sites
def search_static(parsed):
    domain = parsed.netloc

    # MySQL or MongoDB?
    if (domain in STATIC_LIST):
        return True
    return False


# GA
def check_GA(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    prefs = {'profile.default_content_setting_values': {'notifications': 2}}
    options.add_experimental_option('prefs', prefs)
    browser = webdriver.Chrome(options=options, executable_path='./chromedriver')
    # browser.set_window_size(1024, 960)
    browser.get(url)
    m = re.search("UA-[0-9]{9}-[0-9]", browser.page_source)
    browser.quit()
    found = m.group(0)

    # MySQL or MongoDB?
    if (found in GA_LIST):
        return True
    return False


def check_post(url):
    parsed_url = urlparse(url)
    return search_static(parsed_url)
    # return check_GA(url)
    # return check_archive(url)


# Flask app
app = Flask(__name__)
app.config.from_object("config")  # For security, use envvar instead.


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return "scamblock app"
    else:
        url = request.form.get('url')
        if not url:
            return json.dumps({"status": "false"})

        else:
            status = check_post(url)
            return json.dumps({"status": status, "via": "ga"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
