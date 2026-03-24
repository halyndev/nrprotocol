# Contributing to NRP

NRP is the universal protocol for AI-to-world control.

## The Protocol

NRP defines 4 things:

1. **Identity** — `nrp://scope/kind/name`
2. **Manifest** — Self-describing capabilities (JSON)
3. **Events** — Real-time push notifications
4. **Driver Interface** — `observe()`, `act()`, `shield_rules()`, `manifest()`

## SDK Development

```bash
cd sdk/python
pip install -e .
pytest
```

## Writing a Driver

See `examples/hello_ssh.py` for the minimal template.
A driver implements 4 methods.

## Specification Changes

Changes to the NRP spec (in `spec/`) require an RFC process:
1. Open an issue describing the change
2. Discuss with maintainers
3. Submit PR with spec changes + SDK implementation + tests

## License

MIT. See LICENSE for terms.

