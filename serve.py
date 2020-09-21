#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020-09-21 15:29:38
# @Author  : Racter Liu (racterub) (racterub@gmail.com)
# @Link    : https://racterub.me
# @License : MIT


# Misc
import time

# Flask
from flask import Flask, request
import json

# Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Crawler
def check_post(url):

    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    prefs = {'profile.default_content_setting_values':{'notifications': 2}}
    options.add_experimental_option('prefs', prefs)
    browser = webdriver.Chrome(options=options, executable_path='./chromedriver')
    browser.set_window_size(1024, 960)
    browser.get(url)
    time.sleep(10)
    browser.quit()

# Flask app
app = Flask(__name__)
app.config['DEBUG'] = True


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return "scamblock app"
    else:
        url = request.values.get('url')
        if not url:
            return json.dumps({"status": "false"})

        else:
            check_post(url)
            return "test"
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
