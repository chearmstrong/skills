---
name: postgresql-guardrails
description: Use when designing, building, changing, debugging, or reviewing PostgreSQL relational models, entities, relationships, schemas, SQL, joins, views, materialised views, migrations, transactions, concurrent workers, connections, security, or query performance. Guides implementation and review with brief explanations. Covers local PostgreSQL and loads AWS RDS guidance when relevant.
metadata:
  author: "chearmstrong"
  canonical-source: "https://github.com/chearmstrong/skills"
---

# PostgreSQL Guardrails

Protect correctness and operational safety while helping the user learn through
the work. Prefer the smallest change that meets the actual access patterns and
correctness requirements.

## Establish Context

- Inspect repository contracts, migrations, SQL, driver and connection handling.
  Establish the target PostgreSQL major version, hosting, application roles,
  workload and whether the data is disposable or must be retained.
- Distinguish source configuration from verified database settings. Use existing
  evidence or authorised read-only inspection; ask only when missing information
  materially changes the decision. Do not print credentials or sensitive rows.
- Reviews and diagnosis remain read-only unless changes are also authorised.
  Make authorised local changes and run proportionate checks. Obtain explicit
  approval for external writes, destructive actions or a material scope increase;
  existing approval covers actions within its stated bounds.

## Load Relevant Guidance

Read the relevant references before making decisions in these areas:

| Task | Reference |
| --- | --- |
| Entities, relationships, normalisation, ownership, history or mapping application models to storage | [Relational design](references/relational-design.md) |
| Result-row meaning, joins, aggregation, views or derived read models | [Query and view design](references/query-and-view-design.md) |
| Transactions, competing writes, retries, job claims or delivery | [Correctness and concurrency](references/correctness-and-concurrency.md) |
| Tables, constraints, types, SQL, indexes or query performance | [Schema and queries](references/schema-and-queries.md) |
| Connections, timeouts, migrations, security or recovery | [Connections and operations](references/connections-and-operations.md) |
| RDS PostgreSQL, RDS Proxy, AWS authentication, networking or deployment | [AWS RDS](references/aws-rds.md), plus relevant general guidance |
| Behavioural claims or version-dependent choices | [Documentation map](references/documentation-map.md) |

For a broad implementation review, read correctness/concurrency, schema/queries
and connections/operations; include the design references when modelling or
query/view design is in scope. For narrow work, read only applicable sections.
Do not load AWS guidance for local-only work unless assessing RDS compatibility.

## Apply And Verify

1. Identify the required behaviour and main risk before changing the design.
   Prioritise correctness, security and recoverability before performance.
   For a new model, establish business facts and relationships before tables,
   then walk through representative writes and queries before tuning.
2. Verify consequential PostgreSQL, driver and provider behaviour using the
   documentation map. If sources or runtime access are unavailable, state
   assumptions and limit claims; do not invent observations.
3. Preserve project tooling and patterns. Do not introduce JSONB, enums,
   extensions, partitioning, a pooler or stronger isolation merely because they
   are available. Match the mechanism to a demonstrated requirement.
4. Verify changed behaviour through real PostgreSQL when semantics matter.
   Select relevant cases: constraint rejection, rollback after partial failure,
   competing connections, replay, migration compatibility or bounded queries.
   Mocks and SQLite alone do not prove PostgreSQL locking or isolation behaviour.
5. Report findings with severity, file/line, concrete failure, evidence and the
   smallest remedy. For implementation, report the change, relevant checks and
   remaining limits. Separate local evidence from RDS and production evidence.

## Explain Through The Work

For consequential decisions, briefly connect the choice to its failure mode
and verification. Explain a new term in plain English on first use. For example:

> **Decision:** Commit the user change and delivery job together.
> **Why:** A failure between separate commits could leave a changed user with
> no job to deliver it.
> **Verification:** Force the job insert to fail and confirm neither write persists.

Keep explanations next to the relevant decision or finding. Say whether a
check was run or is proposed. Expand when asked; avoid repeating concepts the
user already understands or adding lessons to trivial edits. Honour requests
for terse output or deeper teaching.

## Supporting Skills

Supabase's optional
[`supabase-postgres-best-practices`](https://github.com/supabase/agent-skills/tree/main/skills/supabase-postgres-best-practices)
can supplement a specific topic when installed. Apply the same source and
workload checks to its recommendations; this skill works independently of it.
