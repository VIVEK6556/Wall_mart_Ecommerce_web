import undetected_chromedriver as uc
import warnings
warnings.filterwarnings('ignore')
import time
from bs4 import BeautifulSoup
from selenium.webdriver.chrome import service
from driver import get_options
import pandas as pd
import re
class Wallmart:
    def Wallmart_Login(self):
        self.counter=2
        self.product_catagorey = input("Please enter the Product_Category:")
        self.product_brand = input("Please enter the Product_Brand(Optional):")
        self.file=input('Please enter the Floder name(For Datasaving):')
        options = get_options("testing1")
        cs = service.Service(executable_path="driver/chromedriver.exe")
        # self.driver = webdriver.ChromiumDriver(service=cs, browser_name="chrome", vendor_prefix="GC", options=options)
        self.link = (
                    'https://www.walmart.com/search?q=' + self.product_catagorey + '&facet=brand%3A' + self.product_brand)
        self.driver=uc.Chrome(options=options,)
        self.driver.get(self.link)
        doup = BeautifulSoup(self.driver.page_source, 'lxml')
        if doup.find('h1', {'class': 'heading heading-d sign-in-widget'}):
            captcha = input('Please check wheather captch is cleared OR not:')
        else:
            pass
        self.df = pd.DataFrame({'ITEM_ Category': [''], 'ITEM_Brand': [''], 'ITEM_NAME': [''], 'ITEM_UPC': [''],'ITEM_Original_Price': [''], 'ITEM_Actual_Price': [''], 'PRODUCT_LINK': ['']})
        self.Link_Scraping()
    def Link_Scraping(self):
        time.sleep(10)
        self.pst = []
        last_Hieght = self.driver.execute_script('return document.body.scrollHeight')
        while True:
            self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            time.sleep(2)
            new_Hieght = self.driver.execute_script('return document.body.scrollHeight')
            if new_Hieght == last_Hieght:
                break
            last_Hieght = new_Hieght
        time.sleep(5)
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        links = soup.find_all('a', {'class': 'absolute w-100 h-100 z-1 hide-sibling-opacity'})
        for i in links:
            try:
                link = i.get('href')
            except:
                continue
            self.pst.append(link)
        self.Details_Scraping()
    def Details_Scraping(self):
        global Product_Name,item_brand
        count = 1
        for i in self.pst:
            try:
                self.driver.get(i)
            except:
                try:
                    self.driver.get('https://www.walmart.com'+i)
                    i='https://www.walmart.com'+i
                except:
                    continue
            doup = BeautifulSoup(self.driver.page_source, 'lxml')
            if doup.find('h1', {'class': 'heading heading-d sign-in-widget'}):
                try:
                    self.driver.get('https://api.scrapingdog.com/scrape?dynamic=false&url='+i+'&api_key=635752a08fc4e26b38226434')
                except:
                    try:
                        self.driver.get('https://www.walmart.com' + i+'&api_key=635752a08fc4e26b38226434')
                        i = 'https://www.walmart.com' + i
                    except:
                        continue
                # captcha = input('Please check wheather captch is cleared OR not:')
            else:
                pass
            time.sleep(5)
            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            try:
                Upc=soup.find('script',{'id':'__NEXT_DATA__'}).text
                Code=re.search(r'upc',Upc)
                end=Code.end()
                Upc=Upc[end+3:end+15]
            except:
                Upc='NA'
            if not Upc.isdigit():
                Upc='NULL'
            else:
                pass
            Product_Name='NA'
            try:
                try:
                    Product_Name=soup.find('h1').text
                except:
                    pass
                try:
                    Product_Name=soup.find('h1',{'class':'b lh-copy dark-gray mt1 mb2 f3'}).text
                except:
                    pass
                try:
                    Product_Name=soup.find('h1',{'class':'b lh-copy dark-gray mt1 mb2 f6 f3-m'}).text
                except:
                    pass
                try:
                    Product_Name=soup.find('h1',{'class':'b lh-copy dark-gray mt1 mb2 f6 f3-m mh0-l mh3'}).text
                except:
                    pass
            except:
                pass
            if Product_Name=='NA' or Product_Name=='Sorry...':
                continue
            else:
                pass
            try:
                item_brand=soup.find('a',{'class':'bg-transparent bn lh-solid pa0 sans-serif tc underline inline-button mid-gray pointer f6'}).text
            except:
                item_brand='NA'
            try:
                Product_Price=soup.find('span',{'class':'inline-flex flex-column'}).text
            except:
                Product_Price='NA'
            try:
                Actual_Price=soup.find('span',{'class':'mr2 f6 gray strike'}).text
            except:
                Actual_Price='NA'
            count+=1
            self.df = self.df._append({'ITEM_ Category':self.product_catagorey,'ITEM_Brand': item_brand,'ITEM_NAME':Product_Name,'ITEM_UPC':Upc, 'ITEM_Original_Price': Product_Price, 'ITEM_Actual_Price': Actual_Price, 'PRODUCT_LINK': i}, ignore_index=True)
            self.df.to_csv(self.file+'\\'+self.product_brand+self.product_catagorey+'.csv')
        self.next_Page()
    def next_Page(self):
        self.link = ('https://www.walmart.com/search?q=' + self.product_catagorey + '&facet=brand%3A' + self.product_brand)
        self.driver.get(self.link + '&page=' + str(self.counter) + '&affinityOverride=default')
        doup = BeautifulSoup(self.driver.page_source, 'lxml')
        if doup.find('h1', {'class': 'heading heading-d sign-in-widget'}):
            captcha = input('Please check wheather captch is cleared OR not:')
        else:
            pass
        self.counter += 1
        self.Link_Scraping()

object=Wallmart()
object.Wallmart_Login()

