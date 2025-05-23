from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import pandas as pd

url = 'https://shopee.co.id/buyer/145591552/rating?shop_id=145589728'

if url:
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-notifications")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    driver = webdriver.Chrome(options=options)
    
    # Set user agent
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
        "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })
    
    # Access the URL
    driver.get(url)
    
    # Wait for page to load
    print("Waiting for page to load...")
    time.sleep(5)
    
    try:
        # Wait for content to be visible
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.flex.flex-col"))
        )
        print("Page loaded successfully")
    except TimeoutException:
        print("Timeout waiting for page to load")
    
    data = []
    page = 1
    max_pages = 1
    
    while page <= max_pages:
        print(f"Scraping page {page}")
        # Allow some time for dynamic content to load
        time.sleep(3)
        
        # Get page source after JavaScript has rendered
        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        # Find review containers - adjust selector based on actual page structure
        reviews = soup.select("div.shopee-product-comment-list div.shopee-product-rating")
        if not reviews:
            reviews = soup.select("div.flex.flex-col div.rating-comment-container")
        
        if not reviews:
            print(f"No reviews found on page {page}. Trying alternative selectors...")
            reviews = soup.select("article.css-ccpe8t")
            
        print(f"Found {len(reviews)} reviews on page {page}")
        
        for review in reviews:
            try:
                # Try different selectors for review text
                review_text = None
                review_selectors = [
                    "span[data-testid='lblItemUlasan']",
                    "div.shopee-product-rating__content",
                    "div.rating-comment-text",
                    "p.review-content"
                ]
                
                for selector in review_selectors:
                    review_element = review.select_one(selector)
                    if review_element:
                        review_text = review_element.text.strip()
                        break
                
                if review_text:
                    data.append(review_text)
                    print(f"Review found: {review_text[:50]}..." if len(review_text) > 50 else f"Review found: {review_text}")
            except Exception as e:
                print(f"Error extracting review: {str(e)}")
                continue
        
        # Try to navigate to the next page
        try:
            if page < max_pages:
                # Try different selectors for next page button
                next_button = None
                try:
                    next_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label^='Laman berikutnya']")
                except NoSuchElementException:
                    try:
                        next_button = driver.find_element(By.CSS_SELECTOR, "button.shopee-icon-button--right")
                    except NoSuchElementException:
                        try:
                            pagination_buttons = driver.find_elements(By.CSS_SELECTOR, "div.shopee-page-controller button")
                            for button in pagination_buttons:
                                if "next" in button.get_attribute("class").lower() or "right" in button.get_attribute("class").lower():
                                    next_button = button
                                    break
                        except:
                            pass
                
                if next_button and next_button.is_enabled():
                    next_button.click()
                    print(f"Navigated to page {page + 1}")
                    time.sleep(3)
                else:
                    print("No more pages available or next button not found")
                    break
            else:
                print(f"Reached maximum number of pages ({max_pages})")
        except Exception as e:
            print(f"Error navigating to next page: {str(e)}")
            break
            
        page += 1

    print(f"Total reviews collected: {len(data)}")
    if data:
        df = pd.DataFrame(data, columns=["Ulasan"])
        df.to_csv("hns.csv", index=False)
        print("Data saved to hns.csv")
    else:
        print("No data collected")
        
    # Close the browser
    driver.quit()