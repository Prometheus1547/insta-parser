import re
from datetime import datetime

import cookies
import json_util
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.expected_conditions import staleness_of, presence_of_element_located
from selenium.webdriver.support.ui import WebDriverWait

PATH = 'C:\Python\chromedriver.exe'
URL = 'https://www.instagram.com/'
URL_DIRECT = URL + 'direct/inbox/'

USER = 'prometheus1548'
PASSWORD = 'Stratocaster1547'

driver = webdriver.Chrome(PATH)


def accept_cookies():
    btn = WebDriverWait(driver, 10).until(presence_of_element_located((By.XPATH, "//button")))
    btn.click()
    sleep(0.5)


def authorize():
    inputForm = driver.find_elements_by_xpath('//input')
    inputForm[0].send_keys(USER)
    inputForm[1].send_keys(PASSWORD)
    inputForm[1].send_keys(Keys.ENTER)
    sleep(1)


def disable_notifications():
    try:
        btn = WebDriverWait(driver, 2).until(presence_of_element_located((By.XPATH, "//button[text()='Not Now']")))
        btn.click()
    except:
        pass


def get_dm():
    print("Starting to get DM's")
    driver.get(URL_DIRECT)
    disable_notifications()
    WebDriverWait(driver, 10).until(presence_of_element_located((By.XPATH, "//div[@class='OEMU4']")))
    directs = driver.find_elements_by_xpath("//div[@class='N9abW']//a[@*]")
    dms = []
    sleep(1)
    for x in directs:
        text = x.get_attribute('innerText')
        words = text.split('\n', 1)
        dms.append({
            'title': words[0],
            'id': x.get_attribute('href').rsplit('/', 1)[1],
            'active': get_active(text)
        })

    print(dms)
    json_util.save_file(dms, "dms.json")
    return dms


def get_active(text):
    active = re.search("(Active\s\d+.)|(Active\snow)", text)
    print("string: " + text)
    if active:
        print("string: " + text + " active:true")
        split = active.group().split(' ', 1)
        if split:
            return split[1]
    else:
        return "none"


def get_messages(msg_id):
    print("Started to find messages for id: " + str(msg_id))
    dialogue_pre = driver.find_element_by_xpath("//*[contains(@href'{id_dil}')]".format(id_dil=str(msg_id)))
    name = dialogue_pre.get_attribute("innerText").split('\n', 1)[0]
    print("Open dialogue: " + name)
    dialogue_pre.click()
    sleep(1)
    base_div = '                     Igw0E  Xf6Yq         eGOV_     ybXk5    _4EzTm                                                                                                              '
    inner_div = '_7UhW9   xLCgt      MMzan  KV-D4             p1tLr      hjZTB'
    my_div = 'VdURK e9_tN JRTzd'
    them_div = ' e9_tN JRTzd'
    message_elements = driver.find_elements_by_xpath(f"//div[@class='{base_div}']")
    messages = []
    for msg in message_elements:
        if msg.find_elements(By.XPATH,
                             f"//div[@class='{my_div}']//div[@class='{inner_div}' and contains(span, '{msg.text}')]"):
            messages.append({"me": msg.text})
        else:
            if msg.find_elements(By.XPATH,
                                 f"//div[@class='{them_div}']//div[@class='{inner_div}' and contains(span, '{msg.text}')]"):
                messages.append({"them": msg.text})
    print(messages)
    msg_obj = {"id": msg_id,
               "dialogue_name": name,
               "messages": messages
               }
    json_util.save_file(msg_obj, f"{name}-dm.json")
    sleep(5)


def launch_request():
    print("Started launch request at " + now())
    driver.get(URL)
    if not cookies.check_cookies():
        print("Local cookies not find. Prepare for saving...")
        accept_cookies()
        authorize()
        sleep(5)
        cookies.save_cookie(driver)
    else:
        print("Load local cookies...")
        cookies.load_cookie(driver)
        print("Loaded cookies with success")


def now():
    return str(datetime.now())


launch_request()
