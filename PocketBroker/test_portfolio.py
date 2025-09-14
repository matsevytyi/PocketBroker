from entities.Token import Token
from entities.Portfolio import Portfolio
from RAG.onchain_metrics import fetch_token_from_coingecko


# assess portfolio

tokens = [
    Token(symbol='ETH', name='Ethereum', price=4660.03, volume_24h=32341962383, market_cap=562303192886, circulating_supply=120704705.5174823, change_24h=23.260529, change_percent_24h=0.50165, rank=2, holding_amount=0.0, weight=0.0, sector='Layer1', is_stablecoin=False, news_refs=[], embedding_id=None, metadata={'categories': ['Smart Contract Platform', 'Layer 1 (L1)', 'Ethereum Ecosystem', 'FTX holding_amount', 'Multicoin Capital Portfolio', 'Proof of Stake (PoS)', 'Alameda Research Portfolio', 'Andreessen Horowitz (a16z) Portfolio', 'GMCI Layer 1 Index', 'GMCI 30 Index', 'Delphi Ventures Portfolio', 'Galaxy Digital Portfolio', 'GMCI Index', 'World Liberty Financial Portfolio', 'Coinbase 50 Index'], 'homepage': 'https://www.ethereum.org/', 'blockchain_site': 'https://etherscan.io/', 'genesis_date': '2015-07-30'}), 
    Token(symbol='BTC', name='Bitcoin', price=115953, volume_24h=33029342892, market_cap=2310033021527, circulating_supply=19920381.0, change_24h=-169.2068273357, change_percent_24h=-0.14571, rank=1, holding_amount=0.0, weight=0.0, sector='Layer1', is_stablecoin=False, news_refs=[], embedding_id=None, metadata={'categories': ['Smart Contract Platform', 'Layer 1 (L1)', 'FTX holding_amount', 'Proof of Work (PoW)', 'Bitcoin Ecosystem', 'GMCI 30 Index', 'GMCI Index', 'Coinbase 50 Index'], 'homepage': 'http://www.bitcoin.org', 'blockchain_site': 'https://mempool.space/', 'genesis_date': '2009-01-03'}), 
    Token(symbol='SOL', name='Solana', price=239.81, volume_24h=8354197772, market_cap=130105355611, circulating_supply=542444938.2873168, change_24h=-0.1488619518528, change_percent_24h=-0.06204, rank=5, holding_amount=0.05, weight=0.0, sector='Layer1', is_stablecoin=False, news_refs=[], embedding_id=None, metadata={'categories': ['Smart Contract Platform', 'Solana Ecosystem', 'Layer 1 (L1)', 'Alleged SEC Securities', 'FTX holding_amount', 'Multicoin Capital Portfolio', 'Proof of Stake (PoS)', 'Alameda Research Portfolio', 'Andreessen Horowitz (a16z) Portfolio', 'GMCI Layer 1 Index', 'GMCI 30 Index', 'Delphi Ventures Portfolio', 'GMCI Index', 'Polychain Capital Portfolio', 'Made in USA', 'Coinbase 50 Index'], 'homepage': 'https://solana.com/', 'blockchain_site': 'https://solscan.io/', 'genesis_date': None}), 
    Token(symbol='DOGE', name='Dogecoin', price=0.288179, volume_24h=8956193850, market_cap=43514242701, circulating_supply=150924576383.7052, change_24h=0.01690701, change_percent_24h=6.2325, rank=8, holding_amount=0.0, weight=0.0, sector='Layer1', is_stablecoin=False, news_refs=[], embedding_id=None, metadata={'categories': ['Smart Contract Platform', 'Meme', 'Dog-Themed', 'Elon Musk-Inspired', 'Proof of Work (PoW)', 'GMCI Meme Index', 'GMCI 30 Index', 'GMCI Index', 'Coinbase 50 Index', '4chan-Themed'], 'homepage': 'http://dogecoin.com/', 'blockchain_site': 'https://blockchair.com/dogecoin', 'genesis_date': '2013-12-08'}), 
    Token(symbol='USDT', name='Tether', price=1.001, volume_24h=95042259789, market_cap=170088737642, circulating_supply=170001696466.3275, change_24h=-0.000183914326584, change_percent_24h=-0.01838, rank=4, holding_amount=1.0, weight=0.0, sector='Stablecoin', is_stablecoin=False, news_refs=[], embedding_id=None, metadata={'categories': ['Stablecoins', 'USD Stablecoin', 'Solana Ecosystem', 'Avalanche Ecosystem', 'Near Protocol Ecosystem', 'Celo Ecosystem', 'Ethereum Ecosystem', 'Kaia Ecosystem', 'Aptos Ecosystem', 'FTX holding_amount', 'TON Ecosystem', 'Tron Ecosystem', 'Kava Ecosystem', 'Fiat-backed Stablecoin', 'World Liberty Financial Portfolio'], 'homepage': 'https://tether.to/', 'blockchain_site': 'https://etherscan.io/token/0xdac17f958d2ee523a2206206994597c13d831ec7', 'genesis_date': None}), 
    Token(symbol='UNI', name='Uniswap', price=10.1, volume_24h=345860784, market_cap=6068720735, circulating_supply=600483073.71, change_24h=0.02596092, change_percent_24h=0.25768, rank=36, holding_amount=0.0, weight=0.0, sector='DeFi', is_stablecoin=False, news_refs=[], embedding_id=None, metadata={'categories': ['Decentralized Exchange (DEX)', 'Exchange-based Tokens', 'Decentralized Finance (DeFi)', 'Yield Farming', 'Automated Market Maker (AMM)', 'BNB Chain Ecosystem', 'Avalanche Ecosystem', 'Polygon Ecosystem', 'Near Protocol Ecosystem', 'Gnosis Chain Ecosystem', 'Harmony Ecosystem', 'Arbitrum Ecosystem', 'Ethereum Ecosystem', 'Optimism Ecosystem', 'Paradigm Portfolio', 'Coinbase Ventures Portfolio', 'Index Coop Defi Index', 'Andreessen Horowitz (a16z) Portfolio', 'Energi Ecosystem', 'Sora Ecosystem', 'Huobi ECO Chain Ecosystem', 'GMCI DeFi Index', 'GMCI 30 Index', 'Blockchain Capital Portfolio', 'GMCI Index', 'Polychain Capital Portfolio', 'Made in USA', 'Unichain Ecosystem', 'Coinbase 50 Index', 'Governance'], 'homepage': 'https://uniswap.org/', 'blockchain_site': 'https://etherscan.io/token/0x1f9840a85d5af5bf1d1762f925bdaddc4201f984', 'genesis_date': None},),
    ]

portfolio = Portfolio(tokens)

# Sector Allocation - gives immediate insights about the composition of the portfolio
print("Sector Allocation Before", portfolio.sector_allocation())

# HHI - gives an estimate of the concentration of the portfolio (closer to the one - more concentrated)
print("HHI Before", portfolio.compute_hhi())

# lets say user wants to hold 0.69 of TrumpCoin
trump = fetch_token_from_coingecko("trumpcoin")
trump.holding_amount = 6900
tokens.append(trump)

portfolio = Portfolio(tokens)

# Sector Allocation - gives immediate insights about the composition of the portfolio
print("Sector Allocation After", portfolio.sector_allocation())

# HHI - gives an estimate of the concentration of the portfolio (closer to the one - more concentrated)
print("HHI After", portfolio.compute_hhi())