from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

def check_xpath(driver, xpath):
    try:
        driver.find_element(By.XPATH, xpath)
        exist = True
    except NoSuchElementException:
        exist = False
    return exist
def check_class(Class, driver):
        try:
            driver.find_element(By.CLASS_NAME, Class)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist