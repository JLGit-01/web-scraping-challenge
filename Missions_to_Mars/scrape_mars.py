from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager


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
    step_one=soup.find('img' , class_='headerimage fade-in')['src']
    feature_image_url= 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/'+step_one


    url= 'https://space-facts.com/mars/'
    browser.visit(url)
    
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    step_graph= soup.find('table', class_='tablepress tablepress-id-p-mars')


    mars_dictionary["Title"] = title
    mars_dictionary["Paragraph"] = paragraph
    mars_dictionary["Feature Image"] = feature_image_url
    mars_dictionary["Mars Info"] = step_graph


    # Quit the browser
    browser.quit()

    return mars_dictionary
