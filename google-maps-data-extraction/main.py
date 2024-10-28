from playwright.sync_api import sync_playwright
import pandas as pd
import argparse
import logging
import os
from itertools import zip_longest

# Logging settings
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Lists to store data
names_list = []
address_list = []
website_list = []
phones_list = []
reviews_c_list = []
reviews_a_list = []
place_t_list = []
open_list = []
intro_list = []


def add_unique_data(data, data_list):
    """Adds data if it is not empty and not already in the list."""
    if data and data not in data_list:
        data_list.append(data)


def extract_data(locator, data_list, page):
    """Extracts data from the page using the specified locator."""
    if page.locator(locator).count() > 0:
        data = page.locator(locator).all_inner_texts()
        for item in data:
            add_unique_data(item, data_list)
    else:
        data_list.append("-")


def main():
    """Main function."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()

        # Go to the Google Maps page
        page.goto("https://www.google.com/maps", timeout=60000)
        page.wait_for_timeout(1000)

        # Concatenate the search term with location
        search_query = f"{search_for} in {location}"

        # Type the search term in the search box and press Enter
        page.fill('//input[@id="searchboxinput"]', search_query)
        page.keyboard.press("Enter")
        page.wait_for_selector('//a[contains(@href, "https://www.google.com/maps/place")]', timeout=10000)

        previously_counted = 0
        i = 1
        while i < 200:
            i += 1
            page.locator("//*[@id=\"QA0Szd\"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]").hover()
            page.mouse.wheel(0, 1000)  # Scroll down the page
        page.wait_for_timeout(20)

        while True:
            page.wait_for_selector('//a[contains(@href, "https://www.google.com/maps/place")]')

            counted = page.locator('//a[contains(@href, "https://www.google.com/maps/place")]').count()
            if counted >= total:
                listings = page.locator('//a[contains(@href, "https://www.google.com/maps/place")]').all()[:total]
                logging.info(f"Total Found: {len(listings)}")
                break
            elif counted == previously_counted:
                listings = page.locator('//a[contains(@href, "https://www.google.com/maps/place")]').all()
                logging.info(f"All available data found.\nTotal Found: {len(listings)}")
                break
            else:
                previously_counted = counted
                logging.info(f"Currently Found: {previously_counted}")

        # Data extraction process
        for i in range(len(listings)):
            if page.locator('//a[contains(@href, "https://www.google.com/maps/place")]').nth(i).is_visible():
                page.locator('//a[contains(@href, "https://www.google.com/maps/place")]').nth(i).click()
                page.wait_for_timeout(2000)  # Wait for data to load

                # Xpaths
                name_xpath = '//div[@class="TIHn2 "]//h1[@class="DUwDvf lfPIob"]'
                address_xpath = '//button[@data-item-id="address"]//div[contains(@class, "fontBodyMedium")]'
                website_xpath = '//a[@data-item-id="authority"]//div[contains(@class, "fontBodyMedium")]'
                phone_number_xpath = '//button[contains(@data-item-id, "phone:tel:")]//div[contains(@class, "fontBodyMedium")]'
                reviews_count_xpath = '//div[@class="TIHn2 "]//div[@class="fontBodyMedium dmRWX"]//div//span//span//span[@aria-label]'
                reviews_average_xpath = '//div[@class="TIHn2 "]//div[@class="fontBodyMedium dmRWX"]//div//span[@aria-hidden]'
                opens_at_xpath = '//button[contains(@data-item-id, "oh")]//div[contains(@class, "fontBodyMedium")]'
                place_type_xpath = '//div[@class="LBgpqf"]//button[@class="DkEaL "]'
                intro_xpath = '//div[@class="WeS02d fontBodyMedium"]//div[@class="PYvSYb "]'

                # Extract data
                extract_data(name_xpath, names_list, page)
                extract_data(address_xpath, address_list, page)
                extract_data(website_xpath, website_list, page)
                extract_data(phone_number_xpath, phones_list, page)
                extract_data(reviews_count_xpath, reviews_c_list, page)
                extract_data(reviews_average_xpath, reviews_a_list, page)
                extract_data(opens_at_xpath, open_list, page)
                extract_data(place_type_xpath, place_t_list, page)
                if page.locator(intro_xpath).count() > 0:
                    intro = page.locator(intro_xpath).inner_text()
                    add_unique_data(intro, intro_list)
                else:
                    intro_list.append("")

        # Using zip_longest to make lists the same length
        data = list(zip_longest(names_list, website_list, intro_list, phones_list,
                                address_list, reviews_c_list, reviews_a_list,
                                open_list, place_t_list, fillvalue=""))

        # Check if the /output directory exists, and create it if not
        output_dir = './output'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Create and save the DataFrame
        try:
            df = pd.DataFrame(data, columns=[
                'Names', 'Website', 'Introduction', 'Phone Number',
                'Address', 'Review Count', 'Average Review Count',
                'Opens At', 'Type'
            ])
            df = df.drop_duplicates()  # Remove duplicate rows

            # File paths
            csv_path = os.path.join(output_dir, "result.csv")
            json_path = os.path.join(output_dir, "result.json")
            html_path = os.path.join(output_dir, "result.html")

            # Save data as CSV, JSON, and HTML
            df.to_csv(csv_path, index=False)
            df.to_json(json_path, orient="table", index=False)
            df.to_html(html_path, index=False)

            logging.info("Data saved to /output directory.")
            print(df.head())
        except ValueError as e:
            logging.error(f"Error: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--search", type=str, default="Restaurant")
    parser.add_argument("-l", "--location", type=str, default="Turkey")
    parser.add_argument("-t", "--total", type=int, default=100)
    args = parser.parse_args()

    search_for = args.search
    location = args.location
    total = args.total

    main()
