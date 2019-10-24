# -*-coding:utf-8 -*-
from info import *
from selenium import webdriver
from time import sleep
from info import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from PIL import Image
import os
import pytesseract
from collections import defaultdict
import requests as req
from io import BytesIO
import sys

def if_training_school(item):
    diploma = item.find_element_by_css_selector('.experience .slash:nth-child(2)').text
    if '本科'.decode('utf-8') in diploma:
        experience = item.find_elements_by_css_selector('.item-info-edu .content .info-item')
        if len(experience) > 1:
            return True
    return False

def say_hello(item):
    chat = item.find_element_by_class_name('chat')
    if '打招呼'.decode('utf-8') in chat.text:
        chat.click()
        sleep(1)
        browser.find_element_by_class_name('btn-confirm').click()
        sleep(1)

def login(browser):
    try:
        browser.get(lagou_login)
        browser.find_element_by_xpath('//input[@type="text"]').send_keys(lagou_id)
        browser.find_element_by_xpath('//input[@type="password"]').send_keys(lagou_password)
        browser.find_element_by_xpath('//input[@type="submit"]').click()
        sleep(20)
    except Exception as e:
        browser.quit()
        raise Exception(e)
    return browser

def search(browser):
    school_list = ["北京大学", "清华大学", "复旦大学", "上海交通大学", "武汉大学", "浙江大学", "中国人民大学", "南京大学", "吉林大学", "中山大学", "北京师范大学", "华中科技大学", "四川大学", "中国科学技术大学", "南开大学", "山东大学", "中南大学", "西安交通大学", "厦门大学", "哈尔滨工业大学", "北京航空航天大学", "同济大学", "天津大学", "华东师范大学", "东南大学", "中国农业大学", "华南理工大学", "湖南大学", "西北工业大学", "大连理工大学", "北京理工大学", "重庆大学", "东北大学", "兰州大学", "中国海洋大学", " 电子科技大学", "西北农林科技大学", " 中央民族大学", " 国防科学技术大学"]
    for school in school_list:
        for i in range(1, 20):
            search_url = "https://easy.lagou.com/talent/search/list.htm?positionName=WEB前端&pageNo=" + str(i) + "&city=北京&education=本科及以上&workYear=不限&industryField=不限&expectSalary=不限&isEliteSchool=1&keyword=" + school
            browser.get(search_url)
            sleep(5)
            items = browser.find_elements_by_class_name('talent-item')
            for item in items:
                try:
                    if if_training_school(item):
                        print 'Is training school, skip'
                    else:
                        say_hello(item)
                except Exception as e:
                    print(e)
            # 专升本不要
            # try:
            #     item.find_element_by_class_name('txt-light')
            #     say_hello(item)
            # except:
            #     try:
            #         item.find_element_by_class_name('isFamousSchool')
            #         say_hello(item)
            #     except:
            #         print 'not wanted'

if __name__ == '__main__':
    try:
        # set browsers
        chromeOptions = webdriver.ChromeOptions()
        # chromeOptions.add_argument('headless')
        # chromeOptions.add_argument("--proxy-server=http://127.0.0.1:8087")
        chromeOptions.add_argument('disable-infobars')
        browser = webdriver.Chrome(chrome_options=chromeOptions)
        browser.maximize_window()
        login(browser)
        search(browser)
    except Exception as e:
        print(e)