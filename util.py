import csv
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

default_user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'

def write_csv_file(filename: str, columns: list, records: list):
    with open(filename, 'w', newline='', encoding="utf-8") as output_file:
        writer = csv.writer(output_file)
        writer.writerow(columns)
        if len(columns) != len(records[0]):
            print('columns and records are not matched')
            return
        for record in records:
            writer.writerow(record)
    pass
    return filename


def get_page_by_selenium(url: str, wait_time: int = 10,user_agent: str = default_user_agent):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-gpu')
    options.add_argument('--allow-running-insecure-content')
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        # WebDriverWait(driver, wait_time).until(ec.presence_of_element_located((By.XPATH, '//ul[@data-testid="hero-title-block__metadata"]')))
        html = driver.page_source
    except TimeoutException:
        print('Error: get_page_by_selenium')
        html = None
    finally:
        driver.quit()
    return html


def sanitize_filename(filename):
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename
