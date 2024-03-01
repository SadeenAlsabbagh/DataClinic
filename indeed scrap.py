from httpcore import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd

# Setup Chrome options for Selenium
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
# Uncomment the next line to run Chrome in headless mode
# options.add_argument('--headless')

# Initialize the Chrome WebDriver
driver = webdriver.Chrome(options=options)

# Setup explicit wait
wait = WebDriverWait(driver, 10)

jobs_data = []
max_pages = 5  # Set a maximum number of pages to scrape
page = 0

while page < max_pages:
    url = f"https://www.indeed.com/jobs?q=media+jobs&l=USA&start={page * 10}"
    driver.get(url)

    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.job_seen_beacon')))
    except TimeoutException:
        print("Timed out waiting for page to load")
        break

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    jobs = soup.findAll('div', class_='job_seen_beacon')

    if not jobs:
        print("No more jobs found.")
        break

    for job in jobs:
        data = {}
        try:
            data['Title'] = job.find('h2', class_='jobTitle').text.strip()
        except AttributeError:
            data['Title'] = "Not listed"

        try:
            data['Company'] = job.find('span', class_="css-92r8pb").text.strip()
        except AttributeError:
            data['Company'] = "Not listed"

        try:
            data['Location'] = job.find('div', class_='company_location').text.strip()
        except AttributeError:
            data['Location'] = "Not listed"

        skills_section = job.find('div', class_='jobsearch-SkillsWrapper')
        data['Skills'] = ', '.join([skill.text.strip() for skill in skills_section.find_all('span', class_='jobsearch-SkillTag')]) if skills_section else "Not listed"

        try:
            data['Salary'] = job.find('div', class_='css-1cvo3fd').text.strip()
        except AttributeError:
            data['Salary'] = "Not listed"

        try:
            jobDescriptionText = job.find('div', class_='jobsearch-jobDescriptionText')
            data['Description'] = jobDescriptionText.text.strip() if jobDescriptionText else "Not listed"
        except AttributeError:
            data['Description'] = "Not listed"

        try:
            job_link = job.find('a', class_='jcs-JobTitle')['href']
            data['Apply Link'] = 'https://www.indeed.com' + job_link
        except TypeError:
            data['Apply Link'] = "Not listed"

        jobs_data.append(data)

    print(f"Page {page + 1} completed.")
    page += 1

driver.quit()

df = pd.DataFrame(jobs_data)
df.to_csv('indeed_jobs.csv', index=False)
print("Job extraction complete. Data saved to 'indeed_jobs.csv'.")
