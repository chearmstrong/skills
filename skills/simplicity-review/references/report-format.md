# Consolidated Report Format

Use plain language and the user's or repository's language conventions. Keep empty findings sections as a short `None` so the absence of findings is explicit.

Scale detail to the change. For a small review, coverage may be one short paragraph or compact table with source identifiers grouped together. Keep detail that affects confidence: reviewed revisions/snapshots, check outcomes, fallbacks, missing evidence and disagreements. Do not repeat the same provenance under every finding.

## Scope and readiness verdict

Summarise what the change does and the cumulative scope reviewed. State base/head commits, stack contributions and included working-tree snapshot identifiers. Identify the agreed baseline, expected load and material assumptions.

**Readiness:** ready on reviewed evidence, required fixes remain, or insufficient evidence. Name blocking finding IDs or missing evidence. Passing tests alone do not establish readiness, and an incomplete reviewer run cannot receive an unqualified ready verdict.

## Required fixes

Number findings in priority order. For each, include:

- **Title, priority and category.**
- **Location:** exact path and line(s), tied to the reviewed revision. Use clickable file or diff links where supported.
- **Evidence and consequence:** requirement/source and concrete failure scenario or cost.
- **Smallest fix and trade-off:** preserve required behaviour and guarantees; name affected decisions or documentation.
- **Verification:** focused evidence needed to establish the fix.

## Optional improvements

Continue the same numbering and finding fields. Explain why each simplification is worth doing and why it is optional.

## Simplicity verdict

Choose **appropriately simple**, **justified complexity**, **unnecessarily complex** or **insufficient evidence**. Explain the judgement with concrete examples, including why necessary complexity should remain. Refer to numbered simplifications where applicable. Keep this verdict separate from readiness: simple code can still be incorrect.

## Coverage and limitations

- State whether both fresh reviewers completed independently and reviewed the same scope.
- Summarise inspected evidence and checks, distinguishing existing results from checks run for this review. Include relevant commands, revisions, outcomes and limits.
- Record guidance sources: local path plus digest, or remote repository/path/commit; identify fallbacks and missing references.
- State missing checks, assumptions, unsupported external claims and changes to sources during the review. Include the working-tree drift-check result and distinguish the reviewed snapshot from any later live content.
- Preserve material reviewer disagreements and explain how they were resolved or what evidence is still needed. Unconfirmed concerns stay here rather than becoming findings.

Report in chat unless the user requests a saved report. No implementation changes, automatic fix rounds or candidate-selection questions follow this report.
