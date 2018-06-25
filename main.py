from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import config_reader
import mysql_connector as mysql_db
import sys, time, socket


class DbConnectException(Exception):
    pass


class ResponseTime:

    def __init__(self):
        self.get_cwd()
        self.init_chrome()
        self.init_config()

        self.pageLoadTime = 0
        self.pageRenderTime = 0
        self.reqResTime = 0
        self.navigationTime = 0

        self.hostname = socket.gethostname()
        self.ip = socket.gethostbyname(self.hostname)

    def get_cwd(self):
        if getattr(sys, 'frozen', False):
            self.config_path = sys._MEIPASS + "\\config.json"
            self.chrome_driver_path = sys._MEIPASS + "\\chromedriver.exe"
        else:
            self.config_path = "config.json"
            self.chrome_driver_path = "chromedriver.exe"

    def init_chrome(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--disable-cache')
        # chrome_options.add_argument('--incognito')
        # chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--window-size=1920x1080")
        self.driver = webdriver.Chrome(chrome_options=self.chrome_options, executable_path=self.chrome_driver_path)

    def init_config(self):
        self.config = config_reader.ConfigReader(self.config_path)
        db_conf = self.config.get_db_details()
        try:
            self.db = mysql_db.DbConnector(db_conf['hostname'], db_conf['username'], db_conf['password'], db_conf['db'])
        except:
            raise DbConnectException

    def calculate_timings(self):
        navigationStart = self.driver.execute_script("return window.performance.timing.navigationStart")
        loadEventEnd = self.driver.execute_script("return window.performance.timing.loadEventEnd")
        # requestStart = self.driver.execute_script("return window.performance.timing.requestStart")
        # responseStart = self.driver.execute_script("return window.performance.timing.responseStart")
        # responseEnd = self.driver.execute_script("return window.performance.timing.responseEnd")
        # domLoading = self.driver.execute_script("return window.performance.timing.domLoading")
        # domComplete = self.driver.execute_script("return window.performance.timing.domComplete")

        self.pageLoadTime = loadEventEnd - navigationStart
        # self.pageRenderTime = domComplete - domLoading
        # self.reqResTime = responseEnd - requestStart

    def navigation_timings(self, each):

        cred = each['login']

        try:
            cpf = self.driver.find_element_by_name(cred['user_elem'])
            cpf.send_keys(cred['username'])
        except NoSuchElementException:
            return 0

        try:
            password = self.driver.find_element_by_name(cred['pass_elem'])
            password.send_keys(cred['password'])
        except NoSuchElementException:
            return 0

        try:
            loginBtn = self.driver.find_element_by_name(cred['submit_elem'])
        except NoSuchElementException:
            loginBtn = self.driver.find_element_by_id(cred['submit_elem'])

        if cred['captcha'] != "":
            captcha = cred['captcha']
            num1 = self.driver.find_element_by_id(captcha['num1_id']).get_attribute('value')
            num2 = self.driver.find_element_by_id(captcha['num2_id']).get_attribute('value')
            sign = self.driver.find_element_by_id(captcha['math_sign_id']).get_attribute('value')

            out = eval(num1 + sign + num2)
            self.driver.find_element_by_id(captcha['userinput_id']).send_keys(out)

            loginBtn.click()

        else:
            loginBtn.click()

        navigationStart = self.driver.execute_script("return window.performance.timing.navigationStart")
        loadEventEnd = self.driver.execute_script("return window.performance.timing.loadEventEnd")

        self.navigationTime = (loadEventEnd - navigationStart)

    def run_test(self):
        sources = self.config.get_urls()
        for each in sources:
            self.driver.get(each['url'])

            if self.driver.title == each['title']:
                self.calculate_timings()
                if each['login'] != "":
                    self.navigation_timings(each)
            else:
                return False

            # self.db.write(each['name'], self.reqResTime, self.pageRenderTime, self.pageLoadTime, self.navigationTime)

        self.driver.quit()
        return True


if __name__ == "__main__":

    try:
        t = ResponseTime()
        while not (t.run_test()):
            print 'no internet : continuing..'
            time.sleep(20)
    except DbConnectException:
        print "Db Connect Error"


