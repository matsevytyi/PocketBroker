import requests
from typing import Optional

from entities.Token import Token

COINGECKO_API = "https://api.coingecko.com/api/v3"

def fetch_token_from_coingecko(coin_id: str, holdings: float = 0.0) -> Optional[Token]:
    url = f"{COINGECKO_API}/coins/{coin_id}"
    params = {
        "localization": "false",
        "tickers": "false",
        "market_data": "true",
        "community_data": "false",
        "developer_data": "false",
        "sparkline": "false"
    }
    resp = requests.get(url, params=params)
    if resp.status_code != 200:
        print(f"Error fetching {coin_id}: {resp.text}")
        return None
    
    data = resp.json()
    m = data["market_data"]
    
    token = Token(
        symbol=data["symbol"].upper(),
        name=data["name"],
        price=m["current_price"]["usd"],
        volume_24h=m["total_volume"]["usd"],
        market_cap=m["market_cap"]["usd"],
        circulating_supply=m.get("circulating_supply", 0.0),
        change_24h=m["price_change_24h"],
        change_percent_24h=m["price_change_percentage_24h"],
        rank=data.get("market_cap_rank", -1),
        holdings=holdings,
    )
    
    # classification from categories
    categories = data.get("categories", [])
    if token.is_stablecoin is False:
        if categories:
            token.sector = map_to_sector(categories, token.symbol)
    
    # metadata fallback
    token.metadata = {
        "categories": categories,
        "homepage": data.get("links", {}).get("homepage", [None])[0],
        "blockchain_site": data.get("links", {}).get("blockchain_site", [None])[0],
        "genesis_date": data.get("genesis_date")
    }
    
    return token

def map_to_sector(tags, symbol):
    SECTOR_MAP = {
        "Layer 1": "Layer1",
        "L1": "Layer1",
        "Smart Contract Platform": "Layer1",
        "Layer 2": "Layer2",
        "L2": "Layer2",
        "DeFi": "DeFi",
        "Lending/Borrowing": "DeFi",
        "DEX": "DeFi",
        "Gaming": "Gaming",
        "GameFi": "Gaming",
        "NFT": "Gaming",
        "Meme": "Memecoin",
    }
    
    if symbol.upper() in ["USDT", "USDC", "DAI", "BUSD", "TUSD"]:
        return "Stablecoin"
    
    for tag in tags:
        for key, sector in SECTOR_MAP.items():
            if key.lower() in tag.lower():
                return sector
    return "Noname"