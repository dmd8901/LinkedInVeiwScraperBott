import argparse
import time
import os
import random
from selenium import webdriver
from parsel import Selector
import csv
import pandas as pd
from selenium.webdriver.firefox.options import Options

def args_parser():

    # Passing the email and password as arguments into the command line
    parser = argparse.ArgumentParser()
    parser.add_argument("email", help="linkedin email")
    parser.add_argument("password", help="linked password")
    args = parser.parse_args


def validate_field(field):

    # if field is present pass if field:
    if field:
        pass
    # if field is not present print text else:
    else:
        field = 'No results'
    return field


def view_bot(browser):

        # The "pandas" package import the excel file and then creates a basic url list in python.
        df = pd.read_excel(r'C:\Users\Owner\PycharmProjects\LinkedInVeiwBot\URLS.xlsx')
        url_list = df["URLS"].tolist()
        # This guy suppose to open an excel.csv file and activate write mode:'w'
        writer = csv.writer(open('Linkedinfile.csv', 'w', encoding='utf-8'))
        # writerow() method to the write to the file object
        writer.writerow(['Name', 'Job Title', 'Company', 'Last jobs', 'College', 'Location', 'URL'])
        for url in url_list:

            # sleep to make sure everything loads, add random to make us look human.

            browser.get(url)
            time.sleep(random.randint(5, 10))
            # assigning the source code for the web page to variable sel
            sel = Selector(text=browser.page_source)

            # Find the button 'view more'
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            try:
                element = browser.find_element_by_xpath('//section[@id="experience-section"]/div/button')
                button_text = element.text
                while button_text != "Show fewer experiences":
                    browser.execute_script("return arguments[0].scrollIntoView();", element)
                    browser.execute_script("window.scrollBy(0,-200);")
                    time.sleep(2)
                    element.click()
                    time.sleep(2)
                    element = browser.find_element_by_xpath('//section[@id="experience-section"]/div/button')
                    button_text = element.text
            except:
                print("No button found")
            else:
                pass

            # xpath to extract the text from the class containing the name
            name = sel.xpath('//*[starts-with(@class, "pv-top-card-section__name")]/text()').extract_first()

            # if name exists
            if name:
                # .strip() will remove the new line /n and white spaces
                name = name.strip()

            # xpath to extract the text from the class containing the job title
            job_title = sel.xpath('//*[starts-with(@class, "pv-top-card-section__headline")]/text()').extract_first()

            if job_title:
                job_title = job_title.strip()

            # xpath to extract the text from the class containing the company
            company = sel.xpath('//*[starts-with(@class,"pv-entity__secondary-title")]/text()').extract_first()

            if company:
                company = company.strip()

            # Trying to get the entire list of job secondary job titles.
            last_positions_array = \
                browser.find_elements_by_xpath('//a[@data-control-name = "background_details_company"]/div/h3')
            last_jobs_array = browser.find_elements_by_xpath('//span[@class = "pv-entity__secondary-title"]')
            last_jobs = ''
            for index, job in enumerate(last_jobs_array):
                last_jobs += last_positions_array[index].text + ' at '
                last_jobs += job.text
                last_jobs += ' || '
            last_jobs = last_jobs[:-2]
            # xpath to extract the text from the class containing the college
            college = sel.xpath('//*[starts-with(@class, "pv-entity__school-name t-16 t-black t-bold")]/text()').extract_first()

            if college:
                college = college.strip()

            # xpath to extract the text from the class containing the location
            location = sel.xpath('//*[starts-with(@class, "pv-top-card-section__location")]/text()').extract_first()

            if location:
                location = location.strip()

            # assignment of the current URL
            linkedin_url = browser.current_url

            # validating if the fields exist on the profile
            name = validate_field(name)
            job_title = validate_field(job_title)
            company = validate_field(company)
            college = validate_field(college)
            location = validate_field(location)
            linkedin_url = validate_field(linkedin_url)

            # printing the output to the terminal
            print('\n')
            print('Name: ' + name)
            print('Job Title: ' + job_title)
            print('Company: ' + company)
            print('Previous Jobs: ' + last_jobs)
            print('College: ' + college)
            print('Location: ' + location)
            print('URL: ' + linkedin_url)
            print('\n')

            # This guy writes all the params below into csv file.
            writer.writerow([name, job_title, company, last_jobs, college, location, linkedin_url])


def main():

    # command-line args.
    args_parser()
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options)
    print('Activating: Headless mode on')
    browser.get("https://linkedin.com/uas/login")
    email_element = browser.find_element_by_id("username")
    email_element.send_keys("email")
    pass_element = browser.find_element_by_id("password")
    pass_element.send_keys("password")
    pass_element.submit()
    print('\n')
    print("Login Success!")
    print('\n')
    time.sleep(3)
    print('\n')
    print("Fetching links")

    os.system('cls')
    view_bot(browser)
    browser.close()


if __name__ == '__main__':
        main()
