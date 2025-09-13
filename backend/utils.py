import hmac
import base64
import time
import hashlib
import os
from dotenv import load_dotenv
import http.client
import urllib.request
import urllib.parse
import json
from typing import Dict, Optional

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



def get_nonce() -> str:
   return str(int(time.time() * 1000))

def get_signature(private_key: str, data: str, nonce: str, path: str) -> str:
   return sign(
        private_key=private_key,
        message=path.encode() + hashlib.sha256(
            (nonce + data).encode()
        ).digest()
    )

def sign(private_key: str, message: bytes) -> str:
   return base64.b64encode(
        hmac.new(
            key=base64.b64decode(private_key),
            msg=message,
            digestmod=hashlib.sha512,
        ).digest()
    ).decode()