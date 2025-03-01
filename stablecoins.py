import requests
import json
import csv
import time
from io import StringIO
from selenium import webdriver
from selenium.webdriver.common.by import By

# Function to fetch stablecoin market cap data
def fetch_market_data():
    driver = webdriver.Chrome()
    extracted_data = []

    try:
        driver.get("https://www.coingecko.com/en/categories/stablecoins")
        time.sleep(5)  # Allow time for the page to load

        # Get total market cap (Updated XPath)
        try:
            total_marketcap = driver.find_element(By.XPATH, '/html/body/div[3]/main/div/div[3]/div/div/div[1]/div/div[1]/span').text
            extracted_data.append({"symbol": "TOTAL_MARKETCAP", "marketcap_usd": total_marketcap.replace("$", "").replace(",", "").strip()})
        except:
            extracted_data.append({"symbol": "TOTAL_MARKETCAP", "marketcap_usd": "N/A"})

        # Get top 50 stablecoins
        for i in range(1, 51):
            try:
                symbol = driver.find_element(By.XPATH, f'/html/body/div[3]/main/div/div[5]/div[1]/div[3]/table/tbody/tr[{i}]/td[3]/a/div/div').text
                marketcap = driver.find_element(By.XPATH, f'/html/body/div[3]/main/div/div[5]/div[1]/div[3]/table/tbody/tr[{i}]/td[11]/span').text.replace("$", "").replace(",", "").strip()
                extracted_data.append({"symbol": symbol, "marketcap_usd": marketcap})
            except:
                continue
    finally:
        driver.quit()

    return extracted_data

# Convert to CSV
def convert_to_csv(data):
    csv_file = StringIO()
    writer = csv.DictWriter(csv_file, fieldnames=["symbol", "marketcap_usd"])
    writer.writeheader()
    writer.writerows(data)
    return csv_file.getvalue()

# Upload to Dune
def upload_to_dune(csv_data):
    response = requests.post(
        "https://api.dune.com/api/v1/table/upload/csv",
        headers={'Content-Type': 'application/json', 'X-DUNE-API-KEY': 'BbxP6Oq2RHQS8nJurQlMfXWsovZNIrro'},
        data=json.dumps({
            "data": csv_data,
            "description": "Stablecoin Market Capitalization (Total + Top 50)",
            "table_name": "stablecoins_marketcap_data",
            "is_private": False
        })
    )
    print("Upload Response:", response.text)

# Main function
def main():
    data = fetch_market_data()
    if data:
        csv_data = convert_to_csv(data)
        upload_to_dune(csv_data)

if __name__ == "__main__":
    main()
