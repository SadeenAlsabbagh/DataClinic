from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import os
import time

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

def search_jobs(driver):
        driver.get(f"https://www.linkedin.com/jobs/search/?keywords={'Sustainability'}&location={'United States'}")

def scroll_job_list(driver):
    job_list_container = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'jobs-search-results-list'))
    )

    last_height = driver.execute_script(
        "return arguments[0].scrollHeight", job_list_container
    )
    
    # Define the scroll increment (smaller value for slower scroll)
    scroll_increment = 100

    while True:
        # Scroll down by a small increment
        driver.execute_script(
            f"arguments[0].scrollTo(0, arguments[0].scrollTop + {scroll_increment});", job_list_container
        )
        
        # Wait a bit for the page to load
        time.sleep(1)  # Adjust the sleep time to control the scroll speed

        new_height = driver.execute_script(
            "return arguments[0].scrollHeight", job_list_container
        )
        
        # Check if we've reached the bottom of the job list container
        if driver.execute_script("return arguments[0].scrollTop + arguments[0].clientHeight", job_list_container) >= new_height:
            break

        # Update last_height if needed (may not be necessary with small increments)
        last_height = new_height


# Use this function in your scrape_jobs function to scroll within the job listing

def scrape_jobs(driver, max_pages=1):
    current_page = 1
    while current_page <= max_pages:
        scroll_job_list(driver)

        # Get the current page's source and create a BeautifulSoup object
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Find all job posting containers using the class name
        job_postings = soup.find_all('div', class_='job-card-container')
        
        # Extract job details
        for job in job_postings:
            # Extract the title and company name using the correct class names
            title_element = job.find('a', class_='job-card-list__title')
            title = title_element.get_text(strip=True) if title_element else 'No Title Found'
    
            company_element = job.find('span', class_='job-card-container__primary-description')
            company = company_element.get_text(strip=True) if company_element else 'No Company Found'

            location_element = job.find('li', class_='job-card-container__metadata-item')
            location = location_element.get_text(strip=True) if location_element else 'No Location Found'

            # The job link is typically within an 'a' tag's 'href' attribute
            job_link_element = job.find('a', class_='job-card-list__title')  # Assuming the class name for the 'a' tag is correct
            job_link = job_link_element['href'] if job_link_element and job_link_element.has_attr('href') else 'No Job Link Found'

            print(f"Title: {title}, Company: {company}, Location: {location}, Job Link: {job_link}")
            
        # Attempt to navigate to the next page
        try:
            pagination_controls = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'artdeco-pagination'))
            )
            next_page_buttons = pagination_controls.find_elements(By.TAG_NAME, 'button')
            next_page_button = next_page_buttons[current_page]  # current_page is zero-indexed
            next_page_button.click()
            current_page += 1
            time.sleep(2)  # Wait for the page to load
        except (NoSuchElementException, TimeoutException):
            print("Pagination controls not found on the page.")
            break
        except IndexError:
            print("No more pages to navigate to. Exiting loop.")
            break
        except Exception as e:
            print(f"An error occurred while trying to navigate pages: {e}")
            break

        time.sleep(2)

def main():
    driver = initialize_driver()
    try:
        login_to_linkedin(driver, 'princenoworkhere@gmail.com', 'DataClinic')
        search_jobs(driver)
        scrape_jobs(driver)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
