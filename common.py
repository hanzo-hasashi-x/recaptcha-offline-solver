from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.service import Service
from selenium.webdriver.common.by import By
from selenium.common import exceptions
import undetected_chromedriver as uc
from selenium import webdriver

import pickle
import random
import time


class Driver:

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    def get_options(self, headless):
        options = uc.ChromeOptions()

        if headless:
            options.add_argument("--headless")
        
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument(f"--user-agent={self.user_agent}")
        options.add_argument('--disable-notifications')
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")
        options.add_argument("--no-first-run")
        options.add_argument("--disable-fre")
    
        options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
        options.add_argument("--no-default-browser-check")
        options.add_argument('--no-sandbox')

        return options

    def __init__(self, driver_path=None, headless=True, window_size=(1400, 900),
                 actions=True, wait_timeout=10):
    
        self.driver_path = driver_path

        self.driver_ = uc.Chrome(driver_executable_path=driver_path,
                                 options=self.get_options(headless))
        self.driver_.set_window_size(*window_size)

        self.actions = ActionChains(self.driver_) if actions else None
        self.wait = WebDriverWait(self.driver_, wait_timeout) if wait_timeout else None

    def check_xpath(self, xpath):
        try:
            self.driver_.find_element(By.XPATH, xpath)
            exist = True
        except exceptions.NoSuchElementException:
            exist = False
        return exist

    def check_class(self, class_):
        try:
            self.driver_.find_element(By.CLASS_NAME, class_)
            exist = True
        except exceptions.NoSuchElementException:
            exist = False
        return exist

    def close_windows(self, main_handle):
        # function of closing not necessary windows
        for handle in self.driver_.window_handles:
            try:
    
                if handle != main_handle:
                    self.driver_.switch_to.window(handle)
                    self.driver_.close()
                    time.sleep(1)
            except:
                continue
        self.driver_.switch_to.window(main_handle)

    def stop(self):
        self.driver_.close(), self.driver_.quit()

    ec_conditions = {
        "element_precence": ec.presence_of_element_located,
        "elements_precence": ec.presence_of_all_elements_located,
        "clickable": ec.element_to_be_clickable
    }
    def get_element(self, search_term, selector=By.XPATH, condition='element_precence'):
        ec_condition = self.ec_conditions[condition]
        element = self.wait.until(ec_condition( (selector, search_term) ))

        return element

    def get_elements(self, search_term, selector=By.XPATH):
        return self.get_element(search_term, selector, condition='elements_precence')
    
    #==========================Working with time==========================
    
    def delay(self):
        t = random.randint(150000000, 300000000)
    
        t = t  / 100000000
        # wait
        time.sleep(t)
    
    #=========================Working with cookies==========================
    
    def set_cookies(self, cookies):
        try:
            cookies = pickle.load(open(cookies, "rb"))
            for cookie in cookies:
                self.driver_.add_cookie(cookie)
            self.driver_.refresh()
        except Exception as e:
            pass
    
    def get_cookies(self, cookies):
        try:
            pickle.dump(self.driver_.get_cookies(), open(cookies, "wb"))
        except Exception as e:
            pass

