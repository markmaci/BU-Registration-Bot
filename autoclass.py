import requests
import re
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import os
from selenium.common.exceptions import NoSuchElementException

from settings import USERNAME, PASSWORD
# from settings import USERNAME, PASSWORD
# import logging
# import datetime

PATH = "./chromedriver_mac_arm64/chromedriver"

def check_exists_by_xpath(xpath):
    try:
        wd.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

def credentials():
    return (USERNAME, PASSWORD)

wd = webdriver.Chrome()

wd.implicitly_wait(5)  # seconds

wd.get("https://student.bu.edu/MyBU/s/")
username, password = credentials()
wd.find_element(By.ID, "j_username").send_keys(username)
wd.find_element(By.ID, "j_password").send_keys(password)
wd.find_element(By.CLASS_NAME, "input-submit").click()
while "studentlink" not in wd.current_url:
    time.sleep(3)
myAcademics = wd.find_element(By.XPATH, ('//*[@id="CustomerPortalTemplate"]/div[1]/div[2]/div/div/div[2]/div/div/div/community_navigation-global-navigation-list/div/nav/ul/li[2]'))
myAcademics.click()
wd.implicitly_wait(1)

myClasses = wd.find_element(By.XPATH, ('//*[@id="CustomerPortalTemplate"]/div[2]/div/div[2]/div[1]/div/div[1]/community_navigation-tile-menu/community_navigation-tile-menu-ui/community_navigation-tile-menu-item[3]/a/community_navigation-tile-menu-item-unified-layout/div/div'))
myClasses.click()
wd.implicitly_wait(1)

myAcademics = wd.find_element(By.XPATH, ('/html/body/table[1]/tbody/tr[2]/td[1]/table/tbody/tr/td[2]'))
myAcademics.click()
wd.implicitly_wait(1)

Register = wd.find_element(By.XPATH, ('/html/body/table[2]/tbody/tr[2]/td/table/tbody/tr/td/font/a[8]'))
Register.click()

regOptions = wd.find_element(By.XPATH, ('/html/body/table[3]/tbody/tr[2]/td[1]/a[1]'))
regOptions.click()
wd.implicitly_wait(1)

registerFor = wd.find_element(By.XPATH, ('/html/body/center[1]/table[2]/tbody/tr[3]/td[2]/a'))
registerFor.click()
wd.implicitly_wait(1)

dropDown = wd.find_element(By.XPATH, ('/html/body/table[4]/tbody/tr[3]/td[2]/form/table/tbody/tr[2]/td[1]/select'))
Select(dropDown).select_by_value('CAS') #MUST FIX FOR INTENDED COLLEGE, CAS IS DEFAULT, VARIABLE WILL BE PLACED

dept = wd.find_element(By.XPATH, ('/html/body/table[4]/tbody/tr[3]/td[2]/form/table/tbody/tr[2]/td[2]/input'))
dept.send_keys('CS') #MUST FIX FOR INTENDED DEPT, CS IS DEFAULT, VARIABLE WILL BE PLACED

course = wd.find_element(By.XPATH, ('/html/body/table[4]/tbody/tr[3]/td[2]/form/table/tbody/tr[2]/td[3]/input'))
course.send_keys('111') #MUST FIX FOR INTENDED COURSE, 111 IS DEFAULT, VARIABLE WILL BE PLACED

section = wd.find_element(By.XPATH, ('/html/body/table[4]/tbody/tr[3]/td[2]/form/table/tbody/tr[2]/td[4]/input'))
section.send_keys('A1') #MUST FIX FOR INTENDED SECTION, A1 IS DEFAULT, VARIABLE WILL BE PLACED

goBtn = wd.find_element(By.XPATH, ('/html/body/table[4]/tbody/tr[3]/td[2]/form/table/tbody/tr[2]/td[6]/input'))
goBtn.click()
wd.implicitly_wait(1)

#This XPATH is specific but I will make it such that it has a relative xpath
# with a variable relating to the name of the course
rowOfClass = wd.find_element(By.XPATH, ('/html/body/form/table[1]/tbody/tr[3]'))

#Same for here, this relates to the image.
if(check_exists_by_xpath('/html/body/form/table[1]/tbody/tr[3]/td[1]/a/img')):
    print("Class is closed!")
else:
    print("Class is open!")
    #this where the user will get an email saying they have signed up successfully 
    open = wd.find_element(By.XPATH, ('/html/body/form/table[1]/tbody/tr[5]/td[1]/input'))
    open.click()
    addSchedule = wd.find_element(By.XPATH, ('/html/body/form/center[2]/table/tbody/tr/td[1]/input'))
    addSchedule.click()
    alert_obj = wd.switch_to.alert
    alert_obj.accept() #this will close the alert box and accept the alert
    wd.implicitly_wait(1)
    if check_exists_by_xpath('/html/body/table[4]/tbody/tr[2]/td[1]/img'): #This is the check mark image
        print("Class was added to schedule")
    else:
        print("Class was not added to schedule")

wd.quit()