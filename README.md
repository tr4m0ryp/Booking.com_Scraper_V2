# Booking.com Hotel Scraper V2

A Python script to scrape hotel information from Booking.com search results using Selenium and BeautifulSoup.

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

1. Run the script:
    ```bash
    python booking_scraper.py
    ```

2. Follow the on-screen instructions to input the Booking.com search results URL and the maximum number of hotels to scrape.

3. The scraped data will be saved to an Excel file named `hotels.xlsx`.

## Notes

- Ensure that the Booking.com URL provided returns a list of hotel search results.
- The script will handle scrolling and loading more results automatically.
- The script includes retry and cooldown mechanisms to handle potential scraping issues.

## License

This project is licensed under the MIT License.
