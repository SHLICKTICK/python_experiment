import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def automate_youtube_search():
    print("[*] Launching browser...")
    # Opens a new instance of Chrome
    driver = webdriver.Chrome()

    try:
        print("[*] Navigating to YouTube...")
        driver.get("https://www.youtube.com")
        
        # Allow the page to load initial DOM elements
        time.sleep(3)

        print("[*] Locating search bar and entering query...")
        # Find the YouTube search input element by its HTML name attribute
        search_box = driver.find_element(By.NAME, "search_query")
        
        # Type the text into the input field
        search_box.send_keys("Hip Hop Classics")
        
        # Press the Enter key
        search_box.send_keys(Keys.RETURN)
        
        print("[+] Search submitted successfully!")
        
        # Keep browser open for demonstration
        time.sleep(10)

    finally:
        driver.quit()

if __name__ == "__main__":
    automate_youtube_search()