import logging
import os
import pickle
import sys
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.warning('Reference: https://iqss.github.io/dss-webscrape/filling-in-web-forms.html')
logging.warning('Reference: https://selenium-python.readthedocs.io/locating-elements.html')
logging.warning('Reference: https://pythonbasics.org/selenium-wait-for-page-to-load/')
logging.warning('Reference: https://www.selenium.dev/selenium/docs/api/py/webdriver_chromium/selenium.webdriver.chromium.webdriver.html?highlight=refresh#selenium.webdriver.chromium.webdriver.ChromiumDriver.refresh')
logging.warning('Reference: https://www.selenium.dev/documentation/webdriver/actions_api/mouse/')

def wait_for_loading(driver, xpath, plural=False):
    timeout = 30
    try:
        if plural:
            element_present = EC.presence_of_all_elements_located((By.XPATH, xpath))
            print(f'Checking for row td {xpath}')
        else:
            element_present = EC.presence_of_element_located((By.XPATH, xpath))

        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print(f'Timed out waiting for {xpath} to load')
        sys.exit()
    finally:
        print(f'Page loaded: {xpath}')

CODE = os.getenv('CODE')
URL = os.getenv('URL')
PICKLE_FN = os.getenv('PICKLE_FN', 'current_datadump.pickle')
READ_PICKLE =  os.getenv('READ_PICKLE', 'no') == 'yes'

if not READ_PICKLE:
    if not CODE:
        sys.exit('''Yikes,....
        There is no CODE variable in the environment!!!
        ''')
    if not URL:
        sys.exit('''Yikes,....
        There is no URL variable in the environment!!!
        ''')

    driver = webdriver.Chrome()
    driver.get(URL)

    xpath = '//input[1]'
    _ = wait_for_loading(driver, xpath)
    input_box = driver.find_element(By.XPATH, xpath)
    input_box.send_keys(CODE)

    xpath = '//button[text()=" Rechercher "]'
    _ = wait_for_loading(driver, xpath)
    driver.find_element(By.XPATH, xpath).click()

    xpath = '//button[text()=" Élèves "]'
    _ = wait_for_loading(driver, xpath)
    driver.find_element(By.XPATH, xpath).click()

    student_list = []

def main():
    while True:
        xpath = '/html/body/app-root/div/main/div/app-list/div/div[3]/div[1]/table/tbody'
        _ = wait_for_loading(driver, xpath)
        table_body = driver.find_element(By.XPATH, xpath)
        sleep(0.5)

        xpath = ".//tr"
        _ = wait_for_loading(table_body, xpath, plural=True)

        table_rows = driver.find_elements(By.XPATH, xpath)
        sleep(0.5)

        for row in table_rows:
            l = [td.text for td in row.find_elements(By.XPATH, ".//td")]
            if l:
                if l not in student_list:
                    student_list.append(l)
                    print(l)
                else:
                    print(f'DUPLICATE: {l}')
        print(len(student_list))
        #_ = input('Press enter to continue')

        try:
            xpath_next = '/html/body/app-root/div/main/div/app-list/div/div[3]/div[2]/nav/ul/li[3]/a'
            _ = wait_for_loading(driver, xpath_next)

            next_page_link = driver.find_element(By.XPATH, xpath_next)
            driver.execute_script("arguments[0].click();", next_page_link)
            sleep(0.5)

        except ElementClickInterceptedException as e:
            print(f'Finished: {type(e)} - {e}')

if __name__ == '__main__':
    try:
        if READ_PICKLE:
            with open(PICKLE_FN, 'rb') as fh:
                students = pickle.load(fh)
                print(students)
                print(f'Number of students: {len(students)}')
        else:
            _ = main()
    except KeyboardInterrupt as e:
        sys.exit('''
        Exiting ...
        ''')
    finally:
        if not READ_PICKLE:
            driver.quit()
            with open(PICKLE_FN, 'wb') as fh:
                pickle.dump(student_list, fh)

            print(f'Finished writing {PICKLE_FN}')

# vim: ai et ts=4 sts=4 sw=4 nu
