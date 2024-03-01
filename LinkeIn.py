from httpcore import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd

def init_driver(headless=False):
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    if headless:
        options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
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

def get_job_data(soup):
    jobs = soup.findAll('div', class_='job-card-container')
    job_list = []

    for job in jobs:
        data = {}
        data['Title'] = job.find('a', class_='job-card-list__title').text.strip() if job.find('a', class_='job-card-list__title') else "Not listed"
        data['Company'] = job.find('job-card-container__primary-description').text.strip() if job.find('job-card-container__primary-description') else "Not listed"
        data['Location'] = job.find('li', class_='job-card-container__metadata-item').text.strip() if job.find('li', class_='job-card-container__metadata-item') else "Not listed"
        job_link = job.find('a', class_='jcs-JobTitle')
        data['Apply Link'] = 'https://www.linkedin.com' + job_link['href'] if job_link else "Not listed"
        job_list.append(data)

    return job_list

def scrape_linkedin_jobs(max_pages=5):
    driver = init_driver()
    wait = WebDriverWait(driver, 10)
    jobs_data = []

    for page in range(max_pages):
        url =  f"https://www.linkedin.com/jobs/search/?keywords=software%20engineer&start={page * 25}"
        driver.get(url)

        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.job-card-container')))
        except TimeoutException:
            print("Timed out waiting for page to load")
            break

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        jobs_data.extend(get_job_data(soup))
        print(f"Page {page + 1} completed.")

    driver.quit()
    return jobs_data

def main():
    driver = init_driver(headless=False)
    login_to_linkedin(driver, 'princenoworkhere@gmail.com', 'DataClinic')
    search_jobs(driver, "Sustainability")
    jobs_data = scrape_linkedin_jobs()
    df = pd.DataFrame(jobs_data)
    df.to_csv('linkedin_jobs.csv', index=False)
    print("Job extraction complete. Data saved to 'linkedin_jobs.csv'.")

if __name__ == "__main__":
    main()
