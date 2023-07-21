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

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--URL", help = "Input URL")
default_dir = "/Users/avaneeshdevkota/Desktop/repos/competitive-coding"

args = parser.parse_args()

class Driver:

    def __init__(self):

        self.chromeOptions = webdriver.ChromeOptions()
        self.chromeOptions.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        self.driver = webdriver.Chrome(options = self.chromeOptions)

    def extract(self, url = args.URL):

        self.driver.get(url)
        time.sleep(5)
        self.title = self.driver.find_element(By.XPATH, '//span[@class="mr-2 text-label-1 dark:text-dark-label-1 text-lg font-medium"]').text
        self.difficulty = self.driver.find_element(By.XPATH, '//div[@class="mt-3 flex items-center space-x-4"]//div').text
        self.images = self.driver.find_elements(By.XPATH, '//div[@class="_1l1MA"]//img')

        self.image_files = []

        for img in self.images:

            i = img.get_attribute('src')
            fname = i.split('/')[-1]
            res = requests.get(i, stream = True)

            if (res.status_code == 200):
                with open(fname, 'wb') as f:
                    shutil.copyfileobj(res.raw, f)
                    
            self.image_files.append(f'\n![]({fname})\n')

        content = self.driver.find_element(By.XPATH, '//div[@class="_1l1MA"]').get_attribute('innerHTML')
        self.soup = BeautifulSoup(content, 'html.parser')
    
    def download(self, dir = default_dir):

        if dir == None:
            dir = default_dir

        md = \
'''
## {title}     

`{difficulty}`

{description}
'''

        self.description = ''
        img_counter = 0

        for item in self.soup:

            if (isinstance(item, NavigableString)):

                if (len(item) > 1):
                    self.description += item
                else:
                    self.description += "\n"
                continue

            if (item.name == 'img'):

                self.description += self.image_files[img_counter]
                img_counter += 1
            
            else :

                self.description += item.prettify()

        md = md.format(title = self.title, difficulty = self.difficulty, description = self.description)

        os.chdir(dir)

        if not os.path.exists(self.title):
            os.mkdir(self.title)

        os.chdir(self.title)

        print(self.title)

        f = open("README.md", "w")
        f.write(md)
        f.close()

        os.chdir('../')

d = Driver()
d.extract()
d.download()