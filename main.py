import shutil
from selenium.webdriver.common.by import By
import chromedriver_binary
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
import urllib
import time
from bs4 import BeautifulSoup, NavigableString
import os
import requests

class Driver:
    def __init__(self):
        self.driver: webdriver.Chrome = None
        self.reset()

    def reset(self):
        try:
            if self.driver:
                self.driver.close()
            self.start()
            time.sleep(3)
        except Exception:
            self.reset()

    def start(self):
        try:
            chrome_options = Options()
            # chrome_options.add_argument('--headless')
            # chrome_options.add_argument('--no-sandbox')
            # chrome_options.add_argument('--disable-dev-shm-usage')
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.maximize_window()
            print("Started Instance")
        except Exception as e:
            print("Could not start instance...trying again")
            print(e)
            time.sleep(5)
            return self.start()

    def download(self, url):
        md = \
'''
## {title}     

`{difficulty}`

{description}

---

### Examples

{examples}

**Constraints**

{constraints}
'''
        # try:
        self.driver.get(url)
        time.sleep(5)
        title = self.driver.find_element(By.CSS_SELECTOR, 'div[data-cy="question-title"]').text
        difficulty = self.driver.find_element(By.CSS_SELECTOR, 'div[diff]').text
        content = self.driver.find_element(By.CSS_SELECTOR, 'div[class*="question-content"]').get_attribute('innerHTML')
        soup = BeautifulSoup(str(content), 'lxml').div

        os.mkdir(title)
        os.chdir(title)

        description = ''
        examples = ''
        constraints = ''
        follow_up = ''

        current = 'description'

        images = []
        filename = ''

        for img in soup.find_all('img'):
            images.append(img.get('src'))

        for i in images:
            filename = i.rsplit('/')[-1]
            res = requests.get(i, stream = True)

            if res.status_code == 200:
                with open(filename, 'wb') as f:
                    shutil.copyfileobj(res.raw, f)

            examples = examples + f'\n![]({filename})\n'

        for item in soup:

            if (isinstance(item, NavigableString) and item.text != ' '):
                continue

            if current == 'description' and item.name == 'p':

                if item.text.strip() == '':
                    current = 'examples'
                    continue
                else:
                    description = description + item.decode_contents()

            elif len(item.text) < 15 and (item.text.startswith('Example') or item.text.strip() == ""):
                continue

            # elif item.find('img') != None:
            #     src = item.img.get('src')
            #     filename = src.rsplit('/')[-1]
            #     res = requests.get(src, stream = True)
                
            #     if res.status_code == 200:
            #         with open(filename, 'wb') as f:
            #             shutil.copyfileobj(res.raw, f)
                
            #     examples += f'\n![]({filename})\n'

            elif current == 'examples' and item.name == 'pre':

                examples = examples + str(item)

            elif item.name == 'ul':

                constraints = constraints + str(item)

        md = md.format(title=title, difficulty= difficulty, examples=examples, constraints=constraints, description=description)

        f = open("README.md", "w")
        f.write(md)
        f.close()

        os.chdir('../')

        # # except Exception as e:
        # #     print(f"{e} Error processing {url}")
        # #     return self.download(url)
        #     # self.data.append([url, 'sjb8193', 'N', ' ', ' ', ' ', 'Y'])

if __name__ == "__main__":

    input_file = "problems.txt"
    with open(input_file, 'r', encoding="utf-8") as f:
        urls = [x.strip() for x in f.readlines()]

    d = Driver()
    # for i, url in enumerate(urls):
    #     d.download(f'https://leetcode.com{url}')

    d.download('https://leetcode.com/problems/add-two-numbers/')
