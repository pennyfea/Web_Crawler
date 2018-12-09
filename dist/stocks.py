from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup as soup
from urllib2 import urlopen as uReq
import time
import random
import requests



# Old implementation

# def getTrendingQuotes(source_code):
#     # grabs all the trending quotes for that day
#     links = []
#     page_soup = soup(source_code, "lxml")
#     trendingQuotes = page_soup.findAll("div", {"id": "trendingQuotes"})
#     all_trendingQuotes = trendingQuotes[0].findAll('a')
#     for link in all_trendingQuotes:
#         url = link.get('href')
#         #name = link.text
#         # print(name)
#         links.append(url)
#     return links


# def getStockDetails(url, browser):
#     print(url)
#     source_code = browser.execute_script(
#         "return document.documentElement.outerHTML")
#     page_soup = soup(source_code, "html.parser")
#     quote_wrapper = page_soup.findAll("div", {"class": "quote-wrapper"})

#     for quote in quote_wrapper:

#         qn = quote.find("div", {"class": "quote-name"})
#         quote_name = qn.h2.text

#         qp = quote.find("div", {"class": "quote-price"})
#         quote_price = qp.span.text

#         qv = quote.find("div", {"class": "quote-volume"})
#         quote_volume = qv.span.br.string
#         print("Quote Name: " + quote_name)
#         print("Quote Price: " + quote_price)
#         print("Quote Volume: " + quote_volume)


# def trendingBot(browser):
#     while True:
#         source_code = browser.execute_script(
#             "return document.documentElement.outerHTML")
#         trending = getTrendingQuotes(source_code)
#         for trend in trending:
#             browser.get(trend)
#             getStockDetails(trend, browser)
#         break


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



def trendingBot(url, browser):
    browser.get(url)
    trending = getTrendingQuotes(browser)
    for trend in trending:
        getStockDetails(trend, browser)


def Main():

    url = 'https://www.tmxmoney.com/en/index.html'
    browser = webdriver.Chrome(
        r"C:\Users\austi\OneDrive\Desktop\chromeDriver\chromedriver_win32\chromedriver.exe")
    browser.get(url)

    print("[+] Success! Bot Starting!")
    trendingBot(url, browser)
    # trendingBot(browser)
    browser.quit()


if __name__ == "__main__":
    Main()
