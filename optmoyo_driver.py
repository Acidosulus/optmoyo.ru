from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import os
from my_library import *
import colorama
from colorama import Fore, Back, Style
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import configparser

class WD:
    def init(self):
        lc_link = r'https://optmoyo.ru/zhen/catalog/jenskoe-belye-aksessuary/eroticheskoye-belyo-jenskoe-belye'
        config = configparser.ConfigParser()
        config.read("options.ini")
        print(config["Login"]["Login"], config["Login"]["Password"])
        print(Fore.RED + 'Chrome Web Driver '+Fore.YELLOW +lc_link+Fore.RESET)
        if True:
            chrome_options = webdriver.ChromeOptions()
            chrome_prefs = {}
            chrome_options.experimental_options["prefs"] = chrome_prefs
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument("--disable-notifications")
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.maximize_window()
        self.Get_HTML(lc_link)
        time.sleep(1)
        link = self.driver.find_element(by=By.PARTIAL_LINK_TEXT, value=r'Вход/Регистрация')
        link.click()
        time.sleep(1)
        self.driver.find_element(by=By.NAME, value = "Login").send_keys(config["Login"]["Login"])
        self.driver.find_element(by=By.NAME, value = "Password").send_keys(config["Login"]["Password"])
        self.driver.find_element(by=By.XPATH, value = "//*[contains(@class,'afarr')]").click()
        self.Get_HTML(lc_link)
    def __init__(self):
        self.init()


    def __del__(self):
        try:
        #    self.driver.quit()
            pass
        except: pass


    def Get_HTML(self, curl):
        self.driver.get(curl)
        return self.driver.page_source


    def Get_List_Of_Links_On_Goods_From_Catalog(self, pc_link):
        print(Fore.RED + 'Список товаров каталога: ' + Fore.YELLOW + pc_link + Fore.RESET)
        ll_catalog_items = []
        ll_list_of_pages = self.Get_List_Pages_Of_Catalog(pc_link)
        for link_on_page  in ll_list_of_pages:
            ll_goods_from_page = self.Get_List_of_Links_On_Good_From_Page(link_on_page)
            for link in ll_goods_from_page:
                if link not in ll_catalog_items:
                    ll_catalog_items.append(link)
        print(Fore.LIGHTRED_EX,ll_catalog_items,Fore.RESET)
        return ll_catalog_items


    def Get_List_of_Links_On_Good_From_Page(self, pc_link):
        print(Fore.RED + 'Список товаров страницы: ' + Fore.YELLOW + pc_link + Fore.RESET)
        ll_result = []
        self.driver.get(pc_link)
        lo_product_links = self.driver.find_elements(by=By.XPATH, value="//a[@class='link']")
        for lo_link in lo_product_links:
            lc_link = lo_link.get_attribute('href')
            if len(lc_link)>10 and lc_link not in ll_result:
                ll_result.append(lc_link)
        print(ll_result)
        return ll_result


    def Get_List_Pages_Of_Catalog(self, c_link_on_first_catalog):
        print(Fore.RED + 'Страницы каталога: ' + Fore.YELLOW + c_link_on_first_catalog + Fore.RESET)
        list = []
        self.driver.get(c_link_on_first_catalog)
        try: lo_navigation = self.driver.find_element(by=By.XPATH, value = "//*[contains(@class,'page_navi')]")
        except: 
            list.append(c_link_on_first_catalog)
            return list
        #str_to_file('nav.html', lo_navigation.get_attribute('innerHTML'))
        try:
            li = lo_navigation.find_element(by=By.TAG_NAME, value='ul')
            links = li.find_elements(by=By.TAG_NAME, value='a')
        except:
            list.append(c_link_on_first_catalog)
            return list
        listnumbers = []
        for link in links:
            listnumbers.append(int(link.get_attribute('text')))
        print(listnumbers, max(listnumbers))
        
        for i in range(1,max(listnumbers)):
            lc_link = c_link_on_first_catalog + ('/' if c_link_on_first_catalog[-1]!='/' else '') + str(i)
            if lc_link not in list:
                list.append(lc_link)
        print(list)
        return list


    def Write_To_File(self, cfilename):
        file = open(cfilename, "w", encoding='utf-8')
        file.write(self.driver.page_source)
        file.close()


def Login():
    try:
        wdo = WD()
        print(1)
    except:
        try:
            wdo = WD()
            print(2)
        except:
            try:
                wdo = WD()
                print(3)
            except:
                try:
                    wdo = WD()
                    print(4)
                except:
                    pass
    return wdo


colorama.init()

#wd = WD()
#print(wd.Get_List_Pages_Of_Catalog(r"""https://moyo.moda/zhen/catalog/kupalniki"""))
#print(wd.Get_List_Of_Links_On_Goods_From_Catalog(r"https://moyo.moda/zhen/catalog/kupalniki"))
#print(wd.Get_List_of_Links_On_Good_From_Page(r"https://moyo.moda/zhen/catalog/kupalniki"))



#    if wd.driver.page_source.count('user773')>0:
#        print('Авторизация прошла успешно')
#        return wd
#    else:
#        print('Авторизация не прошла')
#        try:
#            pass
#            wd.driver.quit()
#        except:
#            print('Рекурсивный перезапуск')
#            return LoginOB()