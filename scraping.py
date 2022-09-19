
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    #"headless" browsing session is when a browser is run without the users seeing it at all.

    news_title, news_paragraph = mars_news(browser) #This line of code tells Python that we'll be using our mars_news function to pull this data.

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemispheres(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    
    return data
    
    # ### News Scraping
def mars_news(browser):
    '''
    "browser" tells Python that we'll be using the browser variable we defined outside the function. 
    All of our scraping code utilizes an automated browser, and without this section, our function wouldn't work.
    '''

    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    '''
    With the following line, browser.is_element_present_by_css('div.list_text', wait_time=1), we are accomplishing two things.

    One is that we're searching for elements with a specific combination of tag (div) and attribute (list_text). 
    As an example, ul.item_list would be found in HTML as <ul class="item_list">.

    Secondly, we're also telling our browser to wait one second before searching for components. 
    The optional delay is useful because sometimes dynamic pages take a little while to load, especially if they are image-heavy.
    '''


    html = browser.html

    try:
        news_soup = soup(html, 'html.parser')
        slide_elem = news_soup.select_one('div.list_text')



        #slide_elem.find('div', class_='content_title')


        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        news_title

        '''
        .find() is used when we want only the first class and attribute we've specified.
        .find_all() is used when we want to retrieve all of the tags and attributes.

        '''


        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:    
        return None, None

    return news_title, news_p

# ### Image Scraping

def featured_image(browser):
# Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)


    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()


    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Find the relative image url
    try:
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        img_url_rel
    
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    
    return img_url


# ### Facts Scraping

def mars_facts():

    try:
        # use 'read_html" to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    
    except BaseException:    
        return None

    # Assign columns and set index of dataframe
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    
     # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

def hemispheres(browser):
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # 2. Create a list to hold the images and titles. #wide-image
    hemisphere_image_urls = []
    html = browser.html
    link_soup = soup(html, 'html.parser')

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    links = link_soup.find_all('a', class_="itemLink product-item")

    link_url = []
    title_lst = []

    links[0] = links[0].get('href')
    fst_link_url = f'https://marshemispheres.com/{links[0]}'
    browser.visit(fst_link_url)

    html0 = browser.html
    img_soup = soup(html0, 'html.parser')
    fst_images = img_soup.find_all('a')
    fst_images[3] = fst_images[3].get('href')
    fst_images_url = f'https://marshemispheres.com/{fst_images[3]}'
    link_url.append(fst_images_url)

    titles = img_soup.find('h2', class_ = 'title').get_text()
    title_lst.append(titles)

    dict1 ={'img_url': fst_images_url, 'title': titles}

    #-----------

    links[2] = links[2].get('href')
    scnd_link_url = f'https://marshemispheres.com/{links[2]}'
    browser.visit(scnd_link_url)

    html1 = browser.html
    img_soup = soup(html1, 'html.parser')
    scnd_images = img_soup.find_all('a')
    scnd_images[3] = scnd_images[3].get('href')
    scnd_images_url = f'https://marshemispheres.com/{scnd_images[3]}'
    link_url.append(scnd_images_url)

    titles = img_soup.find('h2', class_ = 'title').get_text()
    title_lst.append(titles)

    dict2 ={'img_url': scnd_images_url, 'title': titles}

    #-------------

    links[4] = links[4].get('href')
    trd_link_url = f'https://marshemispheres.com/{links[4]}'
    browser.visit(trd_link_url)

    html2 = browser.html
    img_soup = soup(html2, 'html.parser')
    trd_images = img_soup.find_all('a')
    trd_images[3] = trd_images[3].get('href')
    trd_images_url = f'https://marshemispheres.com/{trd_images[3]}'
    link_url.append(trd_images_url)

    titles = img_soup.find('h2', class_ = 'title').get_text()
    title_lst.append(titles)

    dict3 ={'img_url': trd_images_url, 'title': titles}

    #-------------

    links[6] = links[6].get('href')
    fth_link_url = f'https://marshemispheres.com/{links[6]}'
    browser.visit(fth_link_url)

    html3 = browser.html
    img_soup = soup(html3, 'html.parser')
    fth_images = img_soup.find_all('a')
    fth_images[3] = fth_images[3].get('href')
    fth_images_url = f'https://marshemispheres.com/{fth_images[3]}'
    link_url.append(fth_images_url)

    titles = img_soup.find('h2', class_ = 'title').get_text()
    title_lst.append(titles)

    dict4 ={'img_url': fth_images_url, 'title': titles}

    hemisphere_image_urls = [dict1, dict2,dict3,dict4]

    return hemisphere_image_urls

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())
