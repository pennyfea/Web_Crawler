from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as soup
from apscheduler.schedulers.background import BlockingScheduler
from urllib2 import urlopen as uReq
import time
import random
import requests
import os
import json
from datetime import datetime

# grabs all the trending quotes for that day


def getTrendingQuotes(browser):
    # wait until trending links appear, not really needed only for example
    all_trendingQuotes = WebDriverWait(browser, 10).until(
        lambda d: d.find_elements_by_css_selector('#trendingQuotes a')
    )
    return [link.get_attribute('href') for link in all_trendingQuotes]


def getStockDetails(url, browser):

    print(url)
    browser.get(url)

    quote_wrapper = browser.find_element_by_css_selector('div.quote-wrapper')
    quote_name = quote_wrapper.find_element_by_class_name(
        "quote-name").find_element_by_tag_name('h2').text
    quote_price = quote_wrapper.find_element_by_class_name("quote-price").text
    quote_volume = quote_wrapper.find_element_by_class_name(
        "quote-volume").text

    print("\n")
    print("Quote Name: " + quote_name)
    print("Quote Price: " + quote_price)
    print("Quote Volume: " + quote_volume)
    print("\n")

    convertToJson(quote_name, quote_price, quote_volume, url)


quotesArr = []
# Convert to a JSON  file


def convertToJson(quote_name, quote_price, quote_volume, url):

    quoteObject = {
        "url": url,
        "Name": quote_name,
        "Price": quote_price,
        "Volume": quote_volume
    }
    quotesArr.append(quoteObject)


def trendingBot(url, browser):
    browser.get(url)
    trending = getTrendingQuotes(browser)
    for trend in trending:
        getStockDetails(trend, browser)
    # requests finished, write json to file

    # REMOVE ANY DUPLICATE url from the list, then write json to file.

    quotesArr_dict = {quote['url']: quote for quote in quotesArr}
    newList = list(quotesArr_dict.values())

    with open('trendingQuoteData.json', 'w') as outfile:
        json.dump(newList, outfile)


def Main():
    scheduler = BlockingScheduler()
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    # applicable to windows os only
    chrome_options.add_argument('--disable-gpu')

    url = 'https://www.tmxmoney.com/en/index.html'
    browser = webdriver.Chrome(
        r"C:\Users\austi\OneDrive\Desktop\chromeDriver\chromedriver_win32\chromedriver.exe", chrome_options=chrome_options)
    # browser = webdriver.Chrome(
    #   r"C:\Users\austi\OneDrive\Desktop\chromeDriver\chromedriver_win32\chromedriver.exe")
    browser.get(url)

    os.system('cls')
    print("[+] Success! Bot Starting!")
    scheduler.add_job(trendingBot, 'interval', hours=1,
                      next_run_time=datetime.now(), args=[url, browser])
    scheduler.start()
    # trendingBot(url, browser)
    browser.quit()


if __name__ == "__main__":
    Main()
