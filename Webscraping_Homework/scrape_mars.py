from bs4 import BeautifulSoup
import requests
from splinter import Browser
import time
import pandas as pd

def start_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = start_browser()
    mars_dict = {}
    
    # NASA Mars News
    nasa_url = 'https://mars.nasa.gov/news/'
    response = requests.get(nasa_url)
    nasa_soup = BeautifulSoup(response.text)
    news_title = nasa_soup.find('div', class_='content_title').a.text.strip()
    news_p = nasa_soup.find('div', class_="rollover_description_inner").text.strip()
    mars_dict = {
        'title': news_title,
        'article': news_p
        }
    
    # JPL Mars Space Images - Featured Image
    url = 'https://www.jpl.nasa.gov/spaceimages/index.php?category=Mars'
    browser.visit(url)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(3)
    browser.click_link_by_partial_text('more info')
    image_html = browser.html
    image_soup = BeautifulSoup(image_html, 'lxml')
    featured_image_url = 'https://www.jpl.nasa.gov' + image_soup.find('figure', class_='lede').a['href']
    mars_dict['image_url'] = featured_image_url

    # Mars Weather
    twitter_url = 'https://twitter.com/marswxreport'
    twitter_response = requests.get(twitter_url)
    twitter_soup = BeautifulSoup(twitter_response.text)

    mars_weather = twitter_soup.find('p', class_='tweet-text').contents[0]
    mars_dict['mars_weather'] = mars_weather

    # Mars Facts
    marsfacts_url = 'https://space-facts.com/mars/'
    table = pd.read_html(marsfacts_url, index_col=0)[0]
    table_html = table.to_html(header=False)
    mars_dict['html_table'] = table_html

    # Mars Hemispheres
    maps_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(maps_url)
    hemisphere_links = browser.find_link_by_partial_text('Hemisphere')
    hemisphere_image_urls = []
    for link in range(len(hemisphere_links)):
        browser.find_link_by_partial_text('Hemisphere')[link].click()
        img_url=browser.find_link_by_partial_text('Sample')['href']
        title = browser.find_by_tag('h2').text
        hemisphere_image_urls.append(
            {'title': title,
            'img_url': img_url
        })
        browser.back()
    browser.quit()
    mars_dict['hemisphere_image_urls'] = hemisphere_image_urls

    return mars_dict

