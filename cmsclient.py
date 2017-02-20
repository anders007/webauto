#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import Image
except ImportError:
    from PIL import Image
import xml.etree.ElementTree as ET
from ruokuaiclient import APIClient
from enum import Enum
import time
import const
import utility
from selenium.webdriver.common.by import By

const.FILE_SCREENSHORT = "screenshort.png"
const.FILE_VERIFYCODE = "code.png"
const.FILE_UPLOAD = "upload.png"

class EnumPageType(Enum):
    EPT_INVALID = 0
    EPT_LOGIN = 1
    EPT_CMS_ROOT = 2


class LeCmsClient(object):

    def curPage(self, browser):
        page = EnumPageType.EPT_INVALID
        try:
            browser.find_element_by_id("id_username")
            page = EnumPageType.EPT_LOGIN
        except:
            page = EnumPageType.EPT_CMS_ROOT
        return page

    def do_login(self, browser):

        utility.findElementAndSetContext(browser, "id_username", By.ID, "username")
        utility.findElementAndSetContext(browser, "id_password", By.ID, "password")

        browser.save_screenshot(const.FILE_SCREENSHORT)
        vcimgcontrl = utility.findElement(browser, "//img[@id='img_code']", By.XPATH)
        location = vcimgcontrl.location
        size = vcimgcontrl.size
        # 写成我们需要截取的位置坐标
        rangle = (
        int(location['x']), int(location['y']), int(location['x'] + size['width']), int(location['y'] + size['height']))
        i = Image.open(const.FILE_SCREENSHORT)
        framevcimg = i.crop(rangle)
        framevcimg.save(const.FILE_VERIFYCODE)

        # ---------------------------------------------------------------------------------
        # 把图片验证码发给若快识别

        client = APIClient()

        paramDict = {}
        result = ''

        paramDict['username'] = 'username'
        paramDict['password'] = 'password'
        paramDict['typeid'] = '3040'
        paramDict['timeout'] = '60'
        paramDict['softid'] = 'softid'
        paramDict['softkey'] = 'softkey'
        paramKeys = ['username',
                     'password',
                     'typeid',
                     'timeout',
                     'softid',
                     'softkey'
                     ]

        img = Image.open(const.FILE_VERIFYCODE)
        if img is None:
            print('get file error!')
            quit()

        pixdata = img.load()
        # 以下的识别码图片解析前预处理是根据特定类型的识别码做的，不同的场景可能需要做不同的处理
        # 把黑色的点去掉（变成白色）
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if (pixdata[x, y][0] < 100) \
                        and (pixdata[x, y][1] < 100) \
                        and (pixdata[x, y][2] < 100):
                    pixdata[x, y] = (255, 255, 255, 255)
        # 图片灰度转换，将图片二值化，方便识别，提高识别成功率
        img = img.convert("L")
        img.save(const.FILE_UPLOAD, format="png")
        filebytes = open(const.FILE_UPLOAD, "rb").read()
        result = client.http_upload_image("http://api.ruokuai.com/create.xml", paramKeys, paramDict, filebytes)

        root = ET.fromstring(result)
        vcstr = root.find("Result").text

        utility.findElementAndSetContext(browser, "id_verfycode", By.ID, vcstr)
        # 确定登录
        utility.findElementAndClick(browser, "btn_submit", By.ID)


