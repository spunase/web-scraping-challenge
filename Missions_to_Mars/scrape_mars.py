from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import pymongo
import time
# DB Setup

# client = pymongo.MongoClient('mongodb://localhost:27017')
# db = client.mars_db
# collection = db.mars

def init_browser():
   # @NOTE: Replace the path with your actual path to the chromedriver
   executable_path = {"executable_path": 'chromedriver.exe'}
   return Browser("chrome", **executable_path, headless=False)

def scrape():
   browser = init_browser()
   # collection.drop()
    
   #mars news title and paragraph  
   news_url = "https://mars.nasa.gov/news/"
   browser.visit(news_url)
   time.sleep(5)
   html = browser.html
   soup = BeautifulSoup(html, "html.parser")
   article = soup.find("div", class_='list_text')
   news_title = article.find("div", class_="content_title").text
   news_p = article.find("div", class_="article_teaser_body").text
    

   # JPL Mars Space Images - Featured Image

   image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
   browser.visit(image_url)
   time.sleep(5)
   html = browser.html
   soup = BeautifulSoup(html, "html.parser")
   image = soup.find("div", class_="img")
   featured_image = image.find("img", class_="thumb")["src"]
   featured_image_url = "https://www.jpl.nasa.gov" + featured_image
       
   # Mars weather 

   weather_url = "https://twitter.com/marswxreport?lang=en"
   browser.visit(weather_url)
   time.sleep(5)
   html = browser.html
   weather_soup = BeautifulSoup(html, "html.parser")
   weather = weather_soup.find("div", class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0")
   mars_weather = weather.find("span", class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0").text
    
   # Mars Fact Table
   fact_url = "https://space-facts.com/mars/"
   tables = pd.read_html(fact_url)
   mars_df = tables[0]
   mars_df.columns = ["Facts", "Value"]
   mars_facts = mars_df.to_html(index = True, header =True)
    
   #Mars hemisphere image url
   hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
   browser.visit(hemispheres_url)
   time.sleep(5)
   html = browser.html
   soup = BeautifulSoup(html, "html.parser")
   items = soup.find_all('div', class_='item')
   hemisphere_image_urls = []
   hemispheres_main_url = 'https://astrogeology.usgs.gov'
   for item in items:
      hemisphere_dict = {}

      # Store title
      title = item.find('h3').text
      # Store link that leads to full image website
      individual_img_url = item.find('a', class_='itemLink product-item')['href']
      # Visit the link that contains the full image website 
      browser.visit(hemispheres_main_url + individual_img_url)
      # HTML Object of individual hemisphere information website 
      individual_img_html = browser.html
      
      # Parse HTML with Beautiful Soup for every individual hemisphere information website 
      soup = BeautifulSoup( individual_img_html, 'html.parser')
      # Retrieve full image source 
      img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
      # Append the retreived information into a list of dictionaries
      hemisphere_dict['title']= title
      hemisphere_dict['image_url']= img_url
      hemisphere_image_urls.append(hemisphere_dict) 

   # Close the browser after scraping
   browser.quit()
   mars_data = {}
   # Return results
   mars_data = {
      'news_title' : news_title,
      'news_p': news_p, 
      'Featured_image': featured_image_url, 
      'Weather': mars_weather, 
      'Facts': mars_facts, 
      'Hemisphere_image': hemisphere_image_urls
   }
   # print(mars_data)
   # collection.insert_many(mars_data)
   return mars_data  