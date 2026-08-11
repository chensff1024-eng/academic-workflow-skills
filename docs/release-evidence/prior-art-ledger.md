# Prior-art and rights disposition ledger

Checked: 2026-08-11

This ledger records design inputs. It does not claim that linked projects or
services endorse this repository.

| Source | Disposition | What informed this repository | What is excluded |
| --- | --- | --- | --- |
| [OpenAI Codex use cases](https://developers.openai.com/codex/use-cases) | Adopt | Reusable workflows may be saved as focused Skills; deterministic helpers make repeated work inspectable. | No claim of OpenAI affiliation, certification, or program eligibility. |
| [cookjohn/cnki-skills](https://github.com/cookjohn/cnki-skills) | Adapt concept only | Separating search planning, result handling, paper details, journal discovery, and export clarified useful workflow stages. | No source code, Skill text, agents, browser control, CAPTCHA handling, document downloads, or third-party tree is copied or bundled. |
| [CNKI membership agreement](https://wap.oversea.cnki.net/cn/member/agreement.html) | Respect as a hard boundary | The public workflow requires user-led authorized access and local processing of permitted metadata. | No robot, spider, crawler, session extraction, automated article download, or redistribution of downloaded articles. |
| Private prototype workflows | Rewrite from requirements | Evidence levels, explicit downgrade states, manuscript profiling, and topic-fit reasoning were retained as abstract requirements. | No private run, screenshot, document, signed locator, account data, private manuscript, mirrored Skill, or private implementation is included. |
| Official journal and host-institution pages | Adapt into dated heuristics | Broad editorial scope and journal-form distinctions seed the local discovery matrix. | No stale operational details are presented as current; author instructions, indexing, fees, cycle, contacts, and AI policy remain unresolved until rechecked. |

## License decision

All repository-owned code, tests, documentation, synthetic examples, and Skill
contracts are released under Apache-2.0. External pages are referenced by link
and short paraphrase only. They are not redistributed under this license.

## Maintenance decision

The release verifier rejects common private artifacts, downloaded-document
formats, browser-session/download automation anchors, secret-like assignments,
and developer-machine paths. This is a bounded safeguard, not a substitute for
human review of every release.
