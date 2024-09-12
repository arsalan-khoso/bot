# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import Select
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from bs4 import BeautifulSoup
# import csv
# import re
#
# # Base URL for scraping
# base_url = "https://www.mycitybusiness.net/search.php?cate=Contractor"
#
# # Set up Selenium WebDriver with headless Chrome
# chrome_options = Options()
# chrome_options.add_argument("--headless")
# driver = webdriver.Chrome(options=chrome_options)
#
#
# def scrape_page(driver):
#     soup = BeautifulSoup(driver.page_source, 'html.parser')
#
#     # Find all tables on the page
#     tables = soup.find_all('table')
#
#     # Ensure there are enough tables, and select the 14th table
#     if len(tables) >= 14:
#         table_14 = tables[13]  # Index 13 for the 14th table (0-based index)
#
#         # Extract the rows of the table
#         rows = table_14.find_all('tr')
#
#         # List to hold the extracted data
#         scraped_data = []
#
#         # Define a regex pattern to match phone numbers
#         phone_pattern = re.compile(r'\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{4}')
#
#         # Iterate over rows and extract relevant information
#         for i in range(0, len(rows), 2):  # Business info in alternate rows
#             try:
#                 # Extract the business name
#                 business_name = rows[i].find('strong').text.strip()
#
#                 # Skip rows with "Company / Address"
#                 if "Company / Address" in business_name:
#                     continue
#
#                 # Extract full address (with city, state, ZIP code)
#                 address_rows = rows[i + 1].find('td').find('table').find_all('tr')
#                 full_address_parts = [r.text.strip() for r in address_rows[:2]]  # Get only the first 2 <tr> elements
#                 full_address = ', '.join(full_address_parts)
#
#                 # Extract phone number using regex
#                 phone = "N/A"
#                 phone_section = rows[i + 1].text.strip()
#                 phone_match = phone_pattern.search(phone_section)
#                 if phone_match:
#                     phone = phone_match.group()
#
#                 # Extract email if available
#                 email = "N/A"
#                 # Access the correct td element and search for the email link
#                 email_td = rows[i + 1].find_all('td')[5]
#                 email_section = email_td.find('a', href=True)
#                 if email_section and 'mailto:' in email_section['href']:
#                     email = email_section['href'].replace("mailto:", "").strip()
#
#                 # Append the extracted information to the list
#                 scraped_data.append([business_name, email, phone, full_address])
#
#             except Exception as e:
#                 print(f"Error extracting data: {e}")
#
#         return scraped_data
#     else:
#         print("There are less than 14 tables on the page.")
#         return []
#
#
# def navigate_pages(driver, num_pages=5):
#     all_scraped_data = []
#
#     for page in range(num_pages):
#         # Select the page from the dropdown
#         select_element = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.NAME, 'pg'))
#         )
#         select = Select(select_element)
#         select.select_by_value(str(page))  # Select the page by value
#         driver.find_element(By.NAME, 'pageForm1').submit()  # Submit the form
#
#         # Wait for the page to load
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.TAG_NAME, 'table'))
#         )
#
#         # Scrape the page
#         data = scrape_page(driver)
#         if not data:
#             break
#         all_scraped_data.extend(data)
#
#     return all_scraped_data
#
#
# # Start the browser and open the base URL
# driver.get(base_url)
#
# # Scrape the pages
# all_scraped_data = navigate_pages(driver, num_pages=5)
#
# # Close the browser
# driver.quit()
#
# # Save the data to a CSV file
# with open('scraped_business_data.csv', 'w', newline='', encoding='utf-8') as f:
#     writer = csv.writer(f)
#     writer.writerow(['Business Name', 'Email Address', 'Phone', 'Address'])
#     writer.writerows(all_scraped_data)
#
# print(f"Scraping completed successfully. Data saved to 'scraped_business_data.csv'.")


# import aiohttp
# import asyncio
# import csv
# from bs4 import BeautifulSoup
# import re
# from tenacity import retry, stop_after_attempt, wait_exponential
#
# # List of categories to scrape
# categories = [
#     "Contractor", "Contractors", "Plumber", "Plumbers", "Plumbing",
#     "Lubricant", "Lubricants", "Roofing Electrical", "Landscape",
#     "Floors", "Windows", "Remodeling", "HVAC", "Handyman", "Handy",
#     "craftman", "Paint", "Painting", "Charitable", "Home Improvement",
#     "home", "Non profit", "Church", "furniture", "decor", "tree",
#     "kitchen", "interior", "exterior", "material", "doors", "bathroom",
#     "heating", "cooling", "manufactoring", "swimming pool", "showers",
#     "technologies", "tech"
# ]
#
# # Base URL for scraping
# base_url = "https://www.mycitybusiness.net/search.php?cate={}"
#
# # Regex pattern for phone numbers
# phone_pattern = re.compile(r'\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{4}')
#
#
# # Function to scrape data from a single page
# @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
# async def scrape_page(session, category, page):
#     url = base_url.format(category) + f"&pg={page}"
#     try:
#         async with session.get(url) as response:
#             response.raise_for_status()  # Check for HTTP errors
#             html = await response.text()
#             soup = BeautifulSoup(html, 'html.parser')
#             tables = soup.find_all('table')
#             scraped_data = []
#
#             if len(tables) >= 14:
#                 table_14 = tables[13]  # Index 13 for the 14th table
#                 rows = table_14.find_all('tr')
#
#                 for i in range(0, len(rows), 2):
#                     try:
#                         business_name = rows[i].find('strong').text.strip()
#                         if "Company / Address" in business_name:
#                             continue
#                         address_rows = rows[i + 1].find('td').find('table').find_all('tr')
#                         full_address_parts = [r.text.strip() for r in address_rows[:2]]
#                         full_address = ', '.join(full_address_parts)
#                         phone = "N/A"
#                         phone_section = rows[i + 1].text.strip()
#                         phone_match = phone_pattern.search(phone_section)
#                         if phone_match:
#                             phone = phone_match.group()
#                         email = "N/A"
#                         email_td = rows[i + 1].find_all('td')[5]
#                         email_section = email_td.find('a', href=True)
#                         if email_section and 'mailto:' in email_section['href']:
#                             email = email_section['href'].replace("mailto:", "").strip()
#                         scraped_data.append([business_name, email, phone, full_address])
#                     except Exception as e:
#                         print(f"Error extracting data from row: {e}")
#
#             return scraped_data
#     except aiohttp.ClientResponseError as e:
#         print(f"Client response error: {e}")
#     except aiohttp.ClientConnectionError as e:
#         print(f"Client connection error: {e}")
#     except aiohttp.ClientPayloadError as e:
#         print(f"Client payload error: {e}")
#     except Exception as e:
#         print(f"General error: {e}")
#
#
# # Function to handle scraping for all categories and pages
# async def scrape_all_categories(categories, num_pages=5):
#     async with aiohttp.ClientSession() as session:
#         for category in categories:
#             category_data = []
#             tasks = [scrape_page(session, category, page) for page in range(1, num_pages + 1)]
#             results = await asyncio.gather(*tasks)  # Concurrently run all page scraping tasks
#
#             for result in results:
#                 if result:
#                     category_data.extend(result)
#                 else:
#                     print(f"No data found for {category} on a page")
#
#             # Save the data for the current category to a CSV file
#             save_to_csv(category, category_data)
#             print(f"Data for category '{category}' saved to '{category}_business_data.csv'.")
#
#
# # Function to save data to a CSV file
# def save_to_csv(category, data):
#     filename = f'{category}_business_data.csv'
#     with open(filename, 'w', newline='', encoding='utf-8') as f:
#         writer = csv.writer(f)
#         writer.writerow(['Business Name', 'Email Address', 'Phone', 'Address'])
#         writer.writerows(data)
#
#
# # Main function to run the scraping
# async def main():
#     await scrape_all_categories(categories, num_pages=5)
#
#
# # Run the main function
# if __name__ == "__main__":
#     asyncio.run(main())



# import aiohttp
# import asyncio
# import csv
# from tenacity import retry, wait_exponential, stop_after_attempt
#
# # Function to fetch page data
# @retry(wait=wait_exponential(multiplier=1, min=4, max=15), stop=stop_after_attempt(5))
# async def fetch_page(session, url):
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
#     }
#     async with session.get(url, headers=headers) as response:
#         response.raise_for_status()  # Raise an error for bad responses
#         return await response.text()
#
# # Function to scrape data from a single page
# async def scrape_page(session, category, page):
#     url = f"https://www.mycitybusiness.net/search.php?cate={category}&page={page}"
#     html = await fetch_page(session, url)
#     return parse_html(html)
#
# # Function to parse HTML and extract data
# def parse_html(html):
#     from bs4 import BeautifulSoup
#     import re
#
#     soup = BeautifulSoup(html, 'html.parser')
#     tables = soup.find_all('table')
#
#     if len(tables) >= 14:
#         table_14 = tables[13]  # Index 13 for the 14th table (0-based index)
#         rows = table_14.find_all('tr')
#
#         scraped_data = []
#         phone_pattern = re.compile(r'\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{4}')
#
#         for i in range(0, len(rows), 2):
#             try:
#                 business_name = rows[i].find('strong').text.strip()
#                 if "Company / Address" in business_name:
#                     continue
#
#                 address_rows = rows[i + 1].find('td').find('table').find_all('tr')
#                 full_address_parts = [r.text.strip() for r in address_rows[:2]]
#                 full_address = ', '.join(full_address_parts)
#
#                 phone = "N/A"
#                 phone_section = rows[i + 1].text.strip()
#                 phone_match = phone_pattern.search(phone_section)
#                 if phone_match:
#                     phone = phone_match.group()
#
#                 email = "N/A"
#                 email_td = rows[i + 1].find_all('td')[5]
#                 email_section = email_td.find('a', href=True)
#                 if email_section and 'mailto:' in email_section['href']:
#                     email = email_section['href'].replace("mailto:", "").strip()
#
#                 scraped_data.append([business_name, email, phone, full_address])
#
#             except Exception as e:
#                 print(f"Error extracting data: {e}")
#
#         return scraped_data
#     else:
#         print("There are less than 14 tables on the page.")
#         return []
#
# # Function to scrape all pages for all categories
# async def scrape_all_categories(categories, num_pages=500):
#     async with aiohttp.ClientSession() as session:
#         for category in categories:
#             category_data = []
#             tasks = [scrape_page(session, category, page) for page in range(1, num_pages + 1)]
#             results = await asyncio.gather(*tasks)
#
#             for result in results:
#                 if result:
#                     category_data.extend(result)
#                 else:
#                     print(f"No data found for {category} on a page")
#
#             # Save the data for the current category to a CSV file
#             save_to_csv(category, category_data)
#             print(f"Data for category '{category}' saved to '{category}_business_data.csv'.")
#
# # Function to save data to a CSV file
# def save_to_csv(category, data):
#     filename = f"{category}_business_data.csv"
#     with open(filename, 'w', newline='', encoding='utf-8') as f:
#         writer = csv.writer(f)
#         writer.writerow(['Business Name', 'Email Address', 'Phone', 'Address'])
#         writer.writerows(data)
#
# # Main function to run the scraping process
# async def main():
#     categories = [
#         "Contractor", "Contractors", "Plumber", "Plumbers", "Plumbing",
#         "Lubricant", "Lubricants", "Roofing Electrical", "Landscape", "Floors",
#         "Windows", "Remodeling", "HVAC", "Handyman", "Handy", "craftman",
#         "Paint", "Painting", "Charitable", "Home Improvement", "home",
#         "Non profit", "Church", "furniture", "decor", "tree", "kitchen",
#         "interior", "exterior", "material", "doors", "bathroom", "heating",
#         "cooling", "manufactoring", "swimming pool", "showers", "technologies", "tech"
#     ]
#     await scrape_all_categories(categories, num_pages=500)
#
# # Run the main function
# if __name__ == '__main__':
#     asyncio.run(main())
#


import aiohttp
import asyncio
import csv
from tenacity import retry, wait_exponential, stop_after_attempt

# Function to fetch page data
@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(5))
async def fetch_page(session, url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    async with session.get(url, headers=headers) as response:
        response.raise_for_status()
        return await response.text()

# Function to scrape data from a single page
async def scrape_page(session, category, page):
    url = f"https://www.mycitybusiness.net/search.php?cate={category}&page={page}"
    html = await fetch_page(session, url)
    data = parse_html(html)
    return category, data

# Function to parse HTML and extract data
def parse_html(html):
    from bs4 import BeautifulSoup
    import re

    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find_all('table')

    if len(tables) >= 14:
        table_14 = tables[13]
        rows = table_14.find_all('tr')

        scraped_data = []
        phone_pattern = re.compile(r'\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{4}')

        for i in range(0, len(rows), 2):
            try:
                business_name = rows[i].find('strong').text.strip()
                if "Company / Address" in business_name:
                    continue

                address_rows = rows[i + 1].find('td').find('table').find_all('tr')
                full_address_parts = [r.text.strip() for r in address_rows[:2]]
                full_address = ', '.join(full_address_parts)

                phone = "N/A"
                phone_section = rows[i + 1].text.strip()
                phone_match = phone_pattern.search(phone_section)
                if phone_match:
                    phone = phone_match.group()

                email = "N/A"
                email_td = rows[i + 1].find_all('td')[5]
                email_section = email_td.find('a', href=True)
                if email_section and 'mailto:' in email_section['href']:
                    email = email_section['href'].replace("mailto:", "").strip()

                scraped_data.append([business_name, email, phone, full_address])

            except Exception as e:
                print(f"Error extracting data: {e}")

        return scraped_data
    else:
        print("There are less than 14 tables on the page.")
        return []

# Function to scrape all pages for all categories
async def scrape_all_categories(categories, num_pages=3):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for category in categories:
            for page in range(1, num_pages + 1):
                tasks.append(scrape_page(session, category, page))

        results = await asyncio.gather(*tasks)

        # Organize results by category
        categorized_data = {}
        for category, data in results:
            if category not in categorized_data:
                categorized_data[category] = []
            if data:
                categorized_data[category].extend(data)

        # Save data for each category to a CSV file
        for category, data in categorized_data.items():
            save_to_csv(category, data)
            print(f"Data for category '{category}' saved to '{category}_business_data.csv'.")

# Function to save data to a CSV file
def save_to_csv(category, data):
    filename = f"{category}_business_data.csv"
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Business Name', 'Email Address', 'Phone', 'Address'])
        writer.writerows(data)

# Main function to run the scraping process
async def main():
    categories = [
        "Contractor", "Contractors", "Plumber", "Plumbers", "Plumbing",
        "Lubricant", "Lubricants", "Roofing Electrical", "Landscape", "Floors",
        "Windows", "Remodeling", "HVAC", "Handyman", "Handy", "craftman",
        "Paint", "Painting", "Charitable", "Home Improvement", "home",
        "Non profit", "Church", "furniture", "decor", "tree", "kitchen",
        "interior", "exterior", "material", "doors", "bathroom", "heating",
        "cooling", "manufactoring", "swimming pool", "showers", "technologies", "tech"
    ]
    await scrape_all_categories(categories, num_pages=5)

# Run the main function
if __name__ == '__main__':
    asyncio.run(main())
