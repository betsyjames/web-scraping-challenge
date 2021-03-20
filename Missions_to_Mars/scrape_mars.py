from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

def scrape():

    browser = init_browser()

    #Mars News
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(2)
    # latest News Title and Paragraph Text. Assign the text to variables that you can reference later
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    article = soup.find("div", class_='list_text')
    news_title = article.find("div", class_="content_title").text
    #print(news_title)
    # latest News Title and Paragraph Text.
    news_p = article.find("div", class_ ="article_teaser_body").text
    #print(news_p)


    #Featured Image
    jpl_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(jpl_url)
    time.sleep(2)
    jpl_html = browser.html
    jpl_soup = BeautifulSoup(jpl_html, 'html.parser')

    image = jpl_soup.find("div", class_="header")
    full_image = image.find("img", class_="headerimage")["src"]
    featured_image_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/" + full_image
    print(featured_image_url)

    #Mars Facts
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    mars_facts_df = tables[0]
    mars_facts_df.columns = ['Facts', 'Values']
    html_table = mars_facts_df.to_html(index=False)

    #Mars Images
    mars_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_url)
    time.sleep(2)
    mars_html = browser.html
    mars_soup = BeautifulSoup(mars_html, 'html.parser')

    hemisphere_image_urls = []

    for i in range(1,5):
        hemisphere = {}
        xpath = f'//*[@id="product-section"]/div[2]/div[{i}]/a/img'
        results = browser.find_by_xpath(xpath)
        img = results[0]
        img.click()
        mars_html = browser.html
        mars_soup = BeautifulSoup(mars_html, 'html.parser')
        div_url =  mars_soup.find("div", class_="wide-image-wrapper")
        hemisphere["img_url"] = div_url.find("a")["href"]
        hemisphere["title"] = mars_soup.find("h2", class_="title").text
        hemisphere_image_urls.append(hemisphere)
        browser.back()


    # Store data in a dictionary
    mars_data = {
        "newstitle": news_title,
        "newsp": news_p,
        "fea_image" :featured_image_url,
        "mars_table": html_table,
        "hemisphere" :hemisphere_image_urls
    }

     # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data