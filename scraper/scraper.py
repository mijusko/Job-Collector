from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import urllib.parse

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    # Updated User-Agent to match debug script
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # Extra anti-detection options
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def scrape_helloworld(driver, query, location=""):
    base_url = "https://www.helloworld.rs/oglasi-za-posao"
    params = {}
    if query: params['q'] = query
    if location: params['grad'] = location
    
    url = f"{base_url}?{urllib.parse.urlencode(params)}" if params else base_url
    print(f"Scraping HelloWorld: {url}")
    
    jobs = []
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h3")))
        
        h3_elements = driver.find_elements(By.CSS_SELECTOR, "h3")
        for h3 in h3_elements:
            if len(jobs) >= 15: break
            try:
                title = h3.text.strip()
                if not title or len(title) < 5 or any(x in title for x in ["Sačuvaj", "Popuni"]): continue
                
                container = h3
                for _ in range(5):
                    container = container.find_element(By.XPATH, "./parent::*")
                    if container.tag_name in ['a', 'div'] and ('card' in (container.get_attribute('class') or '').lower() or 'item' in (container.get_attribute('class') or '').lower() or container.tag_name == 'a'):
                        break
                
                job_url = ""
                try:
                    if container.tag_name == 'a': job_url = container.get_attribute("href")
                    else: job_url = container.find_element(By.TAG_NAME, "a").get_attribute("href")
                except: continue

                if not job_url or "helloworld.rs" not in job_url: continue

                try: company = container.find_element(By.CSS_SELECTOR, "[class*='company'], [class*='employer'], .text-sm").text.strip()
                except: company = "HelloWorld Poslodavac"
                
                try: loc = container.find_element(By.CSS_SELECTOR, "[class*='location'], [class*='city'], .text-xs").text.strip()
                except: loc = "Srbija"
                
                jobs.append({
                    "id": f"hw-{len(jobs)}",
                    "title": title,
                    "company": company,
                    "location": loc,
                    "date": "Danas",
                    "url": job_url,
                    "source": "HelloWorld"
                })
            except: continue
    except Exception as e:
        print(f"HelloWorld error: {e}")
    return jobs

def scrape_infostud(driver, query, location=""):
    base_url = "https://poslovi.infostud.com/oglasi-za-posao"
    params = {}
    if query: params['q'] = query
    if location: params['grad'] = location
    
    url = f"{base_url}?{urllib.parse.urlencode(params)}" if params else base_url
    print(f"Scraping Infostud: {url}")
    
    jobs = []
    try:
        print(f"Loading URL: {url}")
        driver.set_page_load_timeout(20)
        driver.get(url)
        print("Page loaded, waiting for elements...")
        time.sleep(2)
        
        items = driver.find_elements(By.CSS_SELECTOR, ".search-job-card[data-job-id]")
        print(f"Infostud found {len(items)} potential job cards")
        
        for item in items:
            if len(jobs) >= 15:
                break
            try:
                try:
                    title_elem = item.find_element(By.CSS_SELECTOR, "[id$='job-card-title']")
                except:
                    title_elem = item.find_element(By.CSS_SELECTOR, "h2, h3")
                title = title_elem.text.strip()
                if not title:
                    continue

                try:
                    link_elem = item.find_element(By.CSS_SELECTOR, "a[href*='/posao/']")
                    link = link_elem.get_attribute("href")
                except:
                    link = ""
                if not link:
                    continue

                try:
                    logo = item.find_element(By.CSS_SELECTOR, "img[alt*='logo']")
                    alt_text = logo.get_attribute("alt") or ""
                    company = alt_text.replace(" logo", "").strip()
                    if not company:
                        company = "Infostud Poslodavac"
                except:
                    company = "Infostud Poslodavac"

                try:
                    loc_elem = item.find_element(By.CSS_SELECTOR, "[class*='location'], [class*='grad'], [class*='city']")
                    loc = loc_elem.text.strip()
                    if not loc:
                        loc = "Srbija"
                except:
                    loc = "Srbija"

                jobs.append({
                    "id": f"is-{len(jobs)}",
                    "title": title,
                    "company": company,
                    "location": loc,
                    "date": "Danas",
                    "url": link,
                    "source": "Infostud"
                })
            except Exception:
                continue
    except Exception as e:
        print(f"Infostud error: {e}")
    
    print(f"Infostud found {len(jobs)} valid jobs")
    return jobs

def scrape_all(query, location=""):
    print(f"DEBUG: scrape_all called with query='{query}', location='{location}'")
    driver = get_driver()
    all_jobs = []
    try:
        all_jobs.extend(scrape_helloworld(driver, query, location))
        all_jobs.extend(scrape_infostud(driver, query, location))
    finally:
        driver.quit()
    
    return all_jobs

if __name__ == "__main__":
    results = scrape_all("python")
    print(f"Found total {len(results)} jobs")
    for job in results:
        print(f"[{job['source']}] {job['title']} at {job['company']}")
