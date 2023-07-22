# **Leetcode Scraper**

This Leetcode Scraper is a Python script designed to extract the question description and the top 5 solutions for a Leetcode question based on its URL. It utilizes the Selenium WebDriver and BeautifulSoup libraries to navigate through the web page extract the relevant content, and store it in Markdown format for easy readability.

<br>

## Installation
<br>
<ul>
<li> Download the ChromeDriver executable that matches your Chrome browser version from the <a href = "https://sites.google.com/chromium.org/driver/">official website</a>.</li>
<li> Clone the repository</li>
<li> Install the requirements</li>
<pre> pip install -r requirements.txt</pre>
</ul>

<br>

## Usage
<br>
<pre>python main.py [-u]<br>
-u : URL to the question</pre>
<br>
<p>
The script will launch a Chrome browser window, navigate to the provided URL, and extract the question description along with the top 5 solutions. The extracted content will be stored in a directory named after the question title. </p><p>Inside this directory, you will find a <strong>README.md</strong> file containing the question description, and a <strong>Solutions.md</strong> file with the top 5 solutions.</p><p>The script downloads any images present in the question description and includes them in the <strong>README.md</strong> file for better visualization.</p><p>The default output directory for the scraped content is <strong>/Users/avaneeshdevkota/Desktop/repos/competitive-coding/</strong>. You can change this directory by modifying the default_dir variable in the script.</p>

<br>

## Note
<br>
<p>Working as of July 2023. The scraper may require occasional updates if the Leetcode website's structure or layout changes. Ensure that you are using the latest version of the script to avoid compatibility issues.</p><p>This script is intended for educational and personal use only. Use it responsibly and respect the website's terms of service. Automated scraping of websites may violate their policies, so please exercise caution while using this tool.</p>