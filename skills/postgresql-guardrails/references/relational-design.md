# Relational Design

## From Business Facts To Tables

Before writing DDL, describe what one record represents, its identity, who owns
it, permitted changes, relationships and required history. Walk through a real
create/update/delete workflow and the queries it must support. Resolve missing
business rules before choosing a physical design; label reversible assumptions.

| Decision | Guardrail |
| --- | --- |
| Entity or attribute? | Give independently identified facts their own representation when their lifecycle or relationships require it. Do not make every noun, class or API response into a table. |
| Relationship multiplicity? | Establish whether each side allows zero, one or many related records, and whether this changes over time. A foreign key alone does not enforce one-to-one; uniqueness may also be required. |
| Many-to-many relationship? | Use a linking table when both sides can have several related records. Put attributes of the relationship, such as membership role and dates, on that relationship. |
| Identity and uniqueness? | Separate stable row identity from business uniqueness. A generated primary key does not prevent duplicate business facts. Scope external identifiers to their actual source/tenant when needed. |
| Required or optional? | Define what absence means and enforce required references. Nullable foreign keys can bypass reference checks; do not use null, empty text and sentinel IDs interchangeably. |

## Authority, History And Tenant Ownership

- Normalise around the facts: keep a current fact in one authoritative place
  where practical, avoiding updates that must synchronise several copies.
  Explain the update anomaly being prevented rather than prescribing a normal
  form mechanically. Do not add speculative entities or generic attribute tables.
- Distinguish duplicated current data from independent historical facts. An
  order's agreed price can remain fixed when a product's current price changes.
  Do not remove deliberate snapshots merely to avoid repeated values.
- Application objects and read models can combine several tables. Choose their
  shape for callers without forcing that shape onto stored facts. Denormalised
  copies require an explicit source, update/rebuild owner and consistency need.
- Tenant-scoped IDs and filters alone do not ensure relationships stay within
  one tenant. Where required, reference tenant-qualified unique keys using
  composite foreign keys, with required tenant/reference columns non-null.
  Separate foreign keys proving a user and team exist do not prove a shared tenant.
- Choose delete behaviour from ownership and retention requirements. Cascade
  only when deleting dependent data is intended; do not cascade away retained
  business history or apply soft deletion universally. Check uniqueness and
  references against any agreed soft-deletion lifecycle.

## Example: Membership Is A Relationship With A Lifecycle

A small model has users, teams and memberships. A membership relates one user
to one team and carries role, join time and optional leave time. Keep the
current team name on the team; copy it only if a historical name is required.

If leaving and rejoining must preserve history, one row can represent each
membership period. Uniqueness on user/team across all periods would forbid
rejoining. An appropriate partial unique index on tenant/user/team for rows
with no leave time can prevent duplicate current memberships while retaining
past periods. Define separately whether historical periods may overlap.

Use tenant-qualified references to both user and team if cross-tenant membership
is forbidden. Check required fields and date ordering. Verify orphan references,
cross-tenant links, concurrent duplicate-current inserts, leave/rejoin, deletion
and retained snapshots according to the actual requirements.

Explain the chosen model as business facts, relationships, enforceable rules
and representative reads/writes. An entity diagram can help when relationships
are hard to follow; it is not a substitute for lifecycle and integrity rules.

Official sources: constraints, schemas and indexes in the
[documentation map](documentation-map.md). Use the concurrency reference when
validity depends on competing writes, and query/view design for derived reads.
