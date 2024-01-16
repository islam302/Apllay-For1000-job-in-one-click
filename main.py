# -*- coding: utf-8 -*-
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from ChromeDriver import WebDriver  # Assuming the WebDriver class is defined in ChromeDriver module

class JobScraper:
    def __init__(self):
        self.driver = None

    def start_driver(self):
        self.driver = WebDriver.start_driver(self)
        return self.driver

    def search(self):
        search_keyword = input('INPUT YOUR JOB TITLE: ')
        self.start_driver()
        self.driver.get('https://www.jobillico.com/en')
        try:
            search_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'search-engine-keyword-job'))
            )
            search_input.clear()
            search_input.send_keys(search_keyword)
            search_input.send_keys(Keys.ENTER)
        except Exception as e:
            print(f"Error during search: {e}")

    def open_the_job(self):

        self.search()
        num_pages = 200
        for page in range(26, num_pages + 1):
            url = f'{self.driver.current_url}&ipg={page}'
            self.driver.get(url)
            job_urls = [job_url_element.get_attribute('href') for job_url_element in
                        self.driver.find_elements(By.CSS_SELECTOR, 'article[ref^="job"] h2 a')]

            for job_url in job_urls:
                self.driver.get(job_url)
                try:
                    if 'https://www.jobillico.com/' not in self.driver.current_url:
                        self.driver.back()
                except Exception as e:
                    print(f"Error during navigation: {e}")
                    continue
                try:
                    apply_button = self.driver.find_element(By.XPATH,
                                                            '//a[@class="green-btn button button--primary gtm--CTAApplyButton full-width center js-generateExternPostuABTestingKey"]')
                    apply_button.click()
                except Exception as e:
                    print(f"Error clicking apply button: {e}")
                    continue

                self.input_things()
                time.sleep(2)

        self.driver.quit()

    def input_things(self):
        current_directory = os.getcwd()
        file_name = input('YOUR RESUME (in the same folder): ')
        file_path = os.path.join(current_directory, file_name)
        try:
            cv_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'uploadBtn_externPostu'))
            )
            if cv_input:
                cv_input.send_keys(file_path)

            self.driver.implicitly_wait(5)
            self.driver.find_element(By.ID, 'nameInputExternPostu').send_keys('islam badran')
            self.driver.implicitly_wait(5)
            self.driver.find_element(By.ID, 'emailInputExternPostu').send_keys('islambadran39@gmail.com')

            submit_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="submitFormExternPostu"]'))
            )
            submit_button.click()

            self.driver.switch_to.window(self.driver.window_handles[-1])
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])

        except Exception as e:
            print(f"Error during input: {e}")


if __name__ == "__main__":
    job_scraper = JobScraper()
    job_scraper.open_the_job()
