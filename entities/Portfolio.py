from dataclasses import dataclass, field
from typing import List, Optional, Dict
from sentence_transformers import SentenceTransformer
from entities.Token import Token
import numpy as np


# TODO: move to yaml
SECTORS = ["Layer1", "DeFi", "Gaming", "Memecoin", "Stablecoin", "Noname"]

from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

@dataclass
class Portfolio:
    tokens: List[Token]
    total_profit_loss: float = 0.0
    
    def find_similar(self, token: Token, top_k=5) -> list[Token]:
        """
        Find top-k most similar tokens (by embedding) from this portfolio.
        """
        # compute query vector
        query_vec = token.embedded_sector

        # compute all portfolio vectors
        all_vecs = [token_vector(t) for t in self.tokens]

        sims = cosine_similarity([query_vec], all_vecs)[0]

        # sort by similarity (skip self if in portfolio)
        sorted_idx = sims.argsort()[::-1]

        results = []
        for idx in sorted_idx:
            candidate = self.tokens[idx]
            if candidate.symbol == token.symbol:  # skip self
                continue
            results.append(candidate)
            if len(results) >= top_k:
                break
        return results


    def stablecoin_ratio(self):
        total_value = sum(t.holding_amount * t.price for t in self.tokens)
        if total_value == 0:
            return 0.0
        stable_value = sum(t.holding_amount * t.price for t in self.tokens if t.is_stablecoin)
        return stable_value / total_value

    def sector_allocation(self):
        total_value = sum(t.holding_amount * t.price for t in self.tokens)
        if total_value == 0:
            return {}
        alloc = {}
        for t in self.tokens:
            val = t.holding_amount * t.price
            alloc[t.sector] = alloc.get(t.sector, 0) + val
        return {k: v/total_value for k, v in alloc.items()}

    def compute_hhi(self):
        """Herfindahl–Hirschman Index of portfolio concentration."""
        total_value = sum(t.holding_amount * t.price for t in self.tokens)
        if total_value == 0:
            return 0.0
        weights = [(t.holding_amount * t.price) / total_value for t in self.tokens if t.holding_amount > 0]
        return sum(w**2 for w in weights)



def local_embed(text: str) -> list[float]:
    return model.encode(text).tolist()

def one_hot(value: str, vocab: list[str]) -> np.ndarray:
    
    vec = np.zeros(len(vocab))
    
    if value in vocab:
        vec[vocab.index(value)] = 1.0
        
    return vec

def embed_categories(categories: list[str], text_embedding_fn) -> np.ndarray:
    """Embed each category separately, then average them."""
    
    if not categories or not text_embedding_fn:
        return np.zeros(768)  # assume embedding dim = 768, adjust to your model
    
    cat_vecs = [text_embedding_fn(cat) for cat in categories]
    
    return np.mean(cat_vecs, axis=0)

def token_vector(token: Token, text_embedding_fn=None) -> np.ndarray:

    sector_vec = one_hot(token.sector, SECTORS)
    stable_vec = np.array([1.0 if token.is_stablecoin else 0.0])

    cat_vec = embed_categories(token.metadata.get("categories", []), text_embedding_fn)
    
    desc_vec = np.zeros_like(cat_vec)
    if text_embedding_fn:
        desc = token.metadata.get("description", "")
        if desc:
            desc_vec = text_embedding_fn(desc)

    return np.concatenate([ sector_vec, stable_vec, cat_vec, desc_vec])