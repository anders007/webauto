
import time  #调入time函数
import const
import logging
from selenium.webdriver.common.by import By
import mysms

logger = logging.getLogger('mylogger')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('monitor.log')
fh.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)

const.MAX_RETRY_NUM = 100

def findElement(browser, name, type):
    ele = None
    retrynum = 0

    while (ele is None and retrynum < const.MAX_RETRY_NUM):
        try:
            if By.ID == type:
                ele = browser.find_element_by_id(name)
            elif By.XPATH == type:
                ele = browser.find_element_by_xpath(name)
            elif By.CSS_SELECTOR == type:
                ele = browser.find_element_by_css_selector(name)
            elif By.LINK_TEXT == type:
                ele = browser.find_element_by_link_text(name)
            else:
                ele = None
        except:
            ele = None
            time.sleep(1)
        retrynum += 1

    if ele is None:
        mysms.send_sms("fail", "your mobilephone number")
        logger.critical("element %s is not found ! retry times: %d", name, retrynum)
        browser.quit()

    return ele

def findElementAndClick(browser, name, type):
    done = False
    retrynum = 0

    while (False == done and retrynum < const.MAX_RETRY_NUM):
        try:
            if By.ID == type:
                browser.find_element_by_id(name).click()
            elif By.XPATH == type:
                browser.find_element_by_xpath(name).click()
            elif By.CSS_SELECTOR == type:
                browser.find_element_by_css_selector(name).click()
            elif By.LINK_TEXT == type:
                browser.find_element_by_link_text(name).click()

            done = True
        except:
            time.sleep(1)
        retrynum += 1

    if False == done:
        mysms.send_sms("fail", "your mobilephone number")
        logger.critical("element %s is not clicked ! retry times: %d", name, retrynum)
        browser.quit()


def findElementAndSetContext(browser, name, type, context):
    done = False
    retrynum = 0

    while (False == done and retrynum < const.MAX_RETRY_NUM):
        try:
            if By.ID == type:
                ele = browser.find_element_by_id(name)
            elif By.XPATH == type:
                ele = browser.find_element_by_xpath(name)
            elif By.CSS_SELECTOR == type:
                ele = browser.find_element_by_css_selector(name)
            elif By.LINK_TEXT == type:
                ele = browser.find_element_by_link_text(name)

            ele.clear()
            ele.send_keys(context)
            done = True
        except:
            time.sleep(1)
        retrynum += 1

    if False == done:
        mysms.send_sms("fail", "your mobilephone number")
        logger.critical("element %s is not clicked ! retry times: %d", name, retrynum)
        browser.quit()


def findElementAndSetContextWhenTextNotNull(browser, name, type, context):
    done = False
    retrynum = 0

    while (False == done and retrynum < const.MAX_RETRY_NUM):
        try:
            if By.ID == type:
                ele = browser.find_element_by_id(name)
            elif By.XPATH == type:
                ele = browser.find_element_by_xpath(name)
            elif By.CSS_SELECTOR == type:
                ele = browser.find_element_by_css_selector(name)
            elif By.LINK_TEXT == type:
                ele = browser.find_element_by_link_text(name)

            value = ele.get_attribute('value')
            if "" != value:
                ele.clear()
                ele.send_keys(context)
                done = True
            else:
                time.sleep(1)

        except:
            time.sleep(1)
        retrynum += 1

    if False == done:
        mysms.send_sms("fail", "your mobilephone number")
        logger.critical("element %s is not clicked ! retry times: %d", name, retrynum)
        browser.quit()

