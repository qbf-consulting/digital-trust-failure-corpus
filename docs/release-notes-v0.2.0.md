# Digital Trust Failure Corpus v0.2.0

## Purpose

v0.2.0 expands the corpus with a bounded authority-at-material-commitment tranche. It addresses a recurring agentic-system failure: treating identity, signature validity, capability, reputation, or earlier-session authorization as though it proves current authority for the exact consequential action another party is asked to rely upon.

## Added cases

- **DTF-013** — valid signature mistaken for commitment authority.
- **DTF-014** — expired mandate accepted at commitment.
- **DTF-015** — authority limit exceeded during iterative action.
- **DTF-016** — revocation ignored during an active agent interaction.
- **DTF-017** — approval bound to the wrong or stale action.
- **DTF-018** — reputation or capability substituted for authority.
- **DTF-019** — historical commitment authority cannot be reconstructed.

Each case is technology-neutral, includes explicit evidence requirements and falsification conditions, and prohibits PASS where the failure proposition is present.

## Compatibility

The machine-readable failure-case contract remains schema **v0.1.0**. No new domain, failure-class, disposition, or evidence-category vocabulary was required. Existing DTF-001 through DTF-012 entries are unchanged.

Repository release version, schema version, and individual case versions are distinct lifecycle dimensions. A corpus release may add cases without forcing an otherwise unchanged schema to acquire a new identifier.

## Assurance boundary

The corpus remains **evidence, not authority**. These cases do not define contractual validity, a universal authorization protocol, a negotiation state machine, or a required cryptographic proof system.

The central testable proposition is narrower: a relying system must not create PASS from identity or signature alone when current, action-specific principal-derived authority is required.

## Reproduce validation

```bash
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python tools/validate.py
```

A green result establishes repository/schema invariants, not substantive correctness or ecosystem-wide applicability.
