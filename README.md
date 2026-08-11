# Academic Workflow Skills

[![CI](https://github.com/chensff1024-eng/academic-workflow-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/chensff1024-eng/academic-workflow-skills/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

Two local-first Codex Skills for a research workflow that moves from literature
discovery to journal strategy without automating restricted accounts or final
submission actions.

This project is unofficial and unaffiliated with CNKI, journal publishers,
universities, OpenAI, or submission-platform operators.

## Skills

### `cnki-literature-review`

Plans a manual CNKI search, normalizes user-supplied JSON or CSV bibliographic
metadata, ranks records transparently, and builds an evidence ledger for
literature-review writing.

It does not automate CNKI login, CAPTCHA, browser sessions, article downloads,
or redistribution. A user's own CNKI account establishes only the access rights
granted by that account and the applicable terms; it does not expand this
Skill's automation boundary.

[Read the Skill](skills/cnki-literature-review/SKILL.md)

### `world-history-submission-strategy`

Profiles a history manuscript and returns a dated journal-fit shortlist,
official-source verification checklist, submission sequence, and three
pre-submission revision priorities.

It does not automate journal login, upload, email, payment, or final
submission. The bundled journal matrix contains discovery heuristics, not an
acceptance forecast or a live statement of submission requirements.

[Read the Skill](skills/world-history-submission-strategy/SKILL.md)

## Workflow

1. Define a research question and manual database search plan.
2. Export permitted bibliographic metadata and process it locally.
3. Build an evidence-bounded literature review and identify source gaps.
4. Profile the resulting manuscript.
5. Generate a preliminary journal-fit shortlist.
6. Verify current author instructions on official sites before any human-led
   submission decision.

## Install

Copy either directory under `skills/` into your Codex Skills directory. For
example, on Windows:

```powershell
Copy-Item -Recurse skills\cnki-literature-review $env:USERPROFILE\.codex\skills\
Copy-Item -Recurse skills\world-history-submission-strategy $env:USERPROFILE\.codex\skills\
```

Restart Codex after installation. Each `SKILL.md` contains its trigger and
safety contract.

## Local command examples

```text
python -B skills/cnki-literature-review/scripts/literature_pipeline.py \
  --input skills/cnki-literature-review/examples/sample-records.json \
  --topic "港口与腹地关系" --terms "港口,运输,腹地" \
  --output .tmp/review-packet.md

python -B skills/world-history-submission-strategy/scripts/query_matrix.py \
  --terms "世界史,英国史,港口,运输" \
  --output .tmp/submission-strategy.json
```

The examples are synthetic. Generated outputs stay under `.tmp/`.

## Verify and package

```text
python -B -m unittest discover -s tests -t . -p "test_*.py" -v
python -B scripts/verify_release.py --root .
python -B scripts/package_skills.py --output-dir .tmp/dist
```

The packager runs the release verifier first and creates deterministic archives
with SHA-256 hashes.

## Series context

These two Skills are the first public components extracted from a broader
private, local-first academic workflow maintained by the same author. The local
system connects provenance-aware knowledge ingestion, evidence-bounded writing,
role-isolated review and finalization, human release decisions, document audit,
and journal strategy.

The private implementations and research data are not included here. Their
existence is supporting evidence of the series direction, not a claim of public
adoption or completed end-to-end acceptance. See the
[series roadmap](docs/series-roadmap.md) for the verified local scope, current
limits, and release gates for future components.

## Rights and privacy

- Process only material you are authorized to use.
- Do not commit private manuscripts, restricted full text, downloaded files,
  screenshots, credentials, session data, or signed links.
- Records without abstracts or user notes remain metadata-only and cannot
  support claims about a paper's argument or findings.
- Verify current submission instructions, fees, indexing, review cycles,
  contacts, and AI policies on official journal pages.

See [SECURITY.md](SECURITY.md), [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md),
and [CONTRIBUTING.md](CONTRIBUTING.md).

## Project status

Initial public release. The repository provides tested workflow primitives and
synthetic examples; it does not yet claim broad adoption, download volume, or
community maintenance history.

For the verified program boundary, evidence checklist, and truthful draft
answers, see the
[Codex for Open Source application guide](docs/codex-for-open-source-application.md).
