#!/usr/bin/env python3
"""
FuelSeal — local-first fuel usage, purchase, and consumption evidence sealer.
Emits QuantumGuard CONTRACT-v1 bundles.
"""
import argparse
import base64
import hashlib
import json
import sys
from pathlib import Path

try:
    from cryptography.hazmat.primitives.asymmetric import ed25519
    from cryptography.hazmat.primitives import serialization
    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False

def canonical_json(obj):
    """Deterministic JSON for hashing (sorted keys, no whitespace)."""
    return json.dumps(obj, sort_keys=True, separators=(',', ':')).encode('utf-8')

def create_bundle(payload_bytes, private_key=None):
    payload_b64 = base64.b64encode(payload_bytes).decode('ascii')
    payload_hash = hashlib.sha256(payload_bytes).hexdigest()
    bundle = {
        "version": "1",
        "payload": payload_b64,
        "payload_hash": payload_hash,
        "alg": "ed25519"
    }
    if private_key and HAS_CRYPTO:
        hash_bytes = bytes.fromhex(payload_hash)
        signature = private_key.sign(hash_bytes)
        bundle["signature"] = signature.hex()
        pub = private_key.public_key().public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        bundle["public_key"] = pub.hex()
    else:
        bundle["signature"] = "0" * 128
        bundle["public_key"] = "0" * 64
    return bundle

def main():
    parser = argparse.ArgumentParser(description="FuelSeal — seal fuel logs into QuantumGuard packs")
    parser.add_argument("--json", help="Input fuel JSON file")
    parser.add_argument("--out", default="sealed-fuel.json", help="Output bundle path")
    parser.add_argument("--demo", action="store_true", help="Run demo with sample data")
    parser.add_argument("--key", help="Path to Ed25519 private key PEM (optional)")
    args = parser.parse_args()

    if args.demo:
        data = {
            "job_id": "DEMO-FUEL-001",
            "date": "2026-11-06",
            "site": "Missouri Field Site A",
            "operator": "Field Op 1",
            "fuel_entries": [
                {
                    "type": "purchase",
                    "source": "Station A",
                    "liters": 200.0,
                    "cost_usd": 180.0,
                    "receipt_id": "RCPT-001",
                    "notes": "Diesel for excavator and generator"
                },
                {
                    "type": "dispense",
                    "asset_id": "EXC-4500",
                    "liters": 42.0,
                    "hours_linked": 7.5,
                    "notes": "Matches EquipmentSeal hours"
                }
            ],
            "total_purchased_liters": 200.0,
            "total_dispensed_liters": 42.0,
            "signature_note": "Fuel log sealed for client verification"
        }
        payload = canonical_json(data)
    elif args.json:
        with open(args.json, 'rb') as f:
            raw = f.read()
        data = json.loads(raw)
        payload = canonical_json(data)
    else:
        print("Provide --json or --demo", file=sys.stderr)
        sys.exit(1)

    priv = None
    if args.key and HAS_CRYPTO:
        with open(args.key, 'rb') as f:
            priv = serialization.load_pem_private_key(f.read(), password=None)

    bundle = create_bundle(payload, priv)
    Path(args.out).write_text(json.dumps(bundle, indent=2))
    print(f"Sealed to {args.out}")
    print("Verify with: qg verify", args.out)

if __name__ == "__main__":
    main()
