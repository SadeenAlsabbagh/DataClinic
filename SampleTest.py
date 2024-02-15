from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

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

    time.sleep(10)

finally:
    # Close the browser
    driver.quit()


