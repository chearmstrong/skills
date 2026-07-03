# Sub-agent Review Prompts

Use these templates only when `execution=subagent` or `execution=hybrid`.

## Implementation

```text
You are implementing {{task_name}} from {{plan_path}}.
Constraints:
- Worktree: {{repo_path}}
- Branch: {{branch}}
- Files you own: {{owned_files}}
- Do not edit: {{out_of_scope_files}}
- Follow TDD where practical.
- Use British English in documentation and comments.
- Do not commit unless explicitly told.
- Report status as DONE, DONE_WITH_CONCERNS, NEEDS_CONTEXT, or BLOCKED.
Task:
{{task_details}}
Acceptance criteria:
{{acceptance_criteria}}
Verification:
{{verification_commands}}
```

## Spec Compliance Review

```text
Review only the current changes for {{task_name}}.
Do not edit files. Report APPROVED or CHANGES_REQUESTED.
Verify against:
{{acceptance_criteria}}
Scope:
{{owned_files}}
Known out-of-scope:
{{out_of_scope_files}}
```

## Code-quality Review

```text
Review only the current changes for {{task_name}}.
Do not edit files. Report APPROVED or CHANGES_REQUESTED.
Focus on:
- correctness
- maintainability
- type safety
- test quality
- unnecessary scope expansion
- consistency with existing project patterns
Scope:
{{owned_files}}
```

## Narrow Fix And Re-review

```text
{{review_type}} review requested a narrow fix for {{task_name}}.
Keep changes scoped to:
{{owned_files}}
Do not edit:
{{out_of_scope_files}}
Requested fixes:
{{review_findings}}
Verification:
{{verification_commands}}
Report DONE, DONE_WITH_CONCERNS, NEEDS_CONTEXT, or BLOCKED with files changed and commands run.
```

After a narrow fix, re-review only the changed task scope and the prior findings. Do not restart broad review unless the fix materially changed the design or touched new areas.
