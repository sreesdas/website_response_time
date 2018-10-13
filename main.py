"""

Performance Timing Events flow
navigationStart -> redirectStart -> redirectEnd -> fetchStart -> domainLookupStart -> domainLookupEnd
-> connectStart -> connectEnd -> requestStart -> responseStart -> responseEnd
-> domLoading -> domInteractive -> domContentLoaded -> domComplete -> loadEventStart -> loadEventEnd

"""

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

import config_reader
import mysql_connector as mysql_db
import sys, platform

if getattr(sys, 'frozen', False):
    config_path = sys._MEIPASS + "\\config.json"
    chrome_driver_path = sys._MEIPASS + "\\chromedriver.exe"
else:
    config_path = "config.json"
    chrome_driver_path = "chromedriver.exe"


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-cache')
# chrome_options.add_argument('--incognito')
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver_path)

hostname = platform.node()

# db = mysql_db.DbConnector("root", "", "response_time")

f = open('report.txt', 'a') # to be deleted in prod
f.write("\n\nRunning the offline version without db..\n\n") # to be deleted in prod

config = config_reader.ConfigReader(config_path)
sources = config.get_urls()

for each in sources:

    driver.get(each['url'])

    navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
    loadEventEnd = driver.execute_script("return window.performance.timing.loadEventEnd")
    requestStart = driver.execute_script("return window.performance.timing.requestStart")
    responseStart = driver.execute_script("return window.performance.timing.responseStart")
    responseEnd = driver.execute_script("return window.performance.timing.responseEnd")
    domLoading = driver.execute_script("return window.performance.timing.domLoading")
    domComplete = driver.execute_script("return window.performance.timing.domComplete")

    pageLoadTime = loadEventEnd - navigationStart
    pageRenderTime = domComplete - domLoading
    reqResTime = responseEnd - requestStart
    navigationTime = 0

    f.write(" ----- %s ----- \n" % each['name'])
    f.write("LoginPage Load Time: %s ms\n" % pageLoadTime)

    if each['login'] != "":
        cred = each['login']

        try:
            cpf = driver.find_element_by_name(cred['user_elem'])
            cpf.send_keys(cred['username'])
        except NoSuchElementException:
            continue

        try:
            password = driver.find_element_by_name(cred['pass_elem'])
            password.send_keys(cred['password'])
        except NoSuchElementException:
            continue

        try:
            loginBtn = driver.find_element_by_name(cred['submit_elem'])
        except NoSuchElementException:
            loginBtn = driver.find_element_by_id(cred['submit_elem'])

        if cred['captcha'] != "":
            captcha = cred['captcha']
            num1 = driver.find_element_by_id(captcha['num1_id']).get_attribute('value')
            num2 = driver.find_element_by_id(captcha['num2_id']).get_attribute('value')
            sign = driver.find_element_by_id(captcha['math_sign_id']).get_attribute('value')

            out = eval(num1 + sign + num2)
            driver.find_element_by_id(captcha['userinput_id']).send_keys(out)

            loginBtn.click()

        else:
            loginBtn.click()

        navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
        loadEventEnd = driver.execute_script("return window.performance.timing.loadEventEnd")

        navigationTime = (loadEventEnd - navigationStart )
        f.write( "HomePage Load Time: %s ms\n" % navigationTime )

    db.write(each['name'], reqResTime, pageRenderTime, pageLoadTime, navigationTime)

    f.write("\n")

f.close()
driver.quit()
