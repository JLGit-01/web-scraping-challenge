from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


def init_browser():
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    mars_dictionary = {}

    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    step_one = soup.find('ul', class_='item_list')
    step_two = step_one.find('li', class_='slide')
    title = step_two.find('div', class_='content_title').text

    paragraph = step_two.find('div', class_='article_teaser_body').text

    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    step_one = soup.find('img', class_='headerimage fade-in')['src']
    feature_image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/'+step_one

    url = 'https://space-facts.com/mars/'
    browser.visit(url)

    marsfacts = pd.read_html(url)
    marsfacts_df = marsfacts[1]
    renamed_marsfacts_df = marsfacts_df.rename(columns={0:"Facts", 1:"Value"})
    renamed_mars_index=renamed_marsfacts_df.set_index('Mars - Earth Comparison')
    marsfacts_html=renamed_mars_index.to_html()


    url= 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    step_cerb= soup.find('div' , class_='downloads').find('a')['href']

    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'
    browser.visit(url)  

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    step_schi= soup.find('div' , class_='downloads').find('a')['href']

    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    step_syrt= soup.find('div' , class_='downloads').find('a')['href']

    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    step_vall= soup.find('div' , class_='downloads').find('a')['href']


    mars_dictionary["Title"] = title
    mars_dictionary["Paragraph"] = paragraph
    mars_dictionary["Feature"] = feature_image_url
    mars_dictionary["Table"] = marsfacts_html
    mars_dictionary["Cerb"] = step_cerb
    mars_dictionary["Schi"] = step_schi
    mars_dictionary["Syrt"] = step_syrt
    mars_dictionary["Vall"] = step_vall

    # Quit the browser
    browser.quit()

    return mars_dictionary
