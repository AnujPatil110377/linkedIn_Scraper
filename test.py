import undetected_chromedriver as uc
import time 
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# List of companies to search for
companies = [
    'adobe', 'hr', 'google', 'oracle', 'ibm', 'hp', 'asus', 'microsoft', 'adani',
    'apple', 'amazon', 'microsoft', 'alphabet', 'facebook', 'tencent', 'alibaba', 
    'netflix', 'paypal', 'nvidia', 'salesforce', 'accenture', 'tesla', 'sap', 
    'ibm', 'cisco', 'intel', 'adobe', 'hp', 'qualcomm', 'vmware', 'baidu', 
    'siemens', 'sony', 'panasonic', 'hitachi', 'lenovo', 'xerox', 'huawei', 
    'nintendo', 'dell', 'uber', 'lyft', 'airbnb', 'snap', 'twitter', 
    'linkedin', 'spotify', 'dropbox', 'pinterest', 'ebay', 'zynga'
]


options = uc.ChromeOptions() 
driver = uc.Chrome()

# Iterate over each company
for company in companies:
    # Construct the search query URL
    search_query = '+'.join(company.split()) + '+hr+linkedin'
    search_url = f"https://www.google.com/search?q={search_query}"

    # Navigate to the search query URL
    driver.get(search_url) 

    # Sleep for a certain amount of time to allow the elements to load
    time.sleep(5)  # Adjust the sleep duration as needed

    # Get the page source
    page_source = driver.page_source

    # Parse the page source using BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find all <a> elements containing LinkedIn URLs
    linkedin_links = soup.find_all('a', href=True, attrs={'ping': True})

    # Extract name and LinkedIn ID from each link
    for link in linkedin_links:
        linkedin_url = link.get('href')
        if linkedin_url:
            linkedin_id = linkedin_url.split('/')[-1]

            # Find the <span> element containing the name
            name_span = link.find('span', class_='VuuXrf')
            if name_span:
                name = name_span.text.strip()
            else:
                name = "Name not found"

            # Print the name and LinkedIn ID
            print("Company:", company)
            print("Name:", name)
            print("LinkedIn ID:", linkedin_id)
            print()  # Add a blank line for readability
        else:
            print("No LinkedIn URL found for this search result.")
