# Developed by Dimitar Dimitrov with special credits to Deyan Yuriev Kolev.
# License scope please see "License Agreement".
import time
import os
import random
from selenium import webdriver
from parsel import Selector
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
import urllib.request
import socks
import socket
import stem.process



def link_scraper(browser):
    df = pd.read_csv('C:/Users/Owner/PycharmProjects/LinkedInVeiwBot/companies.csv')
    url_list = df["list_of_companies"].tolist()
    name_list = df["list_of_company_names"].tolist()
    Selector(text=browser.page_source)
    time.sleep(random.randint(1, 5))
    list = []
    for i, url in enumerate(url_list):
        root_url = "https://www.linkedin.com"
        browser.get(url)
        companyname = name_list[i].replace(" ","_")
        filename = companyname + ".csv"
        dirname = 'C:/Users/Owner/PycharmProjects/LinkedInVeiwBot/' + companyname + '/'
        filepath = dirname + filename
        try:
            os.mkdir(dirname)
        except OSError:
            if os.path.isdir(dirname):
                pass
            else:
                raise
        # It takes a really long break and it is causing congestion,which times out the session.????
        browser.find_element_by_class_name("v-align-middle").click()
        time.sleep(random.randint(1, 5))
        try:
            condition = True
            while condition:
                time.sleep(random.randint(1, 6))
                soup = BeautifulSoup(browser.page_source, 'lxml')
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                for link in soup.select('div[class="search-result__info pt3 pb4 ph0"]'):
                    #image_name = companyname + ".jpg"
                    #imgs = browser.find_elements_by_xpath('//img[@class="lazy-image ivm-view-attr__img--centered  EntityPhoto-circle-4 presence-entity__image EntityPhoto-circle-4 loaded"]/@src').get_attribute('src')
                    #urllib.request.urlretrieve(imgs, image_name, dirname)
                    for a in link.find_all('a', class_='search-result__result-link ember-view'):
                        hrefs_tags = (a.get('href'))
                        carrot_list = root_url + str(hrefs_tags)
                        list.append(carrot_list)
                nextt_button = browser.find_element_by_xpath('//button[@class="artdeco-pagination__button artdeco-pagination__button--next artdeco-button artdeco-button--muted artdeco-button--icon-right artdeco-button--1 artdeco-button--tertiary ember-view"]')
                if nextt_button:
                    time.sleep(random.randint(1, 5))
                    nextt_button.click()
                else:
                    condition = False
        except:
            pass
        # Creating a Date frame with a list of company employees URLS, then writing the data to .CSV file.
        data_file_writer = pd.DataFrame(list, columns=['URLS'])
        data_file_writer.to_csv(filepath, sep=',', index=False, encoding='utf-8')
        print(list)


def main():


    # Get Firefox browser.
    #options = Options()
    #options.headless = True
    browser = webdriver.Firefox()#(options=options)
    print('Activating: Headless Mode!')
    browser.get("https://linkedin.com/uas/login")
    email_element = browser.find_element_by_id("username")
    email_element.send_keys("johndowteam@gmail.com")
    pass_element = browser.find_element_by_id("password")
    pass_element.send_keys("password123#")
    pass_element.submit()
    print('\n')
    print("Login Success!")
    print('\n')
    time.sleep(3)
    print('\n')

    link_scraper(browser)

    #print('activating ViewBot!')

    # replace with 'clear' for Unix type system.
    os.system('cls')
    browser.close()
    #binary.kill()


if __name__ == "__main__":
    main()
