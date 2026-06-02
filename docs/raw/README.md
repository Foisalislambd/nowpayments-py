# Postman export (raw)

Unedited exports from the official NOWPayments Postman documentation. Use these as the source of truth when verifying parameters, examples, and edge cases.

| File | Notes |
|------|--------|
| [copied-docs.md](./copied-docs.md) | Main production API export |
| [copied-docs-2.md](./copied-docs-2.md) | Sandbox / alternate sections |
| [copied-docs-3.md](./copied-docs-3.md) | Extended export (payouts, custody, IPN) |

Do not edit these files for SDK behavior — update the formatted docs in the parent `docs/` folder and re-run:

```bash
python scripts/format_api_docs.py
```

**Formatted output:** [../FULL_API_REFERENCE.md](../FULL_API_REFERENCE.md)
