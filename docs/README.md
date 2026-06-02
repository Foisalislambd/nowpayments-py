# NOWPayments API documentation

Documentation for all NOWPayments SDK packages in this monorepo.

## Start here

| Document | Description |
|----------|-------------|
| **[FULL_API_REFERENCE.md](./FULL_API_REFERENCE.md)** | Complete reference: overview, SDK checklist, every endpoint from Postman |
| [API_DOCUMENTATION.md](./API_DOCUMENTATION.md) | Curated quick reference (payments, IPN summary) |
| [METHODS_CHECKLIST.md](./METHODS_CHECKLIST.md) | API route → `nowpayments-node` method mapping |
| [nowpayments-api-stubs.json](./nowpayments-api-stubs.json) | JSON stubs for tooling / tests |

## Raw Postman exports

Original exports live in **[raw/](./raw/)** (do not delete — used to regenerate `FULL_API_REFERENCE.md`).

## Regenerate full reference

From `nowpayments-node`:

```bash
python scripts/format_api_docs.py
```

## Official links

- [Postman — Production](https://documenter.getpostman.com/view/7907941/2s93JusNJt)
- [Postman — Sandbox](https://documenter.getpostman.com/view/7907941/T1LSCRHC)
- [Help Center](https://nowpayments.io/help/payments/api)
