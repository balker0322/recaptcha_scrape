from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import time
import key


def bypass_recaptcha(driver, page_url, key):
    method = "userrecaptcha"
    site_key_element = driver.find_element(By.CLASS_NAME, 'g-recaptcha')
    site_key = site_key_element.get_attribute("data-sitekey")

    url = "http://2captcha.com/in.php?key={}&method={}&googlekey={}&pageurl={}".format(key,method,site_key,page_url)
    response = requests.get(url)


    if response.text[0:2] != 'OK':
        quit('Service error. Error code:' + response.text)

    captcha_id = response.text[3:]

    token_url = "http://2captcha.com/res.php?key={}&action=get&id={}".format(key,captcha_id)


    while True:
        time.sleep(10)
        response = requests.get(token_url)
        if response.text[0:2] == 'OK':
            break

    captha_results = response.text[3:]
    driver.execute_script("""document.querySelector('[name="g-recaptcha-response"]').innerText='{}'""".format(captha_results))
    driver.find_element(By.ID, 'recaptcha-demo-submit').click()
    time.sleep(10)

def test():
    driver_path = './chromedriver.exe'
    option = webdriver.ChromeOptions()
    option.add_argument("--incognito")
    # option.add_argument("--headless")

    browser = webdriver.Chrome(executable_path=driver_path, options=option)
    browser.get("https://www.google.com/recaptcha/api2/demo")

    page_url = "https://www.google.com/recaptcha/api2/demo"


    bypass_recaptcha(driver=browser, page_url=page_url, key=key.key)


if __name__=='__main__':
    test()