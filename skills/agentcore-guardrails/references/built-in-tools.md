# Browser And Code Interpreter Guardrails

Use this reference for AgentCore Browser, browser profiles, web automation,
Live View, session recording, Code Interpreter, generated code, files,
terminal commands, execution roles, or sandbox networking.

## Contents

- [Choose The Tool Boundary](#choose-the-tool-boundary)
- [Browser](#browser)
- [Browser Profiles And Authentication](#browser-profiles-and-authentication)
- [Live View And Session Recording](#live-view-and-session-recording)
- [Code Interpreter](#code-interpreter)
- [Files, Network, And Execution Roles](#files-network-and-execution-roles)
- [Shared Failure Patterns](#shared-failure-patterns)
- [Verification](#verification)

## Choose The Tool Boundary

| Need | Capability | Boundary to preserve |
| --- | --- | --- |
| Navigate or operate a web application | Browser | Website content and UI state remain untrusted; authorise consequential actions outside the model |
| Reuse authenticated website state | Browser profile | Cookies and local storage are credentials and tenant-bound state, not a convenience cache |
| Let a user observe or take over a browser | Live View | Viewing or intervention does not itself approve the agent's next action |
| Execute calculations or transform supplied data | Code Interpreter | Generated code and files remain untrusted inside an isolated execution boundary |
| Reach S3, internal services, or the internet from code | Code Interpreter with network or execution-role access | The reachable data and side effects define the real blast radius, not the sandbox label |

## Browser

- Treat page text, DOM attributes, downloads, pop-ups, redirects, screenshots,
  and accessibility content as untrusted input that can contain prompt
  injection.
- Constrain destinations, redirects, protocols, downloads, uploads, clipboard,
  and file access to what the task requires.
- Resolve actor, tenant, destination, and business authority outside
  model-selected browser inputs.
- Require a bound approval before purchase, submission, deletion, publication,
  permission change, message send, or another irreversible web action.
- Verify the committed server response or resulting application state; a
  rendered success message is not authoritative evidence.
- Define timeout, cancellation, takeover, retry, and partial-form behaviour so
  reconnects do not repeat an action.

## Browser Profiles And Authentication

- Treat saved cookies and local storage as credentials subject to least
  privilege, tenant isolation, rotation, revocation, and deletion.
- Bind each profile to the authenticated actor, tenant, environment, and
  permitted destinations through trusted configuration.
- Do not let the model select an arbitrary profile identifier or save one
  actor's state into another actor's profile.
- Assume saved authentication can expire, be revoked, or outlive the business
  permission that originally created it.
- Prevent concurrent profile save or load operations from silently overwriting
  newer authentication or application state.
- Re-authorise the requested website action even when loading a profile
  successfully restores a logged-in session.

## Live View And Session Recording

- Treat Live View URLs and streams as sensitive session access, not ordinary
  observability links.
- Authenticate and authorise viewers, limit URL lifetime, and prevent
  cross-tenant session selection.
- Record operator takeover, return of control, and the exact action state at
  the hand-off boundary.
- Treat recordings as sensitive datasets: they can contain DOM content, typed
  values, console output, network events, personal data, and secrets.
- Define S3 ownership, encryption, access, retention, deletion, audit, and
  incident handling before enabling recording.
- Do not claim an action was human-approved merely because a person could
  watch the session.

## Code Interpreter

- Treat generated code, commands, package names, paths, URLs, and outputs as
  untrusted.
- Use the least-capable runtime, libraries, duration, storage, CPU, memory, and
  concurrency that satisfy the task.
- Keep policy decisions, credentials, approval commitments, and authoritative
  state outside generated code and session files.
- Validate outputs before using them as commands, queries, configuration,
  executable files, policy inputs, or irreversible-action parameters.
- Pin or constrain dynamically installed dependencies and treat package
  installation as a supply-chain and egress decision.
- Prevent generated code from using resource exhaustion, fork or process
  spawning, archive expansion, or oversized output to bypass task limits.

## Files, Network, And Execution Roles

- Treat uploaded files, archives, spreadsheets, notebooks, and retrieved S3
  objects as untrusted content.
- Constrain file type, size, count, path, archive expansion, retention, and
  output destination.
- Prevent path traversal, symlink escape, executable upload, decompression
  bombs, formula injection, and unsafe output reuse where applicable.
- Select network mode and egress destinations from trusted configuration, not
  model arguments.
- Treat terminal-command or execution-role access as ambient authority
  available to generated code; scope the role to the exact buckets, prefixes,
  APIs, and actions required.
- Keep tenant data separated across sessions and verify current persistence,
  cleanup, and retention semantics against AWS documentation.

## Shared Failure Patterns

- **NEVER equate isolation with authorisation.** A perfectly isolated browser
  or sandbox can still perform an unauthorised action using valid credentials.
- **NEVER reuse a browser profile across actors or tenants.** Persisted cookies
  can silently transfer another user's authenticated authority.
- **NEVER expose Live View, recording, file, or session identifiers without
  resource-level checks.** Guessable or substituted identifiers can cross the
  session boundary.
- **NEVER pass secrets through model-generated code or browser fields when a
  trusted credential boundary can inject them.** Prompts, files, console
  output, recordings, and traces can retain the value.
- **NEVER trust a browser-rendered message or code-generated result as proof of
  commitment.** Verify the authoritative downstream state.

## Verification

- Test prompt injection, redirect and destination escape, profile
  substitution, expired authentication, operator takeover, approval replay,
  duplicate submission, and recording access.
- Test malicious files, archive expansion, path traversal, package
  substitution, egress denial, execution-role denial, resource exhaustion,
  timeout, cleanup, and unsafe output reuse.
- Test the deployed session, profile, Live View, recording, file, network, and
  execution-role contracts rather than relying only on mocked tool calls.
