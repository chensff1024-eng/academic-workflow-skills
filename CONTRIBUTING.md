# Contributing

Contributions are welcome when they preserve the repository's local-first,
rights-safe boundaries.

1. Use synthetic metadata and manuscript briefs in tests and examples.
2. Do not add paywalled full text, downloaded documents, screenshots, private
   manuscripts, account data, or automation for login and submission systems.
3. Add or update tests before changing runtime behavior.
4. Run `python -B -m unittest discover -s tests -t . -p "test_*.py" -v`.
5. Run `python -B scripts/verify_release.py --root .`.
6. Explain provenance and any time-sensitive journal facts in the change.

By submitting a contribution, you agree that it is licensed under Apache-2.0.
