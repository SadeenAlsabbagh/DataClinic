from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from bs4 import BeautifulSoup
import time
import os
def initialize_driver():
    driver = webdriver.Chrome()
    options = webdriver.ChromeOptions()
    options.headless = False  # Change to True if you don't want the browser window to open
    driver = webdriver.Chrome(options=options)
    driver.wait = WebDriverWait(driver, 10)
    return driver

def login_to_linkedin(driver, username, password):
    driver.get("https://www.linkedin.com/login")
    username_field = driver.wait.until(EC.presence_of_element_located((By.ID, "username")))
    password_field = driver.wait.until(EC.presence_of_element_located((By.ID, "password")))
    
    username_field.send_keys(username)
    password_field.send_keys(password)

    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()

def search_jobs(driver, keyword):
    driver.get("https://www.linkedin.com/jobs")
    search_box = driver.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "jobs-search-box__text-input")))
    search_box.send_keys(keyword)
    search_box.send_keys(Keys.RETURN)

def get_each_job_info(driver, jobs_links):
    all_jobs = []
    for j in jobs_links:
        driver.get(j)
        content = driver.page_source
        soup = BeautifulSoup(content, 'html.parser')
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)") 
        
        ####data###
        job = {
            'title': soup.find('a', class_='job-card-list__title').text if soup.find('a', class_='job-card-list__title') else "",
            'location': soup.find('li', class_='job-card-container__metadata-item').text.strip() if soup.find('li', class_='job-card-container__metadata-item') else "",
            'company name': soup.find('span', class_='job-card-container__primary-description').text.strip() if soup.find('span', class_='job-card-container__primary-description') else "",
            'job_link': j
        }
        all_jobs.append(job)
    return all_jobs

def get_current_page_jobs(driver):
    jobs_links = []
    jobs = driver.find_elements(By.XPATH, "//div[@class='full-width artdeco-entity-lockup__title ember-view']/a[@href]")
    for l in jobs:
        jobs_links.append(l.get_attribute('href'))
    return get_each_job_info(driver, jobs_links)

def scrape_jobs(driver):
    all_jobs = []
    current_page = 1
    while True:
        all_jobs.extend(get_current_page_jobs(driver))
        print(f'Page {current_page} completed')
        current_page += 1
        
        try:
            next_page_button = driver.wait.until(EC.element_to_be_clickable((By.XPATH, f"//button[@aria-label='Page {current_page}']")))
            next_page_button.click()
            time.sleep(2)
        except TimeoutException:
            break
    return all_jobs

def main():
    driver = initialize_driver()
    try:
        login_to_linkedin(driver, 'princenoworkhere@gmail.com', 'DataClinic')
        search_jobs(driver, "Sustainability")
        all_jobs = scrape_jobs(driver)
        print(all_jobs)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
