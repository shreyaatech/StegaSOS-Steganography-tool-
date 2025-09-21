from flask import Flask, request, jsonify
import json, os
from datetime import datetime

app = Flask(__name__)

def load_keys():
    path = os.path.join(os.path.dirname(__file__), "keys.json")
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f).get("keys", [])
    return { entry["key"]: { "expires": entry["expires"], "role": entry.get("role", "user") }
             for entry in raw if "key" in entry and "expires" in entry }

VALID_KEYS = load_keys()

@app.route("/verify", methods=["GET"])
def verify():
    api_key = request.headers.get("X-API-Key") or request.args.get("key")
    key_info = VALID_KEYS.get(api_key)
    if not key_info:
        return jsonify({ "valid": False, "reason": "Key not found" }), 401
    try:
        expires = datetime.fromisoformat(key_info["expires"])
    except ValueError:
        return jsonify({ "valid": False, "reason": "Invalid expiry format" }), 400
    if datetime.now() > expires:
        return jsonify({ "valid": False, "reason": "Key expired" }), 403
    return jsonify({ "valid": True, "role": key_info["role"], "expires": key_info["expires"] }), 200

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=False)
