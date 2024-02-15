from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

# Set up the WebDriver
driver = webdriver.Chrome()

# Navigate to Google
driver.get("http://www.google.com")

# Find the search box and search for the query
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys("Prince Track and Field")
search_box.send_keys(Keys.RETURN)

# Wait for results to load
time.sleep(3)

# Extracting data from the top 5 search results
search_results = driver.find_elements(By.XPATH, '//div[@class="tF2Cxc"]')[:5]
for index, result in enumerate(search_results, start=1):
    title = result.find_element(By.XPATH, './/h3').text
    link = result.find_element(By.XPATH, './/a').get_attribute('href')
    snippet = result.find_element(By.XPATH, './/div[@class="IsZvec"]').text
    print(f"Result {index}:")
    print(f"Title: {title}")
    print(f"URL: {link}")
    print(f"Snippet: {snippet}")
    print("\n")

print(search_results)

# Close the WebDriver
driver.quit()
