from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup, NavigableString
import time
import requests
import shutil
import os
import argparse

# Create an argument parser to handle command-line arguments

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--URL", help="Input URL")
default_dir = "/Users/avaneeshdevkota/Desktop/repos/competitive-coding/"

args = parser.parse_args()

class Driver:

    def __init__(self):

        # Set up Chrome options and create a WebDriver instance

        self.chromeOptions = webdriver.ChromeOptions()
        self.chromeOptions.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        self.driver = webdriver.Chrome(options=self.chromeOptions)

    def extract(self):

        # Navigate to the given URL

        self.driver.get(args.URL)
        time.sleep(5)
        
        # Extract title and difficulty of the question

        self.title = self.driver.find_element(By.XPATH, '//span[@class="mr-2 text-label-1 dark:text-dark-label-1 text-lg font-medium"]').text
        self.difficulty = self.driver.find_element(By.XPATH, '//div[@class="mt-3 flex items-center space-x-4"]//div').text
        
        # Find all images on the page and download them

        self.images = self.driver.find_elements(By.XPATH, '//div[@class="_1l1MA"]//img')
        self.image_files = []

        for img in self.images:
            i = img.get_attribute('src')
            fname = i.split('/')[-1]
            res = requests.get(i, stream=True)

            if res.status_code == 200:
                with open(fname, 'wb') as f:
                    shutil.copyfileobj(res.raw, f)
            self.image_files.append(f'\n![]({fname})\n')
        
        content = self.driver.find_element(By.XPATH, '//div[@class="_1l1MA"]').get_attribute('innerHTML')
        self.soup = BeautifulSoup(content, 'html.parser')

    def getQuestion(self, dir=default_dir):

        # Prepare the Markdown template for the question

        md = \
'''
## {title}     

`{difficulty}`

{description}
'''
        self.description = ''
        img_counter = 0

        for item in self.soup:
            if isinstance(item, NavigableString):
                if len(item) > 1:
                    self.description += item
                else:
                    self.description += "\n"
                continue
            if item.name == 'img':
                self.description += self.image_files[img_counter]
                img_counter += 1
            else:
                self.description += item.prettify()

        md = md.format(title=self.title, difficulty=self.difficulty, description=self.description)

        # Change the current working directory to the default directory

        os.chdir(dir)

        # Create a directory for the question if it doesn't exist

        if not os.path.exists(self.title):
            os.mkdir(self.title)

        # Change the current working directory to the question directory

        os.chdir(self.title)

        # Write the extracted question to a README.md file

        f = open("README.md", "w")
        f.write(md)
        f.close()

    def getSolutions(self):

        # Navigate to the solutions page

        self.driver.get(args.URL + "/solutions/")
        time.sleep(5)
        
        # Open the dropdown to display the most upvoted solutions

        self.driver.find_element(By.XPATH, '//div[@class="relative"]').click()
        time.sleep(3)
        self.driver.find_elements(By.XPATH, '//div[@class="max-w-[240px] min-w-[140px] absolute z-dropdown mt-1 rounded-lg p-2 overflow-auto focus:outline-none shadow-level2 dark:shadow-dark-level2 bg-overlay-3 dark:bg-dark-overlay-3 transform opacity-100 scale-100"]//div')[-1].click()
        time.sleep(2)

        # Get the list of the top 5 solutions

        self.solutions = self.driver.find_elements(By.XPATH, '//div[@class="hover:bg-fill-4 dark:hover:bg-dark-fill-4 relative flex w-full cursor-pointer gap-4 px-4 py-4"][position()<=5]')

        # Write the solutions to a Solutions.md file

        f = open("Solutions.md", "w")

        for i, sol in enumerate(self.solutions):

            sol.click()
            time.sleep(3)

            f.write(f"# - - - - - Solution {i + 1} - - - - -\n\n")

            content = self.driver.find_element(By.XPATH, '//div[@class="_16yfq _39fEV"]').get_attribute('innerHTML')
            f.write(content + "\n\n")

            self.driver.find_element(By.XPATH, '//button[@class="group flex h-5 w-5 cursor-pointer items-center justify-start gap-4 overflow-hidden"]').click()
        
        f.close()

d = Driver()
d.extract()
d.getQuestion()
d.getSolutions()