from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re
from datetime import date, timedelta
from selenium.webdriver.common.by import By
import pandas as pd

driver = webdriver.Chrome()

def fetch_all_jobs(job,location):

    email=driver.find_element_by_xpath("//input[@class='input__input'][@name='session_key']")
    passw=driver.find_element_by_xpath("//input[@class='input__input'][@name='session_password']")
    sign_button=driver.find_element_by_xpath("//button[@class='sign-in-form__submit-button']")

    mail='upadhyayps@beloit.edu'
    passowrd='@Password'

    email.send_keys(mail)
    passw.send_keys(passowrd)
    sign_button.click()
    time.sleep(2)

    jobs_icon=sign_button=driver.find_element_by_xpath("//a[@href='https://www.linkedin.com/jobs/?']")
    jobs_icon.click()

    job_seach_bar=driver.find_element_by_xpath("//div[@id='global-nav-search']")
    job_seach_bar.click()
    time.sleep(2)

    job_name=driver.find_element_by_xpath("//input[@class='jobs-search-box__text-input jobs-search-box__keyboard-text-input']")  
    job_name.send_keys(job)
    time.sleep(2)
    
    job_location=driver.find_element_by_xpath("//input[@class='jobs-search-box__text-input']")
    job_location.send_keys(location)
    job_name.send_keys(Keys.ENTER)
    time.sleep(2)
    
    get_current_page_jobs()

    return all_jobs

def get_current_page_jobs():
    current_page_url = driver.current_url
    c=1
    while True:
        
        number_of_elements_found = 0
        while True:
            els = driver.find_elements(By.CSS_SELECTOR, '.job-card-list__insight')
            if number_of_elements_found == len(els):
                # Reached the end of loadable elements
                break

            try:
                driver.execute_script("arguments[0].scrollIntoView();", els[-1])
                time.sleep(2)
                number_of_elements_found = len(els)

            except StaleElementReferenceException:
                # Possible to get a StaleElementReferenceException. Ignore it and retry.
                pass
        jobs_links=[]
        jobs=driver.find_elements_by_xpath("//div[@class='full-width artdeco-entity-lockup__title ember-view']/a[@href]")
        for l in jobs:
            jobs_links.append(l.get_attribute('href'))
        get_each_job_info(jobs_links) 
        print('*'*100)
        print(f'page {c} completed')
        
        driver.get(current_page_url)
        time.sleep(2)
        try:
            c +=1
            des='Page '+str(c)
            dest=f"//button[@aria-label='{des}']"
            next_page_button=driver.find_element_by_xpath(dest)
            next_page_button.click()
            time.sleep(2)
            current_page_url=driver.current_url
        except:
            break
def get_each_job_info(jobs):
    for j in jobs:
        driver.get(j)
        content=driver.page_source
        soup=BeautifulSoup(content,'html.parser')
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)") 
        
        ####data###
        
        try:
            title=soup.find('h1',class_='t-24 t-bold jobs-unified-top-card__job-title').text
        except:
            title=""
        try:
            company_name=soup.find('span',class_='jobs-unified-top-card__company-name').text.strip()
        except:
            company_name=""
        try:
            location=soup.find('span',class_='jobs-unified-top-card__bullet').text.strip()
        except:
            location=""
        try:
            work_type=soup.find('span',class_='jobs-unified-top-card__workplace-type').text.strip()
        except:
            work_type=""
        try:
            job_type_2=soup.find('div',class_='mt5 mb2').find('li',class_='jobs-unified-top-card__job-insight').find('span').text.strip()
        except:
            job_type_2=""
        try:
            d=soup.find('span',class_='jobs-unified-top-card__posted-date').text.strip()
            #print(d)
            d=re.search('\d',d).group()
            job_posted_date=date.today()-timedelta(int(d))          
        except:
            job_posted_date='No longer Available'
        #print(str(job_posted_date))
        try:
            pay_range=driver.find_element_by_xpath("//p[@class='t-16']").text
         #   pay_range=driver.find_element_by_xpath("//h2[@class='t-16 pt4 ph5']").text
        except:
            pay_range="unavailable"

        #print(pay_range)
        link_of_job =j
        job={
            'job_posted_date':job_posted_date,
            'title':title,
            'location':location,
            'company name':company_name,
            'work type':work_type,
          #  'job type 2':job_type_2,
            'scraping date':date.today(),
            'pay range':pay_range,
            'job_link':link_of_job
            
        }
        all_jobs.append(job)
        print("job link",j)
    return

url='https://www.linkedin.com'
job='Data Scientist'
location='egypt'
all_jobs=[]
driver.get(url)
all_jobs=fetch_all_jobs(job,location)