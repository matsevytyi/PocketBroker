import hmac
import base64
import time
import hashlib

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