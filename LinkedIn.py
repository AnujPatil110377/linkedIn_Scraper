# import openpyxl
# wb = openpyxl.load_workbook('company.xlsx')
# print("files loaded successfully" )
# sheet = wb['Sheet1']
# # print(sheet)
# # wb.create_sheet("nEWSHEET")
# # print(wb.sheetnames)
# wb.save("company.xlsx")
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from openpyxl import Workbook, load_workbook
import time

def scrape_linkedin(company_name, job_keywords, driver):
    # Perform LinkedIn search
    search_query = f'site:linkedin.com/in "{company_name}" "{job_keywords}"'
    search_url = f'https://www.google.com/search?q={search_query}'
    driver.get(search_url)
    time.sleep(2)  # Add a delay to ensure page load

    # Parse search results
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    profiles = soup.find_all('div', class_='BNeawe UPmit AP7Wnd')

    scraped_data = []
    for profile in profiles:
        try:
            name = profile.text.split(' - ')[0]
            position = profile.text.split(' - ')[1]
            linkedin_url = profile.find_parent('a')['href']
            scraped_data.append((name, position, linkedin_url))
        except Exception as e:
            print(f"Error parsing profile: {e}")

    return scraped_data

def main():
    # Load company names from Excel sheet
    wb = load_workbook('company.xlsx')
    sheet = wb.active
    companies = [cell.value for row in sheet.iter_rows() for cell in row if cell.value]

    # Specify job keywords
    job_keywords = "Campus recruitment -talent acquisition -hr"

    # Initialize Chrome WebDriver
    driver = webdriver.Chrome()

    # Scrape LinkedIn profiles for each company
    all_data = []
    for company in companies:
        print(f"Scraping LinkedIn for {company}...")
        data = scrape_linkedin(company, job_keywords, driver)
        all_data.extend(data)

    # Close the WebDriver
    driver.quit()

    # Write results to Excel sheet
    wb_new = Workbook()
    sheet_new = wb_new.active
    sheet_new.append(['Name', 'Position', 'LinkedIn URL'])
    for name, position, linkedin_url in all_data:
        sheet_new.append([name, position, linkedin_url])
    wb_new.save('linkedin_profiles.xlsx')

if __name__ == "__main__":
    main()
