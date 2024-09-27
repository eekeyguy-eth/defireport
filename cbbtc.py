import requests
import json
import csv
from io import StringIO
from datetime import datetime

def fetch_cbbtc_data():
    url = "https://yields.llama.fi/pools"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        cbbtc_pools = []
        
        for pool in data['data']:
            if 'CBBTC' in pool.get('symbol', ''):
                cbbtc_pools.append({
                    'chain': pool.get('chain'),
                    'project': pool.get('project'),
                    'symbol': pool.get('symbol'),
                    'tvlUsd': pool.get('tvlUsd')
                })
        
        return cbbtc_pools
    
    except requests.RequestException as e:
        print(f"An error occurred while fetching data: {e}")
        return []

def convert_to_csv(data):
    csv_file = StringIO()
    fieldnames = ['date', 'chain', 'project', 'symbol', 'tvlUsd']
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()
    
    current_date = datetime.now().strftime('%Y-%m-%d')
    for item in data:
        item['date'] = current_date
        csv_writer.writerow(item)
    
    csv_data = csv_file.getvalue()
    csv_file.close()
    return csv_data

def upload_to_dune(csv_data, dune_api_key):
    dune_upload_url = "https://api.dune.com/api/v1/table/upload/csv"
    payload = json.dumps({
        "data": csv_data,
        "description": "CBBTC Pool Data",
        "table_name": "cbbtc_pool_data",
        "is_private": False
    })
    headers = {
        'Content-Type': 'application/json',
        'X-DUNE-API-KEY': dune_api_key
    }
    response = requests.post(dune_upload_url, headers=headers, data=payload)
    return response.text

def main():
    dune_api_key = "jc7EW9sSn8HfeveztGERQPHies3Qbem5"  # Replace with your actual Dune API key
    
    # Fetch CBBTC data
    cbbtc_data = fetch_cbbtc_data()
    
    if cbbtc_data:
        # Convert to CSV
        csv_data = convert_to_csv(cbbtc_data)
        
        # Upload to Dune
        result = upload_to_dune(csv_data, dune_api_key)
        print("Upload result:", result)
    else:
        print("No CBBTC pools found or there was an error fetching the data.")

if __name__ == "__main__":
    main()
