# FuelSeal

**Local-first fuel usage, purchase, and consumption evidence sealer for field operators.**

Offline. Deterministic. Pay once. Compatible with QuantumGuard CONTRACT-v1, EquipmentSeal, TimesheetSeal, and the Operator Pages suite.

## Why FuelSeal?

Fuel is one of the largest variable costs and a frequent source of disputes, theft claims, and allocation errors on job sites.  
FuelSeal captures structured fuel purchase and dispense logs (source, liters, cost, asset linkage, receipts) and seals them into a client-verifiable QuantumGuard evidence bundle.

- No SaaS. No subscription. Runs completely offline after key setup.
- Clients (or their auditors) verify the pack with the free QuantumGuard verifier (`qg verify`).
- Pairs perfectly with EquipmentSeal (hours + fuel) for complete equipment evidence.
- Deterministic: same inputs → same sealed pack.

## Quick Start

```bash
# Recommended for real Ed25519 signatures
pip install cryptography

python3 src/fuelseal.py --demo
python3 src/fuelseal.py --json samples/fuel-001.json --out sealed-fuel.json
```

Verify the output with the QuantumGuard CLI (from the quantumguard repo):

```bash
qg verify sealed-fuel.json
```

Expected verdict: **PASS**.

## What you can sell

| SKU       | Price | Includes                                      |
|-----------|-------|-----------------------------------------------|
| Operator  | $39   | CLI + sample templates + key setup guide + 1-year email support |
| Command   | $129  | + batch mode + CSV/Excel export + reseller rights for client packs |
| Agency    | $349  | + white-label + multi-site key management + design partner onboarding |

Purchase / access: danpennic@gmail.com  
Or use the Operator Pages Stripe checkout flow.

Source remains free under Apache-2.0 OR MIT. Commercial Operator Pack sold separately.

## Stack Fit

- Python CLI (same family as EquipmentSeal, TimesheetSeal, DailySeal, etc.)
- Emits QuantumGuard CONTRACT-v1 bundles (Ed25519, deterministic canonical JSON)
- Local key storage (PEM)
- Designed to drop into the Operator Pages field stack

## License

Apache-2.0 OR MIT
