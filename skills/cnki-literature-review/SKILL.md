---
name: cnki-literature-review
description: Plan a CNKI literature search and turn user-supplied bibliographic JSON or CSV into a ranked evidence ledger and evidence-bounded literature-review packet. Use for Chinese literature discovery, screening, synthesis, and review writing when the user will perform authorized searches and exports manually. Do not use for login, CAPTCHA, cookie access, automated downloads, or redistribution of source documents.
---

# CNKI Literature Review

Build a literature-review packet from bibliographic records the user is
authorized to access and export. This Skill is unofficial and unaffiliated with
CNKI.

## Required boundaries

- Ask the user to perform searches and exports through an account and interface
  they are authorized to use.
- Accept bibliographic metadata, abstracts, and user-written notes only.
- Never request credentials, session information, signed links, screenshots,
  downloaded documents, or paywalled full text.
- Never automate login, CAPTCHA, browser state, or downloads.
- Treat records without abstracts or notes as metadata-only. Do not infer their
  arguments, evidence, methods, or conclusions.
- Preserve disagreements and uncertainty. Bibliographic frequency is not proof
  of a historical claim.

## Workflow

1. Read `references/search-playbook.md` and turn the topic into concepts,
   synonyms, exclusions, date range, and screening criteria.
2. Give the user a transparent search worksheet. The user runs it manually and
   exports permitted metadata as described in `references/input-contract.md`.
3. Run the local pipeline:

   ```text
   python -B scripts/literature_pipeline.py --input records.json --topic "研究主题" --terms "关键词一,关键词二" --output review-packet.md
   ```

4. Inspect record-level warnings. Do not silently repair missing titles or turn
   missing abstracts into claims.
5. Use the generated evidence ledger to group scholarship by question,
   chronology, method, archive, or disagreement.
6. Draft only within `references/output-contract.md`. Attach every substantive
   synthesis to abstract-backed evidence or explicit user notes.

## Output

Return:

- search strategy and inclusion criteria;
- ranked evidence ledger with a visible evidence level;
- thematic synthesis and disagreement map;
- gaps and next-search queries;
- a literature-review outline or bounded draft;
- limitations and items requiring source inspection.

The deterministic helper is local-only and uses the Python standard library.
