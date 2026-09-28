# Identity Contract Review

## Establish The Review Target

Classify the target as a reusable template/library, a configured consumer, or a deployed service. A template defines extension points and defaults; a consumer chooses its policy; deployment evidence establishes which configuration runs. Do not infer either of the latter from template code alone.

Trace the route's actual dependency chain, including overrides, middleware and downstream checks. A helper's name or presence does not prove that a route calls it or that its checks execute.

## Record The Contract By Route And Caller

For each materially different route/caller pair, record required context, source, enforcing code, and evidence or unknowns for these layers:

| Layer | Question to answer |
| --- | --- |
| Bearer-token validation | Which signature, issuer, audience, expiry and token-type checks actually run? |
| Operation permission | Which scopes or permissions does this route require, and where is the comparison executed? A disabled check is not enforcement. |
| Authenticated actor | Does the subject represent a person or a service/client? Preserve the authenticated actor separately from any effective user. |
| Tenant selection | Is the requested tenant selected from a header, claim, resource or server-side mapping? What precedence and missing/conflicting-value rules apply? |
| Tenant access | What authoritative policy proves that this actor may perform this operation on the selected tenant/resource? Identify the enforcement point. |
| Delegated user | Can the actor request an effective user? What permission and actor–user–tenant binding authorises it, and which identities are audited? |

For example, a metadata route may require only a valid bearer token, while an object-write route needs operation permission and authorised tenant context. Record their contracts separately; do not impose the write route's identity requirements on metadata.

Distinguish standard token claims from optional application claims. Verify the issuer's token contract for the relevant grant and audience; an M2M token may identify a client without supplying a tenant or end user. Token validity does not establish every application's identity requirements.

## Select The Smallest Correction

| Evidence | Review conclusion |
| --- | --- |
| Valid token rejected for missing context the route does not use | Review the dependency boundary; retain token validation and the route's required permissions. |
| Header or claim supplies a tenant but access is unproven | Trace all policy/resource checks before reporting a bypass. A signed value proves provenance, not automatically tenant entitlement. |
| Template has no application grant source | Specify the consumer-supplied selection and access contract; do not invent a membership store or assume issuer claims. |
| User header follows a required token subject | Check whether the branch is reachable before describing it as working M2M identity or impersonation. |
| Documentation and reachable behaviour disagree | Report the precise mismatch and migration impact, separately from any unproven deployment exposure. |

Keep independently established scope defects separate from tenant/delegation design. Restoring a permission comparison requires the route's intended permission contract, not a blanket scope applied to every route.

## Verify The Boundary

Choose relevant positive and negative checks from the matrix:

- Missing/invalid token versus valid token without optional application claims.
- Required permission present versus absent; authenticated metadata versus tenant-scoped operations.
- Authorised versus unauthorised tenant, conflicting selection sources, and missing required tenant context.
- Actor acting for itself versus permitted and denied delegation; verify both actor and effective-user audit identity.
- Configured consumer policy versus template defaults; check every supported auth entry path affected by a shared change.

Use issuer documentation or a sanitised token shape to establish claim expectations. Local fixtures prove handling of that shape; they do not prove the live issuer emits it. Report unavailable policy, issuer or deployment evidence explicitly.

Never treat a header as authority because it has a familiar name, a signed tenant claim as sufficient entitlement without its policy contract, or a service subject as an end user without evidence. These shortcuts hide distinct trust decisions behind identity extraction.
