from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import pandas as pd
import time

# Set up the Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Uncomment to run in headless mode
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')  # Disable GPU acceleration

driver = webdriver.Chrome(options=options)

# Open the earnings calendar page
driver.get('https://www.investing.com/earnings-calendar/')
time.sleep(120)  # Wait for the page to load

# Define the date range
start_date = datetime(2024, 9, 1)
end_date = datetime(2024, 12, 31)

# Wait for the table to load
try:
    print('entered into try block')
    WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'table.earningsCalendarTable'))
          
    )
    
    # Now find the companies
    print (driver.find_elements(By.CSS_SELECTOR, 'table.earningsCalendarTable tr.js-earnings-item'))
    companies = driver.find_elements(By.CSS_SELECTOR, 'table.earningsCalendarTable tr.js-earnings-item')
    print(f"Found {len(companies)} companies.")  # Check how many companies were found

    # Extract earnings data
    earnings_data = []
    for company in companies:
        date_str = company.find_element(By.CSS_SELECTOR, 'td:nth-child(1)').text
        
        date_obj = datetime.strptime(date_str, '%b %d, %Y')  # Adjust the format if needed
        print(date_obj)

        # Check if the date is within the specified range
        if start_date <= date_obj <= end_date:
            # Extract company information
            company_name = company.find_element(By.CSS_SELECTOR, 'td:nth-child(2) a').text
            ticker = company.find_element(By.CSS_SELECTOR, 'td:nth-child(2) a').get_attribute('title')

            # Check if the ticker indicates a US market listing (for example, it might have a format like "AAPL" or "TSLA")
            if ticker and ticker.isalnum():  # Simple check to ensure ticker is valid
                # Append data if it's a US market company
                earnings_data.append({
                    'date': date_str,
                    'company': company_name,
                    'ticker': ticker,
                    'eps': company.find_element(By.CSS_SELECTOR, 'td:nth-child(3)').text,
                    'eps_forecast': company.find_element(By.CSS_SELECTOR, 'td:nth-child(4)').text,
                    'revenue': company.find_element(By.CSS_SELECTOR, 'td:nth-child(5)').text,
                    'revenue_forecast': company.find_element(By.CSS_SELECTOR, 'td:nth-child(6)').text,
                    'market_cap': company.find_element(By.CSS_SELECTOR, 'td:nth-child(7)').text,
                    'time': company.find_element(By.CSS_SELECTOR, 'td:nth-child(8)').text,
                })

    # Save to Excel
    df = pd.DataFrame(earnings_data)
    df.to_excel('earnings_calendar_us.xlsx', index=False)
    print('Earnings calendar for US markets saved to earnings_calendar_us.xlsx')

except Exception as e:
    print ('some problem still happening')
    print(f"An error occurred: {e}")
    # print(driver.page_source)  # Print the page source for debugging
    with open('page_source.html', 'w', encoding='utf-8') as f:
     f.write('<!DOCTYPE html>\n<html>\n<head>\n  <title>Page Source</title>\n</head>\n<body>\n')
     f.write(driver.page_source)
     f.write('\n</body>\n</html>')


# Close the browser
driver.quit()