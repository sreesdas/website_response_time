"""

Performance Timing Events flow
navigationStart -> redirectStart -> redirectEnd -> fetchStart -> domainLookupStart -> domainLookupEnd
-> connectStart -> connectEnd -> requestStart -> responseStart -> responseEnd
-> domLoading -> domInteractive -> domContentLoaded -> domComplete -> loadEventStart -> loadEventEnd

"""

from selenium import webdriver

import config_reader
import mysql_connector as mysql_db
import sys

if getattr(sys, 'frozen', False):
    config_path = sys._MEIPASS + "\\config.json"
    chrome_driver_path = sys._MEIPASS + "\\chromedriver.exe"
else:
    config_path = "config.json"
    chrome_driver_path = "chromedriver.exe"


chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--disable-cache')
chrome_options.add_argument('--incognito')
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver_path)

# driver = webdriver.Chrome()

db = mysql_db.DbConnector("root", "", "response_time")
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

    print " ----- %s ----- " % each['name']
    print "Request-Response Time: %s sec" % reqResTime
    print "Page Render Time: %s sec" % pageRenderTime
    print "Total Page Load Time: %s sec" % pageLoadTime

    if each['login'] != "":
        cred = each['login']
        cpf = driver.find_element_by_name(cred['user_elem'])
        cpf.send_keys(cred['username'])

        password = driver.find_element_by_name(cred['pass_elem'])
        password.send_keys(cred['password'])

        try:
            loginBtn = driver.find_element_by_name(cred['submit_elem'])
        except:
            loginBtn = driver.find_element_by_id(cred['submit_elem'])

        loginBtn.click()



        navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
        loadEventEnd = driver.execute_script("return window.performance.timing.loadEventEnd")

        navigationTime = (loadEventEnd - navigationStart )
        print "Navigation Time: %s sec" % navigationTime

    db.write(each['name'], reqResTime, pageRenderTime, pageLoadTime, navigationTime)

    print "\n"

driver.quit()
