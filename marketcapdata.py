import requests
import json
import csv
import os
from io import StringIO

# API Keys
COINGECKO_API_KEY = "CG-ep7WBgRCGeDria6EeL1jkPot"
DUNE_API_KEY = "BbxP6Oq2RHQS8nJurQlMfXWsovZNIrro"

# Function to fetch stablecoin market cap data from CoinGecko API
def fetch_market_data():
    url = "https://pro-api.coingecko.com/api/v3/coins/markets"
    headers = {
        "accept": "application/json",
        "x-cg-pro-api-key": COINGECKO_API_KEY
    }
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 1000,
        "page": 1
    }

    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        extracted_data = [{"symbol": item["symbol"], "marketcap_usd": item["market_cap"]} for item in data]
        return extracted_data
    else:
        print("Error fetching data:", response.status_code, response.text)
        return []

# Convert data to CSV format
def convert_to_csv(data):
    csv_file = StringIO()
    writer = csv.DictWriter(csv_file, fieldnames=["symbol", "marketcap_usd"])
    writer.writeheader()
    writer.writerows(data)
    return csv_file.getvalue()

# Upload data to Dune
def upload_to_dune(csv_data):
    url = "https://api.dune.com/api/v1/table/upload/csv"
    headers = {
        'Content-Type': 'application/json',
        'X-DUNE-API-KEY': DUNE_API_KEY
    }
    payload = {
        "data": csv_data,
        "description": "Market Capitalization (Top 100)",
        "table_name": "marketcap_data",
        "is_private": False
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print("Dune Upload Response:", response.text)

# Main function
def main():
    data = fetch_market_data()
    if data:
        csv_data = convert_to_csv(data)
        upload_to_dune(csv_data)

if __name__ == "__main__":
    main()
