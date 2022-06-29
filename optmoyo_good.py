import base64
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import os
from my_library import *
from optmoyo_driver import *
import colorama
from colorama import Fore, Back, Style
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib import request
from urllib.parse import quote
import wget
import uuid
import configparser
from PIL import Image
import requests
from pathlib import Path
import threading

def poiskpers(url):
    geourl = '{0}'.format(quote(url))
    return geourl


class optmoyo_good:
    def __init__(self, ol:WD, lc_link, pc_price:str):
        config = configparser.ConfigParser()
        config.read("Options.ini")
        lc_link = lc_link.replace(r'amp;', '')
        self.pictures = []
        self.sizes = []
        self.prices = []
        self.color = ''
        self.article = ''
        self.name = ''
        self.description= ''
        self.price = ''
        self.brand = ''
        print(Fore.LIGHTGREEN_EX, 'Товар: ', Fore.LIGHTBLUE_EX, lc_link, Fore.RESET)
        self.source = ol.Get_HTML(lc_link)
        
        try: self.name = ol.driver.find_element(By.XPATH, value = "//*[contains(@class,'card_new__info__params')]").text.replace('\r',' ').replace('\n',' ').strip() 
        except: pass

        try: self.description =    ol.driver.find_element(By.XPATH, value = "//*[contains(@class,'card_new__info__dop_info')]").text.replace('\r',' ').replace('\n',r'/').strip() + \
                                   ' ' + \
                                    ol.driver.find_element(By.XPATH, value = "//*[contains(@class,'card_new__info__desc')]").text.replace('\r',' ').replace('\n',' ').strip()
        except: pass

        try: self.article = ol.driver.find_element(By.TAG_NAME, value = 'h1').text 
        except: pass


        try: 
            self.price = sx(ol.driver.page_source,'<span class="new"><ins>','<')
        except: pass
        if len(self.price)==0:
            try: self.price = ol.driver.find_element(By.XPATH, value = "//*[contains(@class,'card_new__top__price')]").text.replace(',','.').replace(' ','')
            except: pass
        self.price = self.price.replace(',','.').replace(' ','')

        lc_pics = ol.driver.find_element(by=By.CLASS_NAME, value='card_new__gallery').get_attribute('innerHTML')
        #str_to_file('pics.html',lc_pics)
        ll_on_site = []
        links_new_last = []
        for i in range(1,lc_pics.count('data-src="')+1):
            lc_picture_link = sx(lc_pics, 'data-src="', '"', i)
            if lc_picture_link not in ll_on_site:
                ll_on_site.append(lc_picture_link)
                if lc_picture_link not in self.pictures:
                    #lc_new_file_name = str(uuid.uuid4())
                    #wget.download(lc_picture_link, config["Paths"]["webppath"] + + lc_new_file_name + r'.webp', bar=None)
                    #im = Image.open(lc_picture_link).convert("RGB")
                    #im.save(config["Paths"]["webppath"] + Path(lc_price).stem + '\\' + lc_new_file_name + r'.jpg',"jpeg")
                    #os.remove(config["Paths"]["webppath"] + lc_new_file_name + r'.webp')
                    lc_new_file_name = base64.b64encode(bytes(lc_picture_link, 'utf-8')).decode()
                    self.pictures.append(r'http://memer.site/static/optmoyo.ru/' + lc_new_file_name +'.jpg')
                    links_new_last.append([lc_new_file_name, lc_picture_link])
                    #url = 'http://memer.site/hoster/moyo.moda/'
                    #fp = open(config["Paths"]["webppath"] + lc_new_file_name + r'.jpg', 'rb')
                    #files = {'myFile': fp}
                    #resp = requests.post(url, files=files)
                    #fp.close()
                    #print(Fore.BLUE,resp,Fore.RESET)
        thread = threading.Thread(target=Download_and_save_pictures, args=(links_new_last,pc_price,))
        thread.start()

        sizes = ol.driver.find_elements(by=By.CLASS_NAME, value='card_new__top__select_size__size_count_block')
        for size in sizes:
            if size.text not in self.sizes:
                self.sizes.append(size.text)


def Download_and_save_pictures(ll, pc_price):
    config = configparser.ConfigParser()
    config.read("Options.ini")
    if not os.path.isdir(config["Paths"]["webppath"] + Path(pc_price).stem):
        os.mkdir(config["Paths"]["webppath"] + Path(pc_price).stem)
    for elem in ll:
        ll_file_name = elem[0]
        ll_link_on_source = elem[1]
        wget.download(ll_link_on_source, config["Paths"]["webppath"] + Path(pc_price).stem + '\\' + ll_file_name + r'.webp', bar=None)
        im = Image.open(config["Paths"]["webppath"] + Path(pc_price).stem + '\\' + ll_file_name + r'.webp').convert("RGB")
        im.save(config["Paths"]["webppath"] + Path(pc_price).stem + '\\' + ll_file_name + r'.jpg',"jpeg")
        os.remove(config["Paths"]["webppath"] + Path(pc_price).stem + '\\' + ll_file_name + r'.webp')