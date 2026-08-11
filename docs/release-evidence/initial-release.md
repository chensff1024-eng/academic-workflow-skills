# Initial release evidence

Evidence captured: 2026-08-11T19:21:33+08:00

## Verified source commit

- Commit: `70050449994867a1635f9a880adf7f6dbe70b0ba`
- Branch: `main`
- Repository state after verification: clean
- Private prototype directories: not modified and not included

## Fresh verification

| Check | Command | Result |
| --- | --- | --- |
| Full test suite | `python -B -m unittest discover -s tests -t . -p "test_*.py" -v` | 23 tests, 0 failures, 0 errors |
| Release tree | `python -B scripts/verify_release.py --root .` | `RELEASE_VERIFY_OK scanned_files=36` |
| Literature workflow | `python -B skills/cnki-literature-review/scripts/literature_pipeline.py` with the synthetic example | `REVIEW_PACKET_OK records=2` |
| Submission strategy | `python -B skills/world-history-submission-strategy/scripts/query_matrix.py` with synthetic terms | `SUBMISSION_STRATEGY_OK candidates=6` |
| Packaging | `python -B scripts/package_skills.py --output-dir .tmp/dist` | Two deterministic archives produced |
| Text encoding | Strict UTF-8 read of public candidate files | 36 files readable; no BOM finding |
| Git whitespace | `git diff --check` | No findings |

All generated verification and package artifacts were written below `.tmp/`
and are excluded from the public tree.

## Package evidence

### `cnki-literature-review.zip`

- SHA-256: `f5b7d5a4ded6da8f298420b653e026f088e7fb289f7934d08686deacc0a47c89`
- Contains the Skill contract, evaluation cases, synthetic records, three
  references, the local metadata pipeline, Apache-2.0, NOTICE, and third-party
  notices.

### `world-history-submission-strategy.zip`

- SHA-256: `aa2a11930234b15b4880ba9eeddabce1abeb15327434ed2779991c0a0142ae2c`
- Contains the Skill contract, evaluation cases, synthetic manuscript brief,
  dated six-journal discovery matrix, evidence and output policies, local query
  helper, Apache-2.0, NOTICE, and third-party notices.

## Rights and safety disposition

- No real article, manuscript, screenshot, account data, session data, signed
  link, private run, or third-party source tree is included.
- The literature Skill handles user-supplied metadata locally and performs no
  login, CAPTCHA, browser-session, or document-download automation.
- The submission Skill performs no login, upload, email, payment, or final
  submission action.
- Journal fit is a dated inference. Current instructions, indexing, fees,
  review cycle, contacts, and AI policies remain subject to official recheck.
- The project is unofficial and unaffiliated with the named services,
  publishers, institutions, and OpenAI.

## External-source checks

- [CNKI membership agreement](https://wap.oversea.cnki.net/cn/member/agreement.html),
  effective 2024-11-01, was used to set the no-automation and
  no-redistribution boundary.
- [OpenAI Codex use cases](https://developers.openai.com/codex/use-cases) was
  used only as public workflow-format guidance.
- Official journal and host-institution sources are recorded in the dated local
  matrix and the prior-art ledger.

## Publication state at capture time

The local release content is verified and committed. The public GitHub
repository had not yet been created at this capture point. Remote visibility,
published commit identity, and public file inventory must be appended only
after they are observed on the remote service.

## Known limitations

- Initial release with no demonstrated stars, downloads, external users,
  issues, pull requests, or maintenance history.
- The release scanner covers named high-risk patterns and artifact classes; it
  does not replace human legal, privacy, or content review.
- The journal matrix is intentionally small and theme-led. It is not a complete
  journal directory and does not claim acceptance probability.
