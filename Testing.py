from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import time
from bs4 import BeautifulSoup
import mysql.connector

def scrape_linkedin_jobs(email, password, search_term):
    driver = webdriver.Chrome()
    job_data = []
    try:
        driver.get("https://www.linkedin.com")
        username = driver.find_element(By.ID, "session_key")
        password_input = driver.find_element(By.ID, "session_password")
        username.send_keys(email)
        password_input.send_keys(password)
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
        driver.get("https://www.linkedin.com/jobs")
        search_box = driver.find_element(By.CLASS_NAME, "jobs-search-box__text-input")
        search_box.send_keys(search_term)
        search_box.send_keys(Keys.RETURN)
        time.sleep(10)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        job_postings = soup.find_all('div', class_='job-posting-class-or-id')

        for job in job_postings:
            title = job.find('h3', class_='title-class').get_text()
            company = job.find('h4', class_='company-class').get_text()
            posted_date = job.find('span', class_='posted-date-class').get_text()  
            location = job.find('span', class_='location-class').get_text()  
            job_link = job.find('a', class_='job-link-class')['href'] 
            job_data.append({"Title": title, "Company": company, "Posted Date": posted_date, "Location": location, "Job Link": job_link})
    finally:
        driver.quit()
    return pd.DataFrame(job_data)

def save_to_mysql(dataframe, db_config):
    connection = mysql.connector.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database']
    )
    cursor = connection.cursor()
    for _, row in dataframe.iterrows():
        sql = "INSERT INTO job_postings (title, company, posted_date, location, job_link) VALUES (%s, %s, %s, %s, %s)"
        values = (row['Title'], row['Company'], row['Posted Date'], row['Location'], row['Job Link'])
        cursor.execute(sql, values)
    connection.commit()
    cursor.close()
    connection.close()

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': 'jobs_scraped'
}
jobs = scrape_linkedin_jobs('princenoworkhere@gmail.com', 'DataClinic', 'Sustainability')
save_to_mysql(jobs, db_config)
