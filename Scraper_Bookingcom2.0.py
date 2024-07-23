import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

# Function to initialize the WebDriver
def initialize_driver():
    return webdriver.Chrome(ChromeDriverManager().install())

# Function to clear the screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to print the header
def print_header():
    clear_screen()
    print(Style.BRIGHT + Fore.CYAN + "=" * 50)
    print(Style.BRIGHT + Fore.MAGENTA + " " * 10 + "🌟 Booking.com Hotel Scraper 🌟")
    print(Style.BRIGHT + Fore.CYAN + "=" * 50 + "\n")

# Function to scroll down the page until the end
def scroll_to_bottom(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)  # Wait to load the page
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

# Function to scrape a single page
def scrape_page(driver, scraped_names):
    hotels = []
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    for hotel in soup.find_all('div', attrs={'data-testid': 'property-card'}):
        try:
            name = hotel.find('div', attrs={'data-testid': 'title'}).text.strip()
        except AttributeError:
            name = 'N/A'
        
        if name in scraped_names:
            continue  # Skip duplicates
        
        hotels.append({
            'Name': name,
        })
        scraped_names.add(name)  # Add the name to the set of scraped names
    
    return hotels

# Function to estimate remaining time
def estimate_remaining_time(start_time, total_scraped, total_needed):
    elapsed_time = datetime.now() - start_time
    time_per_hotel = elapsed_time.total_seconds() / total_scraped
    remaining_hotels = total_needed - total_scraped
    remaining_time = remaining_hotels * time_per_hotel
    return remaining_time

# Function to scrape all pages
def scrape_all_pages(driver, base_url, max_hotels):
    all_hotels = []
    scraped_names = set()
    cooldown_attempts = 0
    start_time = datetime.now()

    while True:
        print_header()
        print(Fore.YELLOW + "Scraping page...")
        try:
            scroll_to_bottom(driver)
            hotels = scrape_page(driver, scraped_names)
        except Exception as e:
            print(Fore.RED + f"Error during scraping: {e}")
            time.sleep(30)
            continue
        
        if not hotels:
            if cooldown_attempts == 0:
                print(Fore.RED + "No more hotels found, starting 1-minute cooldown.")
                for i in range(60, 0, -1):
                    print(Fore.YELLOW + f"Cooldown: {i} seconds remaining...", end='\r')
                    time.sleep(1)
                cooldown_attempts += 1
                continue  # Retry scraping the same page after cooldown
            else:
                print(Fore.RED + "No more hotels found after cooldown, stopping scrape.")
                break
        
        all_hotels.extend(hotels)
        total_hotels = len(all_hotels)
        
        print(Fore.GREEN + f"Total unique hotels collected so far: {total_hotels}")
        
        remaining_time = estimate_remaining_time(start_time, total_hotels, max_hotels)
        print(Fore.BLUE + f"Estimated remaining time: {time.strftime('%H:%M:%S', time.gmtime(remaining_time))}")
        
        if total_hotels >= max_hotels:
            print(Fore.GREEN + f"Reached the maximum limit of {max_hotels} unique hotels. Stopping scrape.")
            break

        retry_count = 0
        max_retries = 5
        while retry_count < max_retries:
            try:
                # Re-find the "Load more results" button before each click
                load_more_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'dba1b3bddf') and contains(@class, 'e99c25fd33') and contains(@class, 'ea757ee64b') and contains(@class, 'f1c8772a7d') and contains(@class, 'ea220f5cdc') and contains(@class, 'f870aa1234')]"))
                )
                load_more_button.click()
                print(Fore.CYAN + "Load more button clicked.")
                time.sleep(5)  # Give time for the next set of results to load
                break  # Exit the retry loop if successful
            except Exception as e:
                retry_count += 1
                print(Fore.RED + f"Error while trying to click 'Load more results' button: {e}")
                if retry_count < max_retries:
                    print(Fore.YELLOW + f"Retrying... ({retry_count}/{max_retries})")
                    time.sleep(30)  # Wait for 30 seconds before retrying
                else:
                    user_input = input(Fore.RED + "Max retries reached. Do you want to retry? (yes/no): ").strip().lower()
                    if user_input == 'yes':
                        retry_count = 0  # Reset retry count if user wants to retry
                    else:
                        print(Fore.RED + "Stopping scrape.")
                        return all_hotels
        
        cooldown_attempts = 0  # Reset cooldown attempts after successful scrape
        time.sleep(1)  # A bit of delay to avoid overloading the server

    return all_hotels

# Main function to run the scraper
def main():
    print_header()
    base_url = input(Fore.YELLOW + "Enter the Booking.com search results URL: ")
    max_hotels = int(input(Fore.YELLOW + "Enter the maximum number of hotels to scrape: "))

    driver = initialize_driver()
    driver.get(base_url)

    all_hotels = scrape_all_pages(driver, base_url, max_hotels)

    # Check if hotels were found
    if all_hotels:
        # Put the collected data into a DataFrame
        df = pd.DataFrame(all_hotels)
        
        # Save the data to an Excel file
        df.to_excel('hotels.xlsx', index=False)
        
        print(Fore.GREEN + "\nData successfully saved in hotels.xlsx")
    else:
        print(Fore.RED + "\nNo hotels found. Check the HTML structure of the page.")

    # Close the browser
    driver.quit()

if __name__ == "__main__":
    main()
