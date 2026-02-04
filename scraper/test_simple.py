from scraper import get_driver, scrape_helloworld, scrape_infostud
import time

def test_simple():
    print("Testing simple scraping...")
    driver = get_driver()
    try:
        # Test HelloWorld with shorter timeout
        print("Testing HelloWorld...")
        driver.set_page_load_timeout(10)
        driver.get("https://www.helloworld.rs/oglasi-za-posao?q=python")
        time.sleep(3)  # Wait for page to load
        
        # Look for job elements
        jobs = driver.find_elements("css selector", "h3")
        print(f"Found {len(jobs)} h3 elements")
        
        for job in jobs[:3]:
            try:
                title = job.text.strip()
                print(f"Title: {title}")
            except:
                continue
                
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    test_simple()