# Jupyter Notebook Conversion to Python Script
#################################################

# Dependencies and Setup
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import datetime as dt

#################################################
# Mac
#################################################
# Set Executable Path & Initialize Chrome Browser
executable_path = {'executable_path': "/Users/moz/.wdm/drivers/chromedriver/mac64/91.0.4472.19/chromedriver"}
browser = Browser('chrome', **executable_path, headless=False)

 # Get First List Item & Wait Half a Second If Not Immediately Present
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=0.5)

#################################################
# NASA Mars News
#################################################
# NASA Mars News Site Web Scraper
def mars_news(browser):
    # Visit the NASA Mars News Site
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    
    
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # Parse Results HTML with BeautifulSoup
    # Find Everything Inside:
    #   <ul class="item_list">
    #     <li class="slide">
    try:
        location = soup.select_one("ul.item_list li.slide")
        location.find("div", class_="content_title")

        # Scrape the Latest News Title
        # Use Parent Element to Find First <a> Tag and Save it as news_title
        news_title = location.find("div", class_="content_title").get_text()

        news_p = location.find("div", class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None
    return news_title, news_p


#################################################
# JPL Mars Space Images - Featured Image
#################################################
# NASA JPL (Jet Propulsion Laboratory) Site Web Scraper
def featured_image(browser):
    # Visit the NASA JPL (Jet Propulsion Laboratory) Site
    url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(url)

    # Find "More Info" Button and Click It
    browser.is_element_present_by_text("FULL IMAGE", wait_time=1)
    more_info_element = browser.find_link_by_partial_text("FULL IMAGE")
    more_info_element.click()

    # Parse Results HTML with BeautifulSoup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    try:
        photo_full = soup.find('img', class_='headerimage fade-in')['src']
    except AttributeError:
        return None 
   # Use Base URL to Create Absolute URL
    photo_full_url = f"https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{photo_full}"
    return photo_full_url


#################################################
# Mars Facts
#################################################
# Mars Facts Web Scraper
# Visit the Mars Facts Site Using Pandas to Read
# Visit the Mars Facts Site Using Pandas to Read & Scrap data
url = 'https://space-facts.com/mars/'
tables = pd.read_html(url)
mars_facts = tables[0]
mars_facts = mars_facts.rename(columns={0: "Description", 1: "Value"})
mars_facts


#################################################
# Mars Hemispheres
#################################################
# Mars Hemispheres Web Scraper
def hemisphere(browser):
    # Visit the USGS Astrogeology Science Center Site
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    hemisphere_image_urls = []

    # Get a List of All the Hemisphere
    links = browser.find_by_css("a.product-item h3")
    for item in range(len(links)):
        hemisphere = {}
        
        # Find Element on Each Loop to Avoid a Stale Element Exception
        browser.find_by_css("a.product-item h3")[item].click()
        
        # Find Sample Image Anchor Tag & Extract <href>
        sample_element = browser.find_link_by_text("Sample").first
        hemisphere["img_url"] = sample_element["href"]
        
        # Get Hemisphere Title
        hemisphere["title"] = browser.find_by_css("h2.title").text
        
        # Append Hemisphere Object to List
        hemisphere_image_urls.append(hemisphere)
        
        # Navigate Backwards
        browser.back()
    return hemisphere_image_urls

# Helper Function
def scrape_hemisphere(html_text):
    hemisphere_soup = BeautifulSoup(html_text, "html.parser")
    try: 
        title_element = hemisphere_soup.find("h2", class_="title").get_text()
        sample_element = hemisphere_soup.find("a", text="Sample").get("href")
    except AttributeError:
        title_element = None
        sample_element = None 
    hemisphere = {
        "title": title_element,
        "img_url": sample_element
    }
    return hemisphere


#################################################
# Main Web Scraping Bot
#################################################
def scrape_all():
    executable_path = {'executable_path': "/Users/moz/.wdm/drivers/chromedriver/mac64/91.0.4472.19/chromedriver"}
    browser = Browser('chrome', **executable_path, headless=False)
    news_title, news_paragraph = mars_news(browser)
    img_url = featured_image(browser)
    facts = mars_facts
    hemisphere_image_urls = hemisphere(browser)
    timestamp = dt.datetime.now()

    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": img_url,
        "facts": facts,
        "hemispheres": hemisphere_image_urls,
        "last_modified": timestamp
    }
    browser.quit()
    return data 

if __name__ == "__main__":
    print(scrape_all())