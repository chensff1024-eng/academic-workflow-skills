# Academic Workflow Skills Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build, verify, and publish a rights-safe monorepo containing a CNKI literature-review Skill and a world-history submission-strategy Skill.

**Architecture:** Each Skill owns a standalone runtime contract and deterministic standard-library helpers. Repository-level verification scans legal documents, distribution contents, prohibited artifacts, and risky automation anchors before packaging or publication.

**Tech Stack:** Markdown Skill contracts, Python 3.11+ standard library, `unittest`, GitHub Actions, Git, OpenSpec.

## Global Constraints

- Do not modify `E:\cnki-writing-skill` or `E:\submission-skill`.
- Do not include real PDFs, CAJ files, screenshots, parsed full text, account information, cookies, signed URLs, private manuscripts, or private run artifacts.
- Do not automate CNKI login, CAPTCHA, browser sessions, or downloads.
- Do not log in to, upload to, email, or submit through journal systems.
- Use only synthetic fixtures in the public repository.
- Use strict UTF-8 without BOM for text files.
- Keep generated test, package, and verification artifacts under `E:\academic-workflow-skills\.tmp`.
- Commits and public upload are authorized for this repository only.

---

### Task 1: Repository Contract and Release Gate

**Files:**
- Create: `AGENTS.md`
- Create: `.gitignore`
- Create: `LICENSE`
- Create: `NOTICE`
- Create: `THIRD_PARTY_NOTICES.md`
- Create: `SECURITY.md`
- Create: `CONTRIBUTING.md`
- Create: `tests/test_release_contract.py`
- Create: `scripts/verify_release.py`

**Interfaces:**
- Consumes: repository root path.
- Produces: `scan_repository(root: Path) -> list[str]` and CLI exit code 0 only for a publishable tree.

- [ ] **Step 1: Write failing contract tests**

Test required legal files, forbidden extensions and directories, forbidden automation anchors, developer-machine absolute paths, and secret-like assignments.

- [ ] **Step 2: Run the focused test and verify RED**

Run: `python -B -m unittest tests.test_release_contract -v`

Expected: FAIL because the release verifier and legal contract files do not exist.

- [ ] **Step 3: Implement the minimal release verifier and repository policy files**

The verifier recursively inspects tracked-candidate files, skips `.git` and `.tmp`, and emits one line per violation. It rejects `.pdf`, `.caj`, screenshots, `runs`, `dist-check`, `__pycache__`, `Storage.getCookies`, `Browser.setDownloadBehavior`, direct download fetch anchors, obvious tokens/passwords, and private absolute paths.

- [ ] **Step 4: Run the focused test and verify GREEN**

Run: `python -B -m unittest tests.test_release_contract -v`

Expected: all release-contract tests pass.

### Task 2: CNKI Literature Review Skill

**Files:**
- Create: `skills/cnki-literature-review/SKILL.md`
- Create: `skills/cnki-literature-review/references/input-contract.md`
- Create: `skills/cnki-literature-review/references/output-contract.md`
- Create: `skills/cnki-literature-review/references/search-playbook.md`
- Create: `skills/cnki-literature-review/scripts/literature_pipeline.py`
- Create: `skills/cnki-literature-review/examples/sample-records.json`
- Create: `tests/test_cnki_literature_review.py`

**Interfaces:**
- Consumes: UTF-8 JSON or CSV bibliographic records supplied by the user.
- Produces: `normalize_record(raw: dict) -> dict`, `rank_records(records: list[dict], topic_terms: list[str]) -> list[dict]`, and `render_review_packet(records: list[dict], topic: str) -> str`.

- [ ] **Step 1: Write failing normalization, ranking, safety, and CLI tests**

Tests require deterministic ordering, rejection of records without titles, metadata-only labeling when abstracts are absent, no source-text invention, and a generated Markdown evidence ledger.

- [ ] **Step 2: Run the focused test and verify RED**

Run: `python -B -m unittest tests.test_cnki_literature_review -v`

Expected: FAIL because the public Skill and pipeline do not exist.

- [ ] **Step 3: Implement the minimal local pipeline and Skill contract**

The CLI accepts `--input`, `--topic`, `--output`, and optional `--terms`. It never opens a network connection. Ranking combines case-insensitive term overlap across title, keywords, and abstract with bounded citation and recency tie-breakers. Rendering labels every evidence row as abstract-backed or metadata-only.

- [ ] **Step 4: Run the focused test and verify GREEN**

Run: `python -B -m unittest tests.test_cnki_literature_review -v`

Expected: all CNKI literature-review tests pass.

### Task 3: World-History Submission Strategy Skill

**Files:**
- Create: `skills/world-history-submission-strategy/SKILL.md`
- Create: `skills/world-history-submission-strategy/references/journal-matrix.json`
- Create: `skills/world-history-submission-strategy/references/evidence-policy.md`
- Create: `skills/world-history-submission-strategy/references/output-contract.md`
- Create: `skills/world-history-submission-strategy/scripts/query_matrix.py`
- Create: `skills/world-history-submission-strategy/examples/sample-manuscript-brief.md`
- Create: `tests/test_submission_strategy.py`

**Interfaces:**
- Consumes: topic terms and a repository-owned dated journal-fit matrix.
- Produces: `query_journals(matrix: dict, terms: list[str]) -> list[dict]` and a CLI JSON result containing evidence date, fit reasons, unresolved dynamic facts, and no submission action.

- [ ] **Step 1: Write failing matrix, ranking, output-boundary, and CLI tests**

Tests require a snapshot date, provenance class, journal-form distinction, deterministic fit scoring, dynamic-fact warnings, and explicit no-submission language.

- [ ] **Step 2: Run the focused test and verify RED**

Run: `python -B -m unittest tests.test_submission_strategy -v`

Expected: FAIL because the public submission Skill and matrix do not exist.

- [ ] **Step 3: Implement the minimal matrix query and Skill contract**

The matrix stores stable editorial-fit heuristics only. The Skill requires official-site verification for current indexing, submission instructions, fees, review cycles, and contacts. The runtime output separates verified facts, heuristic fit, and unresolved information.

- [ ] **Step 4: Run the focused test and verify GREEN**

Run: `python -B -m unittest tests.test_submission_strategy -v`

Expected: all submission-strategy tests pass.

### Task 4: Packaging, CI, and Series Documentation

**Files:**
- Create: `scripts/package_skills.py`
- Create: `tests/test_packaging.py`
- Create: `.github/workflows/ci.yml`
- Create: `README.md`
- Create: `docs/release-evidence/prior-art-ledger.md`

**Interfaces:**
- Consumes: verified repository tree.
- Produces: two deterministic ZIP archives under `.tmp/dist/` and SHA-256 output.

- [ ] **Step 1: Write failing package-inventory and cross-link tests**

Tests require one archive per Skill, required files in each archive, exclusion of caches and private artifacts, series cross-links, and release-verifier execution before packaging.

- [ ] **Step 2: Run the focused test and verify RED**

Run: `python -B -m unittest tests.test_packaging -v`

Expected: FAIL because packaging and series documentation do not exist.

- [ ] **Step 3: Implement packaging, CI, README, and prior-art ledger**

CI runs the full `unittest` suite and release verifier with bytecode disabled. README documents installation, the two-stage research workflow, non-affiliation, rights boundaries, and contribution entrypoints.

- [ ] **Step 4: Run the focused test and verify GREEN**

Run: `python -B -m unittest tests.test_packaging -v`

Expected: all packaging tests pass.

### Task 5: Full Verification and Local Release Evidence

**Files:**
- Create: `docs/release-evidence/initial-release.md`

**Interfaces:**
- Consumes: repository commit, test output, verifier output, package hashes.
- Produces: a human-readable evidence record bound to exact commands and hashes.

- [ ] **Step 1: Run the full suite from the real repository root**

Run: `python -B -m unittest discover -s tests -p "test_*.py" -v`

Expected: zero failures and zero errors.

- [ ] **Step 2: Run the release verifier**

Run: `python -B scripts/verify_release.py --root .`

Expected: `RELEASE_VERIFY_OK` with the scanned-file count.

- [ ] **Step 3: Package both Skills**

Run: `python -B scripts/package_skills.py --output-dir .tmp/dist`

Expected: two ZIP paths and two SHA-256 values.

- [ ] **Step 4: Inspect package contents and write the evidence record**

Record commit hash, test count, verifier count, package inventory and hashes, known platform boundaries, and the unverified remote state before upload.

### Task 6: GitHub Publication and Remote Verification

**Files:**
- Update: `docs/release-evidence/initial-release.md`

**Interfaces:**
- Consumes: verified local commit and current logged-in GitHub account `chensff1024-eng`.
- Produces: public repository `https://github.com/chensff1024-eng/academic-workflow-skills` and verified remote evidence.

- [ ] **Step 1: Commit the verified repository**

Run: `git status --short`, then stage and commit only the reviewed public files.

Expected: a clean worktree at the verified commit.

- [ ] **Step 2: Create the public GitHub repository and push `main`**

Use the authorized GitHub account and preserve the local commit hash.

- [ ] **Step 3: Verify the remote default branch and public visibility**

Read the public repository page and compare the published commit and critical file inventory with the local release evidence.

- [ ] **Step 4: Finalize release evidence and publish the evidence update**

Record the remote URL, public visibility check, published commit, verification time, and residual adoption gap. Commit and push the evidence-only update.

## Plan Audit

- The plan targets the approved public monorepo and never edits the two private sources.
- Each code task begins with a failing test and includes a real CLI acceptance test.
- Release checks cover content, provenance, account automation, private paths, packaging, and the remote branch.
- No helper-only signal substitutes for the two generated user-facing outputs or the public GitHub repository.
- Git commits and publication appear only because the user explicitly authorized them.
- No placeholders, unresolved file ownership, or implicit production-data writes remain.
