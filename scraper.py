import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

def scrape_events_with_selenium(query, city):
    """
    Scrape event data using Selenium.
    Includes titles, links, and event images. Uses a city image as fallback.
    """
    # Set up Selenium WebDriver
    service = Service("/Users/victo/Desktop/chromedriver")  # Update with actual ChromeDriver path
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        # Perform Google search
        driver.get("https://www.google.com")
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        
        time.sleep(2)  # Allow time for results to load
        
        events = []
        results = driver.find_elements(By.CSS_SELECTOR, "div.tF2Cxc")
        print(f"Found {len(results)} results.")  # Debug: Print number of results found
        
        for result in results:
            try:
                # Extract event title and link
                title_element = result.find_element(By.TAG_NAME, "h3")
                link_element = result.find_element(By.CSS_SELECTOR, "a")
                title = title_element.text
                link = link_element.get_attribute("href")
                
                # Attempt to find an image in the result
                try:
                    image_element = result.find_element(By.CSS_SELECTOR, "img")
                    image_url = image_element.get_attribute("src")
                except Exception:
                    # If no image is found, use a fallback image
                    image_url = f"https://source.unsplash.com/400x300/?{city}"
                
                events.append({
                    "title": title,
                    "link": link,
                    "image": image_url
                })
            except Exception as e:
                print(f"Error processing result: {e}")
        
        print(f"Scraped {len(events)} events.")  # Debug: Print number of events scraped
        return events
    finally:
        driver.quit()

