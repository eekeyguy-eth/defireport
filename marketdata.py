import requests
import json
import csv
from io import StringIO
from datetime import datetime

def fetch_coingecko_data(api_key):
    url = "https://pro-api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "ids": "ethereum,solana,the-open-network,cardano,dogecoin,avalanche-2,chainlink,polkadot,uniswap,near,sui,pepe,bittensor,internet-computer,polygon-ecosystem-token,immutable-x,aave,render-token,filecoin,injective-protocol,optimism,maker,arweave,sei-network,celestia,jupiter-exchange-solana,lido-dao,ondo-finance,popcat,beam-2,nervos-network,flare-networks,starknet,pendle,aerodrome-finance,pancakeswap-token,layerzero,zksync,mog-coin,axelar",
        "price_change_percentage": "24h,7d,30d"
    }
    headers = {
        'accept': 'application/json',
        'x-cg-pro-api-key': api_key
    }
    response = requests.get(url, params=params, headers=headers)
    return response.json()

def extract_required_data(json_data):
    extracted_data = []
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    for item in json_data:
        extracted_item = {
            'date': current_date,
            'symbol': item['symbol'],
            'current_price': item['current_price'],
            'market_cap': item['market_cap'],
            'fully_diluted_valuation': item.get('fully_diluted_valuation', 'N/A'),
            'total_volume': item['total_volume'],
            'ath_change_percentage': item['ath_change_percentage'],
            'price_change_percentage_24h_in_currency': item.get('price_change_percentage_24h_in_currency', 'N/A'),
            'price_change_percentage_7d_in_currency': item.get('price_change_percentage_7d_in_currency', 'N/A'),
            'price_change_percentage_30d_in_currency': item.get('price_change_percentage_30d_in_currency', 'N/A')
        }
        extracted_data.append(extracted_item)
    
    return extracted_data

def convert_to_csv(extracted_data):
    csv_file = StringIO()
    fieldnames = ['date', 'symbol', 'current_price', 'market_cap', 'fully_diluted_valuation', 'total_volume', 'ath_change_percentage', 'price_change_percentage_24h_in_currency', 'price_change_percentage_7d_in_currency', 'price_change_percentage_30d_in_currency']
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()
    csv_writer.writerows(extracted_data)
    csv_data = csv_file.getvalue()
    csv_file.close()
    return csv_data

def upload_to_dune(csv_data, dune_api_key):
    dune_upload_url = "https://api.dune.com/api/v1/table/upload/csv"
    payload = json.dumps({
        "data": csv_data,
        "description": "Market Data",
        "table_name": "market_data",
        "is_private": False
    })
    headers = {
        'Content-Type': 'application/json',
        'X-DUNE-API-KEY': dune_api_key
    }
    response = requests.post(dune_upload_url, headers=headers, data=payload)
    print(response.text)

def main():
    coingecko_api_key = "CG-ep7WBgRCGeDria6EeL1jkPot"
    dune_api_key = "p0RZJpTPCUn9Cn7UTXEWDhalc53QzZXV"  # Replace with your actual Dune API key

    # Fetch CoinGecko data
    json_data = fetch_coingecko_data(coingecko_api_key)
    
    # Extract required data
    extracted_data = extract_required_data(json_data)
    
    # Convert to CSV
    csv_data = convert_to_csv(extracted_data)
    
    # Upload to Dune
    upload_to_dune(csv_data, dune_api_key)

if __name__ == "__main__":
    main()
