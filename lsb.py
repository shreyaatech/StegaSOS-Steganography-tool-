from PIL import Image
import numpy as np

def _bytes_to_bits(data: bytes) -> np.ndarray:
    return np.unpackbits(np.frombuffer(data, dtype=np.uint8))

def _bits_to_bytes(bits: np.ndarray) -> bytes:
    return np.packbits(bits).tobytes()

def embed(image: Image.Image, payload: bytes) -> Image.Image:
    img = image.convert("RGB")
    arr = np.array(img)
    flat = arr.flatten()
    bits = _bytes_to_bits(payload)
    if len(bits) > len(flat):
        raise ValueError("Payload too large for this image.")
    flat[:len(bits)] &= 0b11111110
    flat[:len(bits)] |= bits
    return Image.fromarray(flat.reshape(arr.shape).astype(np.uint8))

def extract(image: Image.Image) -> bytes:
    img = image.convert("RGB")
    arr = np.array(img)
    flat = arr.flatten()
    header_bits = flat[:64] & 1
    header_bytes = _bits_to_bytes(header_bits)
    if len(header_bytes) < 8 or header_bytes[:4] != b"STEG":
        raise ValueError("No valid stego payload found.")
    total_len = int.from_bytes(header_bytes[4:8], "big")
    if total_len == 0:
        raise ValueError("Payload has been revoked or is empty.")
    total_bits = (8 + total_len) * 8
    if total_bits > len(flat):
        raise ValueError("Image does not contain full payload.")
    return _bits_to_bytes(flat[:total_bits] & 1)
