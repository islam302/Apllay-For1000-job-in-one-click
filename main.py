# -*- coding: utf-8 -*-
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException
from ChromeDriver import WebDriver  # Assuming the WebDriver class is defined in ChromeDriver module
import pandas as pd


class JobScraper:
    def __init__(self):
        self.driver = None

    def start_driver(self):
        self.driver = WebDriver.start_driver(self)
        return self.driver

    # def login(self):
    #     self.driver.find_element(By.ID, 'gtm--CTALogin').click()
    #     self.driver.find_element(By.ID, 'checkDeletedCandidateLogin').send_keys('khadijahammoumi14@gmail.com')
    #     self.driver.find_element(By.ID, 'validatePasswordField').send_keys('0045&Lwalida9999')
    #
    #     WebDriverWait(self.driver, 10).until(
    #         EC.element_to_be_clickable((By.XPATH, '//input[@type="submit" and @value=" Sign in " and @class="button button--primary register-btn ctrl-form-validate-popup-auth"]'))
    #     ).click()

    def open_the_job(self, num_pages=200):
        self.start_driver()

        for page in range(26, num_pages + 1):
            url = f'https://www.jobillico.com/search-jobs?skwd=%C3%A9ducatrice%20de%20petite%20enfance&icty=0&ipc=0&flat=0&flng=0&mfil=40&imc1=0&imc2=0&imc3=0&imc4=0&isj=0&sort=pert&type=0&ichan=1&ipg={page}'
            self.driver.get(url)
            job_urls = [job_url_element.get_attribute('href') for job_url_element in
                        self.driver.find_elements(By.CSS_SELECTOR, 'article[ref^="job"] h2 a')]

            for job_url in job_urls:
                self.driver.get(job_url)
                try:
                    if 'https://www.jobillico.com/' not in self.driver.current_url:
                        self.driver.back()
                except:
                    continue
                try:
                    apply_button = self.driver.find_element(By.XPATH, '//a[@class="green-btn button button--primary gtm--CTAApplyButton full-width center js-generateExternPostuABTestingKey"]')
                    apply_button.click()
                except:
                    continue

                self.input_things()
                time.sleep(2)

        self.driver.quit()

    def input_things(self):
        current_directory = os.getcwd()
        file_name = 'Khadija_Hammoumi.pdf'
        file_path = os.path.join(current_directory, file_name)
        try:
            cv_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'uploadBtn_externPostu'))
            )
            if cv_input:
                cv_input.send_keys(file_path)

            self.driver.implicitly_wait(5)
            self.driver.find_element(By.ID, 'nameInputExternPostu').send_keys('Khadija Hammoumi')
            self.driver.implicitly_wait(5)
            self.driver.find_element(By.ID, 'emailInputExternPostu').send_keys('khadijahammoumi14@gmail.com')

            submit_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="submitFormExternPostu"]'))
            )
            submit_button.click()

            self.driver.switch_to.window(self.driver.window_handles[-1])
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])

        except Exception as e:
            pass


if __name__ == "__main__":
    job_scraper = JobScraper()
    job_scraper.open_the_job()
