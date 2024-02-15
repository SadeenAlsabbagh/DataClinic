from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import time
from bs4 import BeautifulSoup

driver = webdriver.Chrome()

try:
    # Open LinkedIn
    driver.get("https://www.linkedin.com")

    # Find the login elements
    username = driver.find_element(By.ID, "session_key")
    password = driver.find_element(By.ID, "session_password")

    # Enter your LinkedIn credentials
    username.send_keys('princenoworkhere@gmail.com')
    password.send_keys('DataClinic')

    # Submit the login form
    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()

    driver.get("https://www.linkedin.com/jobs")
    search_box = driver.find_element(By.CLASS_NAME, "jobs-search-box__text-input")
    search_box.send_keys("Sustainability")
    search_box.send_keys(Keys.RETURN)

    time.sleep(10)  # Adjusted wait time

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    job_postings = soup.find_all('div', class_='job-posting-class-or-id')  # Replace with actual class or id

    for job in job_postings:
        title = job.find('h3', class_='title-class').get_text()  # Replace with actual class or id
        company = job.find('h4', class_='company-class').get_text()  # Replace with actual class or id
        # Extract other details in a similar way

        print(f"Title: {title}, Company: {company}")



finally:
    driver.quit()

