---
name: world-history-submission-strategy
description: Analyze a Chinese-language history manuscript and produce a dated journal-fit shortlist, verification checklist, submission sequence, and pre-submission revision priorities. Use for world history, global history, regional history, cross-border history, and adjacent Chinese-history venues. This Skill gives strategy only and must never log in, upload, email, pay, or submit a manuscript.
---

# World History Submission Strategy

Produce evidence-separated journal strategy for a manuscript, abstract, outline,
or detailed brief. This Skill does not submit papers.

## Required boundaries

- Never request journal credentials or operate a submission account.
- Never upload a manuscript, send an email, pay a fee, accept terms, or click a
  final-submission control.
- Do not promise acceptance, review speed, indexing status, or editorial
  interest.
- Treat the bundled matrix as a dated discovery aid. Verify all changing facts
  on the journal's official site at the time of use.
- Keep the manuscript and reviewer correspondence local unless the user
  explicitly authorizes a separate permitted service.

## Workflow

1. Profile the manuscript: question, object, place, period, source base, method,
   central claim, scholarly conversation, and likely readership.
2. Read `references/evidence-policy.md` and
   `references/journal-matrix.json`.
3. Query the local matrix:

   ```text
   python -B scripts/query_matrix.py --terms "世界史,港口,运输" --output strategy.json
   ```

4. Read recent tables of contents and official author instructions for the top
   candidates. Do not infer current requirements from an old or third-party
   page.
5. Separate the final advice into:
   - official-source facts checked now;
   - editorial-fit inference based on topic and recent contents;
   - unresolved dynamic facts;
   - three manuscript revisions that most improve fit.
6. Give a sequential shortlist: first submission, one or two backups, and any
   conditional stretch candidate. Explain opportunity cost and reformatting
   burden.

## Output

Follow `references/output-contract.md`. Include a visible timestamp, source
links, confidence limits, and the explicit statement that no submission action
was performed.
