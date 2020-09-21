#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020-09-21 13:39:55
# @Author  : Racter Liu (racterub) (racterub@gmail.com)
# @Link    : https://racterub.me
# @License : MIT



from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


if __name__ == "__main__":
    url = "https://www.facebook.com/"

    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    prefs = {'profile.default_content_setting_values':{'notifications': 2}}
    options.add_experimental_option('prefs', prefs)
    browser = webdriver.Chrome(options=options, executable_path='./chromedriver')
    browser.set_window_size(1024, 960)
    browser.get(url)
    browser.implicitly_wait(30)