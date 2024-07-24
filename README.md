# Booking.com Hotel Scraper V2

A Python script to scrapes accomandation information from Booking.com search results using Selenium and BeautifulSoup.

## Requirements

- Python 3.x
- Selenium
- BeautifulSoup4
- pandas
- colorama
- webdriver-manager

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/yourusername/booking-hotel-scraper.git
    cd booking-hotel-scraper
    ```

2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Start the script:
    ```bash
    python booking_scraper.py
    ```

2. Follow the on-screen instructions:
    - Enter the Booking.com search results URL when prompted.
    - Enter the maximum number of hotels to scrape.

3. The script will:
    - Open the provided URL in a Chrome browser using Selenium.
    - Scroll down the page to load all hotel results.
    - Scrape hotel names and other details.
    - Handle retries and cooldowns for loading more results.
    - Save the scraped data to an Excel file named `hotels.xlsx`.

## Notes

- Ensure that the Booking.com URL provided returns a list of hotel search results.
- The script will handle scrolling and loading more results automatically.
- The script includes retry and cooldown mechanisms to handle potential scraping issues.

## Warning

- Use this project ethically and legally.
- Respect the website's terms of service.
- Excessive scraping can lead to your IP being blocked by the website.

## License

This project is licensed under the MIT License.
