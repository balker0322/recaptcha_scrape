from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

'''
1. Write a python code for scraping
https://www.ebay-kleinanzeigen.de/s-wohnung-mieten/berlin/c203l3331
https://www.ebay-kleinanzeigen.de/s-wohnung-mieten/berlin/anzeige:angebote/c203l3331+wohnung_mieten.swap_s:nein
2. Implement 2captcha API into script
'''

HOME_URL = 'https://www.ebay-kleinanzeigen.de'

def click_accept_button(driver):
    try:
        element=driver.find_element(By.ID,'gdpr-banner-accept')
        element.click()
        time.sleep(1)
    except:
        pass
    
def get_location(element):
    try:
        result = element.find('div', class_='aditem-main--top--left').text.strip()
        return result
    except:
        return ''

def get_name(element):
    try:
        result = element.find('h2').text.strip()
        return result
    except:
        return ''

def get_description(element):
    try:
        result = element.find('p', class_='aditem-main--middle--description').text.strip()
        return result
    except:
        return ''

def get_price(element):
    try:
        result = element.find('p', class_='aditem-main--middle--price-shipping--price').text.strip()
        return result
    except:
        return ''

def get_url(element):
    try:
        result = element.find('h2').find('a')['href']
        return result
    except:
        return ''


def get_scraped_data(driver):

    soup = BeautifulSoup(driver.page_source, 'lxml')
    item_list = soup.find('ul', class_='itemlist ad-list lazyload it3').find_all('li')
    item_data_list = []
    for item in item_list:
        if len(item['class']) == 1:
            continue
        item_data = {}
        item_data['location']    = get_location(item)
        item_data['name']        = get_name(item)
        item_data['description'] = get_description(item)
        item_data['price']       = get_price(item)
        item_data['url']         = get_url(item)
        item_data_list.append(item_data)

    try:
        url = soup.find('a', class_='pagination-next')['href'].strip()
        print('https://www.ebay-kleinanzeigen.de'+url)
        driver.get(HOME_URL+url)
        time.sleep(2)
        print('success next button')
        return item_data_list + get_scraped_data(driver)
    except:
        print('fail next button')
        return item_data_list

def main():
    # url = 'https://www.ebay-kleinanzeigen.de/s-wohnung-mieten/berlin/c203l3331'
    url = 'https://www.ebay-kleinanzeigen.de/s-wohnung-mieten/berlin/anzeige:angebote/c203l3331+wohnung_mieten.swap_s:nein'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome('./chromedriver.exe', chrome_options=chrome_options)
    driver.get(url)
    time.sleep(3)

    click_accept_button(driver)

    results = get_scraped_data(driver)
    pd.DataFrame(results).to_csv('result.csv')
    
    time.sleep(1)
    driver.quit()

if __name__=='__main__':
    main()