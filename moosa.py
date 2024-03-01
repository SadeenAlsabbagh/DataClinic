import pandas as pd
import numpy as np
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

def login_to_linkedin(username, password):
    driver = webdriver.Chrome()

    try:
        # Open LinkedIn
        driver.get("https://www.linkedin.com")

        username_field = driver.find_element(By.ID, "session_key")
        password_field = driver.find_element(By.ID, "session_password")

        # Enter credentials
        username_field.send_keys(username)
        password_field.send_keys(password)

        # Submit the login form
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()

        time.sleep(10)

        return driver

    except Exception as e:
        print(f"Failed to login: {e}")
        return None

def scrape_jobs(driver, search_query, location, num_pages=1):
    base_url = "https://www.linkedin.com/jobs/search/"
    jobs = []

    page = 1
    while True:
        page_url = f"{base_url}?keywords={search_query}&location={location}&start={page * 25}"
        driver.get(page_url)
        time.sleep(2)

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        job_listings = soup.find_all("li", class_="job-result-card")
        if not job_listings:
            break

        for job in job_listings:
            title = job.find("h3", class_="base-search-card__title").text.strip()
            company = job.find("h4", class_="base-search-card__subtitle").text.strip()
            location = job.find("span", class_="job-search-card__location").text.strip()
            link = job.find("a", class_="base-card__full-link").get("href")

            jobs.append({
                "title": title,
                "company": company,
                "location": location,
                "link": link,
            })

        page += 1

    return jobs

def scrape_data(driver, job_url):
    driver.get(job_url)
    time.sleep(2)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    
    job_description = soup.find('div', class_='show-more-less-html__markup').text.strip()
    
    try:
        job_salary = soup.find("span", class_="salary-snippet").text.strip()
    except AttributeError:
        job_salary = np.nan
    
    return job_description, job_salary

def run_script(username, password, search_query, location, num_pages):
    # Log in to LinkedIn
    driver = login_to_linkedin(username, password)
    if not driver:
        print("Failed to log in. Exiting.")
        return

    # Scrape job listings
    jobs = scrape_jobs(driver, search_query, location, num_pages)

    # Scrape job descriptions and salary
    for job in jobs:
        job['description'], job['salary'] = scrape_data(driver, job['link'])

    # Display job details
    for job in jobs:
        print(f"Title: {job['title']}")
        print(f"Company: {job['company']}")
        print(f"Location: {job['location']}")
        print(f"Link: {job['link']}")
        print(f"Description: {job['description']}")
        print(f"Salary: {job['salary']}")
        print()

    # Quit the Selenium driver
    driver.quit()

# Run the script
if __name__ == "__main__":
    run_script('sports.sherwani@gmail.com', 'dataclinic', 'Sports Management' 'United States', 2)