from dataclasses import dataclass, field
from typing import List, Optional, Dict

@dataclass
class Token:
    
    # Core market data
    symbol: str
    name: str
    price: float
    volume_24h: float
    market_cap: float
    circulating_supply: float
    change_24h: float        # absolute price change
    change_percent_24h: float
    rank: int                # CMC or CoinGecko rank
    
    # Portfolio-specific info
    holding_amount: float = 0.0    # how much user owns (in token units)
    weight: float = 0.0      # % of total portfolio (to be computed)
    
    # Classification
    sector: str = "Other"    # Layer1, DeFi, Gaming, Memecoin, Stablecoin, etc.
    risk_level: str = "Mid"  # Low/Medium/High (blue chip vs alt vs microcap)
    is_stablecoin: bool = False
    
    # RAG / knowledge augmentation
    news_refs: List[str] = field(default_factory=list)   # doc IDs in ChromaDB
    embedding_id: Optional[str] = None                  # ID to vector store
    metadata: Dict = field(default_factory=dict)        # any API extras