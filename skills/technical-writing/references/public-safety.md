# Public-Safety Review

Use this reference for blogs, public docs, customer-facing posts, conference material, examples, or any writing likely to leave the organisation.

## Default Position

Share learning, architecture patterns, tradeoffs, and operational lessons without exposing internal implementation detail. Prefer generic examples unless a detail is already public and relevant.

## Blockers

Flag content that includes or implies:

- Internal project, customer, tenant, repository, ticket, incident, or system names that are not already public. These create search handles that can connect public writing to private systems.
- Commercial terms, pricing, contracts, roadmap commitments, sales strategy, or customer-specific outcomes. These can leak negotiation context or imply commitments.
- Secrets, tokens, account IDs, private URLs, hostnames, bucket names, internal Slack/Jira/GitHub links, or access patterns. These can become direct attack or reconnaissance material.
- Security controls, bypasses, detection gaps, exploit paths, or operational weaknesses beyond what is intentionally public. These can turn a learning post into attacker guidance.
- Proprietary algorithms, prompts, evaluation datasets, business rules, private benchmarks, or vendor-specific commercial findings. These can expose competitive or contractual information.
- Claims about performance, savings, reliability, or quality without caveats and source context. These can become misleading marketing claims when stripped of conditions.
- Future-looking statements that sound committed rather than exploratory. These can be read as roadmap promises.

## Safer Substitutions

- Replace named internal systems with role-based labels such as "the workflow service" or "the search API".
- Replace customer details with neutral scenarios.
- Replace exact numbers with ranges or qualitative statements unless the number is approved for publication.
- Replace private architecture diagrams with simplified public patterns.
- Replace internal incident detail with the general lesson and the guardrail that followed.

## Required Checks

Before treating external writing as ready:

1. Confirm every concrete claim is sourced from public material, supplied approved notes, or repo facts that are safe to disclose.
2. Keep caveats next to benchmarks and measured results.
3. Avoid implying the organisation has solved a broad industry problem if the evidence is narrower.
4. Remove internal names from examples, commands, screenshots, code snippets, and links.
5. State residual approval needs if legal, security, product, or communications review might be required.
