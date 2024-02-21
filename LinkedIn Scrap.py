from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import os

def initialize_driver():
    driver = webdriver.Chrome()
    driver.wait = WebDriverWait(driver, 10)
    return driver

def login_to_linkedin(driver, username, password):
    driver.get("https://www.linkedin.com")
    username_field = driver.wait.until(EC.presence_of_element_located((By.ID, "session_key")))
    password_field = driver.wait.until(EC.presence_of_element_located((By.ID, "session_password")))
    
    username_field.send_keys(username)
    password_field.send_keys(password)

    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()

def search_jobs(driver, keyword):
    driver.get("https://www.linkedin.com/jobs")
    search_box = driver.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "jobs-search-box__text-input")))
    search_box.send_keys(keyword)
    search_box.send_keys(Keys.RETURN)

def scrape_jobs(driver):
    # Wait until the job card containers are loaded
    driver.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'job-card-container')))

    # Get the current page's source and create a BeautifulSoup object
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Find all job posting containers using the class name
    job_postings = soup.find_all('div', class_='job-card-container')

    for job in job_postings:
        # Extract the title using the previously identified class name
        title_element = job.find('a', class_='disabled ember-view job-card-container__link job-card-list__title')
        title = title_element.get_text(strip=True) if title_element else 'No Title Found'
        
        # Extract the company name using the class identified from the screenshot
        company_element = job.find('span', class_='job-card-container__primary-description')
        company = company_element.get_text(strip=True) if company_element else 'No Company Found'

        print(f"Title: {title}, Company: {company}")

def main():
    linkedin_username = os.environ.get('LINKEDIN_USERNAME')
    linkedin_password = os.environ.get('LINKEDIN_PASSWORD')

    driver = initialize_driver()
    try:
        login_to_linkedin(driver, 'princenoworkhere@gmail.com', 'DataClinic')
        search_jobs(driver, "Sustainability")
        scrape_jobs(driver)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
