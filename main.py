import re
import time
from contextlib import suppress
import requests as requests
from bs4 import BeautifulSoup
from lxml import html
from selenium.webdriver.chrome import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.common.by import By
from driver import get_options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as Ec
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
class Lazada:
    counter=2
    cs = service.Service(executable_path="driver/chromedriver.exe")
    options = get_options("testing1")
    driver = webdriver.ChromiumDriver(service=cs, browser_name="chrome", vendor_prefix="GC", options=options, )
    actions = ActionChains(driver)
    product_catagorey = input('Please enter your category:')
    product_catagoery_sub = input('Please enter your category_sub_type:')
    link=('https://www.walmart.com/search?q=' + product_catagorey + '&facet=brand%3A' + product_catagoery_sub)
    driver.get(link)
    def page_links(self):
        last_Hieght = self.driver.execute_script('return document.body.scrollHeight')
        while True:
            self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            time.sleep(5)
            new_Hieght = self.driver.execute_script('return document.body.scrollHeight')
            if new_Hieght == last_Hieght:
                break
            last_Hieght = new_Hieght
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        links = soup.find_all('div', {'class': 'sans-serif mid-gray relative flex flex-column w-100 hide-child-opacity'})
        self.lst = []
        for i in links:
            ok = i.findNext('a').get('href')
            self.lst.append(ok)
        self.feature_scraping()
    def feature_scraping(self):
        actions = ActionChains(self.driver)
        for j in self.lst:
            try:
                self.driver.get(j)
                actions.scroll_to_element(self.driver.find_element(By.CLASS_NAME, 'expand-collapse-section')).perform()
                time.sleep(5)
                details = BeautifulSoup(self.driver.page_source, 'lxml')
                key_values_1=details.find_all('div',{'class':'nt1'})[0]
                product_name = details.find('h1', {'class': 'b lh-copy dark-gray mt1 mb2 f3'}).text
                product_price = details.find('span', {
                    'class': 'inline-flex flex-column'}).text
                print('Product_Name:', product_name)
                print('Product_Price:', product_price)
                dict={}
                for k in key_values_1:
                    key = k.find('h3',{'class':'flex items-center mv0 lh-copy f5 pb1 dark-gray'}).text
                    values = k.find('p',{'class':'mv0 lh-copy f6 mid-gray'}).text
                    dic={key:values}
                    dict.update(dic)
                print(dict)
            except:
                pass
        self.next_page()
    def next_page(self):
        self.driver.get(self.link + '&page=' + str(self.counter)+'&affinityOverride=default')
        self.counter += 1
        self.page_links()
call=Lazada()
call.page_links()
