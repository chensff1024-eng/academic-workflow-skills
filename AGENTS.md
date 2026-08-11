# Repository Rules

- This repository contains public, local-first academic workflow Skills.
- Use synthetic fixtures only. Never add private manuscripts, full-text articles, screenshots, session data, credentials, signed links, or account identifiers.
- The CNKI Skill must not automate login, CAPTCHA, cookies, browser sessions, or document downloads.
- The submission-strategy Skill must not log in, upload, email, pay, or submit on a user's behalf.
- Keep runtime code dependency-free and network-free unless a future change is separately reviewed and documented.
- Write generated artifacts only below `.tmp/`.
- Run the full test suite and `scripts/verify_release.py` before packaging or publication.
