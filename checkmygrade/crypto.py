import base64
from typing import Final

# DEMO-GRADE ONLY: This is NOT secure. Used solely to satisfy reversible requirement.
# Do NOT reuse for real credentials.

_SECRET_KEY: Final[bytes] = b"CHECKMYGRADE-DEMO-KEY-ONLY"


def _xor_bytes(data: bytes, key: bytes) -> bytes:
	if not key:
		raise ValueError("key must not be empty")
	out = bytearray()
	klen = len(key)
	for i, b in enumerate(data):
		out.append(b ^ key[i % klen])
	return bytes(out)


def encrypt_password(plain_text: str) -> str:
	data = plain_text.encode("utf-8")
	cipher = _xor_bytes(data, _SECRET_KEY)
	return base64.urlsafe_b64encode(cipher).decode("ascii")


def decrypt_password(encoded_cipher: str) -> str:
	cipher = base64.urlsafe_b64decode(encoded_cipher.encode("ascii"))
	plain = _xor_bytes(cipher, _SECRET_KEY)
	return plain.decode("utf-8")
