from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from ChromeDriver import WebDriver
import subprocess
import time
import os


class JobScraper:
    def __init__(self):
        self.driver = None

    def start_driver(self):
        self.driver = WebDriver.start_driver(self)
        return self.driver

    def search(self):
        self.driver.get('https://www.workopolis.com/en')

        keyword_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'query-input'))
        )
        keyword_input.send_keys('python developer')

        find_jobs_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@type="submit" and @data-testid="findJobsSearchSubmit"]'))
        )
        find_jobs_button.click()

    def process_all_jobs_on_page(self):
        job_list = self.get_job_list()
        for job_url in job_list:
            self.open_job_application_page(job_url)
            self.input_things()
            self.close_extra_windows()

    def close_extra_windows(self):
        main_window_handle = self.driver.window_handles[0]
        for handle in self.driver.window_handles[1:]:
            self.driver.switch_to.window(handle)
            self.driver.close()
        self.driver.switch_to.window(main_window_handle)

    def get_job_list(self):
        job_list = []
        article_elements = self.driver.find_elements(By.CLASS_NAME, 'SerpJob')
        for article_element in article_elements:
            link_element = article_element.find_element(By.CLASS_NAME, 'SerpJob-titleLink')
            link_url = link_element.get_attribute('href')
            job_list.append(link_url)
        return job_list






if __name__ == "__main__":
    job_scraper = JobScraper()

    print('ATTACH YOUR RESUME IN SAME DIR WITH PROGRAM WITH NAME "Resume"')
    First_name = input("First Name: ")
    Last_name = input("Last Name: ")
    Phone_number = input("Phone Number: ")
    Email = input("Email: ")
    Job_Title = input('Enter the your JobTitle: ')

    job_scraper.start_driver()
    job_scraper.open_the_job()
