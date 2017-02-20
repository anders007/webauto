# coding = utf-8

try:
    import Image
except ImportError:
    from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
import os, sys
import time  #调入time函数
from cmsclient import EnumPageType
from cmsclient import LeCmsClient
import const
import utility
from utility import logger
import mysms

#------------------常量定义-------------------------

const.SLEEP_TIME = 6
const.MAX_RETRY_TIME = 5

#------------------常量定义-------------------------


profile_dir = r".\userdata"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("user-data-dir="+os.path.abspath(profile_dir))

browser = webdriver.Chrome(chrome_options=chrome_options)
browser.implicitly_wait(const.SLEEP_TIME)
browser.maximize_window()
browser.get("your url")

leclient = LeCmsClient()
curpage = leclient.curPage(browser)

def retrylogin(browser, client, page):
    retrytime = 0
    # 有可能验证码识别失败，最多尝试登陆5次
    while EnumPageType.EPT_LOGIN == page and retrytime < const.MAX_RETRY_TIME:
        leclient.do_login(browser)
        time.sleep(const.SLEEP_TIME)
        page = client.curPage(browser)
        retrytime += 1

    if retrytime >= const.MAX_RETRY_TIME:
        logger.critical("[error]login fail !!!!!")
        mysms.send_sms("fail", "your mobilephone number")
        browser.quit()
        sys.exit()


if EnumPageType.EPT_LOGIN == curpage:
    retrylogin(browser, leclient, curpage)



mysms.send_sms("success", "your mobilephone number")
time.sleep(const.SLEEP_TIME)
browser.quit()
