import os
from dotenv import load_dotenv
import http.client
import urllib.request
import urllib.parse
import json
from utils import get_signature, get_nonce
from typing import Optional

load_dotenv()

KRAKEN_API_KEY = os.getenv('KRAKEN_PUBLIC_KEY')
KRAKEN_PRIVATE_KEY = os.getenv('KRAKEN_PRIVATE_KEY')

def request(method: str, path: str, query: Optional[dict] = None, body: dict = {}, environment: str = "https://api.kraken.com") -> http.client.HTTPResponse:
    url = environment + path

    query_str = ""
    if query is not None and len(query):
        query_str = "?" + urllib.parse.urlencode(query)
        url += query_str

    body['nonce'] = get_nonce()

    body_str = json.dumps(body)

    headers = {
        'Content-Type': 'application/json',
        'API-Key': KRAKEN_API_KEY,
        'API-Sign': get_signature(
            private_key=KRAKEN_PRIVATE_KEY, 
            data=query_str + body_str, 
            nonce=body['nonce'], 
            path=path
        ) 
    }

    req = urllib.request.Request(
        method=method,
        url=url,
        headers=headers,
        data=body_str.encode()
    )

    return urllib.request.urlopen(req)