from scraper import get_driver, scrape_helloworld, scrape_infostud

def test_scrapers():
    print("Testing HelloWorld...")
    driver = get_driver()
    try:
        hw_jobs = scrape_helloworld(driver, "python")
        print(f"HelloWorld: Found {len(hw_jobs)} jobs")
    finally:
        driver.quit()
        
    print("\nTesting Infostud...")
    driver = get_driver()
    try:
        is_jobs = scrape_infostud(driver, "python")
        print(f"Infostud: Found {len(is_jobs)} jobs")
    finally:
        driver.quit()

if __name__ == "__main__":
    test_scrapers()
