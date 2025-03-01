import requests
import json
import csv
from io import StringIO

def fetch_stablecoin_data():
    url = "https://stablecoins.llama.fi/stablecoins?includePrices=true"
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Failed to fetch data")
        return []
    
    data = response.json()
    pegged_assets = data.get("peggedAssets", [])
    
    extracted_data = []
    
    for asset in pegged_assets:
        symbol = asset.get("symbol", "N/A")
        circulating = asset.get("circulating", {}).get("peggedUSD", 0)
        
        circulating_prev_month = asset.get("circulatingPrevMonth", 0)
        if isinstance(circulating_prev_month, dict):
            circulating_prev_month = circulating_prev_month.get("peggedUSD", 0)
        
        peg_mechanism = asset.get("pegMechanism", "N/A")
        chains = asset.get("chainCirculating", {})
        number_of_chains = len(chains)
        
        extracted_data.append({
            "symbol": symbol,
            "circulating_peggedUSD": circulating,
            "circulatingPrevMonth_peggedUSD": circulating_prev_month,
            "number_of_chains": number_of_chains,
            "pegMechanism": peg_mechanism,
        })
    
    return extracted_data

def convert_to_csv(data):
    csv_file = StringIO()
    fieldnames = ["symbol", "circulating_peggedUSD", "circulatingPrevMonth_peggedUSD", "number_of_chains", "pegMechanism"]
    
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()
    csv_writer.writerows(data)
    
    csv_data = csv_file.getvalue()
    csv_file.close()
    return csv_data

def upload_to_dune(csv_data):
    dune_upload_url = "https://api.dune.com/api/v1/table/upload/csv"
    
    payload = json.dumps({
        "data": csv_data,
        "description": "Stablecoin Market Data",
        "table_name": "stablecoins_market_data",  # Your desired table name in Dune
        "is_private": False
    })
    
    headers = {
        'Content-Type': 'application/json',
        'X-DUNE-API-KEY': 'BbxP6Oq2RHQS8nJurQlMfXWsovZNIrro'  # Replace with your Dune API key
    }
    
    try:
        response = requests.post(dune_upload_url, headers=headers, data=payload)
        response.raise_for_status()
        print("Successfully uploaded to Dune!")
        print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error uploading to Dune: {e}")
        print(f"Response: {response.text if 'response' in locals() else 'No response'}")

def main():
    stablecoins_data = fetch_stablecoin_data()
    
    if stablecoins_data:
        csv_data = convert_to_csv(stablecoins_data)
        
        with open('stablecoins_market_data.csv', 'w') as f:
            f.write(csv_data)
        print("Data saved locally to 'stablecoins_market_data.csv'")
        
        upload_to_dune(csv_data)
    else:
        print("Failed to fetch data")

if __name__ == "__main__":
    main()
