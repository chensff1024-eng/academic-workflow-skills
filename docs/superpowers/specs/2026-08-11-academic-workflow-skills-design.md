# Academic Workflow Skills Public Series Design

## Goal

Publish one public, maintainable repository containing two complementary Codex Skills:

1. `cnki-literature-review` helps a researcher design CNKI searches, normalize user-supplied bibliographic exports, rank literature, build an evidence ledger, and draft an evidence-bounded literature review.
2. `world-history-submission-strategy` analyzes a manuscript and produces journal-fit, verification, sequencing, and pre-submission revision advice without submitting the manuscript.

The public acceptance object is the repository `chensff1024-eng/academic-workflow-skills`, not the two private source directories.

## Scope Lock

### In scope

- One monorepo at `E:\academic-workflow-skills`.
- Two separately installable Skill directories under `skills/`.
- Standard-library Python helpers for deterministic local processing.
- Synthetic examples and fixtures only.
- Apache-2.0 licensing for repository-owned material.
- Explicit third-party provenance, trademark, privacy, and platform-use boundaries.
- Automated tests, release verification, packaging, and an initial public GitHub release.
- Evidence records suitable for a later Codex for Open Source application.

### Non-goals

- Logging in to CNKI or any journal submission system.
- Reading browser cookies, controlling CAPTCHA, or automating paid-content downloads.
- Redistributing PDFs, CAJ files, paywalled full text, screenshots, session URLs, or private manuscripts.
- Sending submission emails, uploading manuscripts, clicking final-submit buttons, or claiming acceptance probability.
- Vendoring `cookjohn/cnki-skills`, the private reading-report implementation, or other third-party Skill trees.
- Modifying `E:\cnki-writing-skill` or `E:\submission-skill`.

## Repository Architecture

```text
academic-workflow-skills/
├── skills/
│   ├── cnki-literature-review/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   ├── scripts/
│   │   └── examples/
│   └── world-history-submission-strategy/
│       ├── SKILL.md
│       ├── references/
│       ├── scripts/
│       └── examples/
├── scripts/
│   ├── package_skills.py
│   └── verify_release.py
├── tests/
├── docs/release-evidence/
├── .github/workflows/ci.yml
├── README.md
├── LICENSE
├── NOTICE
├── THIRD_PARTY_NOTICES.md
├── SECURITY.md
└── CONTRIBUTING.md
```

Each Skill owns its runtime contract and references. Repository-level scripts only package and verify the distribution.

## CNKI Literature Review Data Flow

1. The Skill derives a transparent search plan from the research topic, timeframe, language, and inclusion criteria.
2. The user performs the search in an account and interface they are authorized to use.
3. The user supplies manually exported CSV/JSON bibliographic metadata or manually entered records.
4. Local scripts normalize and validate title, author, year, source, keywords, abstract, citation count, and a stable public locator when available.
5. Ranking uses explicit topic overlap, source filters, date windows, and optional citation signals.
6. The Skill builds an evidence ledger and literature-review outline. Draft prose may only use claims present in supplied abstracts or notes and must preserve uncertainty.

No runtime component accesses CNKI, browser state, account credentials, or downloadable documents.

## Submission Strategy Data Flow

1. Read a manuscript, abstract, outline, proposal, or title supplied by the user.
2. Extract topic, period, geography, evidence type, method, and scholarly conversation.
3. Query a dated local journal-fit matrix for a preliminary pool.
4. Verify time-sensitive claims through official journal or host-institution pages when web access is available.
5. Separate verified facts, editorial-fit inference, and unresolved information.
6. Return same-discipline and cross-disciplinary candidates, submission sequence, and three pre-submission revision priorities.

The Skill stops before all account, upload, email, payment, and final-submission actions.

## Safety and Rights Boundaries

- CNKI is a third-party trademark; the repository is unofficial and unaffiliated.
- User possession of an account does not authorize automation or redistribution.
- Inputs remain local unless the user explicitly chooses a permitted external tool.
- Generated outputs contain bibliographic metadata, user-provided excerpts, and analysis, not bundled source documents.
- Packaging fails when prohibited extensions, private run directories, credentials, browser-session code, or unapproved third-party trees are present.
- Journal information is a dated heuristic snapshot. Current indexing, submission rules, fees, review cycles, and contact details require official verification.

## Prior-Art Dispositions

| Candidate | Decision | Reused lesson | Rejected assumption |
| --- | --- | --- | --- |
| `cookjohn/cnki-skills` | Adapt | Clear separation of search, result parsing, detail inspection, and export stages | Browser automation, account/session access, download automation, and vendored source |
| Existing private `cnki-writing-skill` | Adapt | Candidate ranking, detail-first evidence, explicit downgrade states, one-shot report concept | Cookie-based direct fetch, PDFs, screenshots, real run artifacts, upstream mirrors, and private reading-report code |
| Existing private `submission-skill` | Adapt | Manuscript profiling, journal-fit matrix, evidence separation, and explicit downgrade wording | Mandatory automated CNKI access and any wording that could imply actual submission |
| OpenAI Codex Skill conventions | Adopt | Focused `SKILL.md`, progressive disclosure, scripts for deterministic work, and explicit testable contracts | Treating README presence or packaging success as user-visible acceptance |

## Acceptance Lock

The release is accepted only when all of the following are freshly verified:

- Both `SKILL.md` files have valid frontmatter and distinct trigger boundaries.
- CNKI sample input is synthetic and the real local processing entrypoint produces a review packet.
- Submission sample input produces a structured strategy without performing external submission actions.
- Repository tests pass from the repository root with Python bytecode disabled and temporary output under `.tmp/`.
- The release verifier reports no prohibited files, secret-like material, browser-cookie/download code, private absolute paths, or missing legal documents.
- Packaged archives contain only approved public files.
- GitHub remote visibility is public and its default branch content matches the verified local commit.
- A release-evidence record binds commit hash, test command, package hashes, remote URL, and known limitations.

## Failure Handling

- Invalid or incomplete bibliographic records are reported with record-level errors and are not silently repaired.
- Missing abstracts produce metadata-only evidence entries and cannot support synthesized scholarly claims.
- Missing live journal verification downgrades confidence and is displayed in the result.
- Packaging or publishing stops on any prohibited artifact or unresolved license/provenance item.

## Testing Strategy

- Contract tests validate Skill frontmatter, required safety language, trigger separation, and output schemas.
- Unit tests cover normalization, ranking, review-packet rendering, journal querying, and package inventory.
- Negative release tests inject prohibited filenames and code anchors and require the verifier to fail.
- Real-entrypoint tests execute both local CLIs against synthetic fixtures.
- A final remote check reads the GitHub repository after upload and compares the published commit.

## Design Self-Review

- No placeholders or unresolved architecture choices remain.
- The two Skills have independent entrypoints and a shared release gate only.
- The design preserves the requested literature-review and submission workflow while excluding account automation and restricted content.
- The user approved the monorepo name, target path, public visibility, Comet initialization, commits, and upload on 2026-08-11.
