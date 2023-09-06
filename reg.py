import requests
import re
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from settings import USERNAME, PASSWORD
import logging
import datetime

# Set up the logging configuration
logging.basicConfig(filename='class_registration.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


TURN_ON_REAL_REGISTRATION = False

# set the module as the planner
module = "reg/plan/add_planner.pl"
is_planner = "Y"

if TURN_ON_REAL_REGISTRATION:
    # set the module for real class registration
    module = "reg/add/confirm_classes.pl"
    is_planner = ""


"""
Press F12 in chrome, navigate to the Network tab, then go to your planner on student link, 
click on the item with a long number, under request headers find "Cookie: .... " 
Copy the `cookie` header below
"""
cookies = "f5_cspm=1234; f5avraaaaaaaaaaaaaaaa_session_=HNOJJDPHFFBCAKPIGHDFNHEKOEOBDNPJBCHELPFDHPGMDHBPOOBDNHGOHGPMPOHIJGFDNGPCFKMIHIMIMKBABHAAOCOIJDHMGLACKGFBFMNIDOIHPJONBELJLKFKJMEP; apt.uid=AP-PQQY5YJEHTTA-2-1662922219175-64262784.0.2.be9b9689-258c-45c1-92ed-3c3793cc6b10; ph_foZTeM1AW8dh5WkaofxTYiInBhS4XzTzRqLs50kVziw_posthog=%7B%22distinct_id%22%3A%221890df2852aaa5-0cedc4f762c71c-1d525634-16a7f0-1890df2852b27d9%22%2C%22%24device_id%22%3A%221890df2852aaa5-0cedc4f762c71c-1d525634-16a7f0-1890df2852b27d9%22%2C%22%24user_state%22%3A%22anonymous%22%2C%22extension_version%22%3A%221.5.5%22%2C%22%24session_recording_enabled_server_side%22%3Afalse%2C%22%24autocapture_disabled_server_side%22%3Afalse%2C%22%24active_feature_flags%22%3A%5B%5D%2C%22%24enabled_feature_flags%22%3A%7B%22enable-session-recording%22%3Afalse%2C%22sourcing%22%3Afalse%2C%22only-company-edit%22%3Afalse%2C%22job-lists%22%3Afalse%7D%2C%22%24feature_flag_payloads%22%3A%7B%7D%7D; AWSALB=vQeckX9UCdbW00KGv9/TPMsmJESGTze/rkxagcErORtFuZvekB6sEkFviFpsWNE1TOf9SF7AeIg3T/oAdtivYEzZHCfLmUd2VGip7NQNiuepCGckwJEr8ycUXutKBWOxYlF5LKalPI/rCoU7yNqBD9D0MIC9DBHNQi4zzGe1QifkhHj2g3YGSTsAnwIzmw==; AWSALBCORS=vQeckX9UCdbW00KGv9/TPMsmJESGTze/rkxagcErORtFuZvekB6sEkFviFpsWNE1TOf9SF7AeIg3T/oAdtivYEzZHCfLmUd2VGip7NQNiuepCGckwJEr8ycUXutKBWOxYlF5LKalPI/rCoU7yNqBD9D0MIC9DBHNQi4zzGe1QifkhHj2g3YGSTsAnwIzmw==; uiscgi_prod=7866ff5ecaab7c53e6dea8bb76b63402:prod; BIGipServerist-uiscgi-app-prod-443-pool=1271252352.47873.0000; BIGipServerist-uiscgi-app-prod-80-pool=1288029568.20480.0000; BIGipServerist-web-legacy-prod-80-pool=907866378.31745.0000; BIGipServerist-wp-app-prod-443-pool=3542148874.47873.0000; BIGipServerwww-prod-crc-443-pool=1833771789.47873.0000; BIGipServerwww-prod-crc-80-pool=139272973.20480.0000; BIGipServerist-web-legacy-prod-443-pool=1662710026.31745.0000"


# You might also have to copy the other headers into here
def generate_headers():
    return {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Cookie": cookies,
        "DNT": "1",
        "Host": "www.bu.edu",
        "Referer": "https://www.bu.edu/link/bin/uiscgi_studentlink.pl/1524338857/1524338857",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    }


url = "https://www.bu.edu/link/bin/uiscgi_studentlink.pl/1693985675"


def generate_params(college, dept, course, section):
    return {
        "College": college,
        "Dept": dept,
        "Course": course,
        "Section": section,
        "ModuleName": "reg/add/browse_schedule.pl",
        "AddPreregInd": "",
        "AddPlannerInd": "",
        "ViewSem": "Fall 2023",
        "KeySem": "20243",
        "PreregViewSem": "",
        "PreregKeySem": "",
        "SearchOptionCd": "S",
        "SearchOptionDesc": "Class Number",
        "MainCampusInd": "",
        "BrowseContinueInd": "",
        "ShoppingCartInd": "",
        "ShoppingCartList": "",
    }


def generate_reg_params(college, dept, course, section, ssid):
    return {
        "SelectIt": ssid,
        "College": college.upper(),
        "Dept": dept.upper(),
        "Course": course,
        "Section": section.upper(),
        "ModuleName": module,
        "AddPreregInd": "",
        "AddPlannerInd": is_planner,
        "ViewSem": "Fall 2023",
        "KeySem": "20243",
        "PreregViewSem": "",
        "PreregKeySem": "",
        "SearchOptionCd": "S",
        "SearchOptionDesc": "Class Number",
        "MainCampusInd": "",
        "BrowseContinueInd": "",
        "ShoppingCartInd": "",
        "ShoppingCartList": "",
    }


# Replace with your own BU login and password.
# Your credentials are only stored in this file, and I am not liable if you expose this file to anyone else.
def credentials():
    return (USERNAME, PASSWORD)


def login():
    print("logging in...")
    driver = webdriver.Chrome()

    driver.get(
        "https://www.bu.edu/link/bin/uiscgi_studentlink.pl/1524541319?ModuleName=regsched.pl"
    )
    username, password = credentials()
    driver.find_element(By.ID, "j_username").send_keys(username)
    driver.find_element(By.ID, "j_password").send_keys(password)
    driver.find_element(By.CLASS_NAME, "input-submit").click()
    while "studentlink" not in driver.current_url:
        time.sleep(3)

    cookies_list = driver.get_cookies()
    global cookies
    cookies = ""
    for cookie in cookies_list:
        cookies = cookies + cookie["name"] + "=" + cookie["value"] + "; "
    print("Retrieving cookies: " + cookies)


"""
Finds course listing and tries to register for the class.

Sometimes course names are wrong, use at your own discretion. 
"""


def find_course(college, dept, course, section):
    name = dept.upper() + course + " " + section.upper()
    print("searching for " + name)
    params_browse = generate_params(college, dept, course, section)
    headers = generate_headers()
    ####
    for retry in range(1, 5):
        # logging.warning('[fetch] try=%d, url=%s' % (retry, url))
        retry_because_of_timeout = False
        try:
            r = requests.get(url, headers=headers, params=params_browse, timeout=3)
            # log request
            text = r.text
            logging.info("FIND COURSE REQUEST: %s" % (r.text))
            # logging.info("FIND COURSE REQUEST TEXT: %s" % (text))
        except Exception as e:
            print(e)
            retry_because_of_timeout = True
            logging.warning("Exception: %s" % (e))
            pass

        if retry_because_of_timeout:
            time.sleep(retry * 2 + 1)
        else:
            break
    ####

    p = re.compile("<tr ALIGN=center Valign= top>.+?</td></tr>", re.DOTALL)
    logging.info("COURSE LIST: %s" % (p))
    m = p.findall(text)
    logging.info("COURSE LIST AFTER findAll: %s" % (m))
    if len(m) == 0:
        print("Something went wrong with the request for " + dept + course)
        login()
        find_course(college, dept, course, section)
        return
    s = college.upper() + dept.upper() + course + "%20" + section.upper()

    found = False
    for item in m:
        if re.search(s, item):
            found = True
            n = re.search('value="(\d{10})"', item)
            if n:
                params_reg = generate_reg_params(
                    college, dept, course, section, n.group(1)
                )
                reg = requests.get(url, headers=headers, params=params_reg)
                logging.info("REGISTER REQUEST: %s" % (reg.text))
                
                o = re.search("<title>Error</title>", reg.text)
                if o:
                    print("Can not register yet :/")
                else:
                    print("Registered successfully!")
            else:
                print("Class is full :(")
            break
    if not found:
        print("could not find course")


# Replace with your own course.
# Ex. ('cas','wr','100','a1')
my_courses = [
    ("CAS", "CS", "320", "B1"),
    ("CAS", "CS", "412", "A1"),
    ("CAS", "CS", "115", "A1"),
]

beginning = time.time()
cycles = 0
login()
# while True:
for i in my_courses:
    print("\n[" + str(time.asctime()) + "]")
    start = time.time()
    find_course(*i)
    duration = time.time() - start
    print("Took " + str(round(duration, 1)) + " seconds")
    cycles += 1
    print("Average time: " + str(round((time.time() - beginning) / cycles, 1)))
