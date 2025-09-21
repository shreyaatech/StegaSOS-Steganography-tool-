# 🔐 StegaSOS / StegaSecure

**StegaSOS** is a secure, encrypted steganography platform that hides sensitive messages inside images. Designed for ethical, privacy-focused communication, it combines AES encryption, passphrase protection, geotagging, API key verification, and sender-controlled revocation — all wrapped in a sleek, cyber-themed interface.

---

## 🚀 Features

- 🖼️ **Image-Based Steganography**  
  Embed encrypted messages inside PNG/JPG images using LSB encoding.

- 🔐 **AES Encryption with Passphrase**  
  Messages are encrypted using a passphrase-derived key via PBKDF2 + Fernet.

- 📍 **Geotagging**  
  Automatically captures sender’s location and embeds it in the encrypted payload.

- 🔑 **API Key Verification**  
  Optional access control via a Flask backend that validates keys with expiration and roles.

- 🧨 **Revoke Access**  
  Strip hidden data from stego images post-send, converting them into clean images.

- 👁️ **Google Cloud Vision Integration** *(Optional)*  
  Analyze cover images for safety using SafeSearch before encoding.

---

## 🛠 Tech Stack

| Component     | Technology         |
|---------------|--------------------|
| Frontend UI   | Streamlit          |
| Encryption    | Python `cryptography` (AES via Fernet) |
| Steganography | Python `Pillow` + `numpy` |
| Geotagging    | `geocoder` (IP-based location) |
| Backend API   | Flask (API key verification) |
| Image Safety  | Google Cloud Vision API *(optional)* |
| Deployment    | Local / Streamlit Cloud / GitHub |

---

## 📁 Project Structure

