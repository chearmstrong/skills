---
name: review-comments
description: Address PR or code review comments. Use when given review comments to verify before fixing, research best practices with available documentation tools or official sources, and document whether each comment was valid, partially valid, or invalid.
---

# Review Comments

## Overview

Address review comments with rigour — verify before fixing, research where needed, document decisions.

**Core principle:** Verify validity first. Research before implementing. Document every decision.

## Input Format

Use this skill with review comments in the path/line plus quoted-comment format below. Comments can come from `manual-review-comment-export`, from manually copied GitHub review comments, or from GitHub Copilot comments copied out of the GitHub UI.

- path/to/file.py:42-45

"Comment text describing the issue or concern."

- path/to/another/file.ts:100

"Another comment about a different issue."

## Procedure

For each review comment:

1. **Locate the code**: Read the file and identify the specific lines mentioned
2. **Verify the comment**: Check if the concern is valid by:
   - Understanding the current implementation
   - Checking for related code patterns
   - Verifying against project standards and best practices
3. **Research if needed**: If the comment involves external libraries, frameworks, or best practices:
   - Use Context7 MCP tools for library/framework documentation if available
   - Otherwise use official documentation, web search, or stable project references
   - Use web search for general best practices or standards when official sources are insufficient
   - Check project-specific documentation in `docs/` directory
4. **Fix if valid**: If the comment is valid:
   - Implement the fix following best practices
   - Ensure the fix aligns with project standards
   - Add tests if the comment highlights missing test coverage
5. **Document**: If the comment is invalid or already addressed, explain why

## Scope & Performance

- **Focus on the specific lines** mentioned in each comment
- Read **minimal surrounding context** (typically 10–20 lines before/after)
- If a comment requires understanding a larger pattern, expand context as needed
- **Cap lookups**: Limit to 5 additional file reads or searches per comment unless essential

## Output Format

For each comment, provide:

1. **Comment Location**: `path/to/file.py:42-45`
2. **Verification**: Whether the comment is valid, partially valid, or invalid
3. **Analysis**: Brief explanation of why it's valid/invalid
4. **Fix Applied** (if valid): Description of the changes made
5. **Files Changed**: List of files modified

### Example Output

#### Comment 1: `src/tests/ingestion/test_service.py:69`

**Verification:** ✅ Valid

**Analysis:** The `__start_sync` method uses `.get()` to extract `ingestionJobId`, which can return `None`, but there's no test case covering this
scenario.

**Fix Applied:** Added test case verifying `ValueError` is raised when `ingestionJobId` is missing from the response.

**Files Changed:** `src/tests/ingestion/test_service.py`

---

#### Comment 2: `src/api/routers/cache_router.py:45-52`

**Verification:** ⚠️ Partially Valid

**Analysis:** Retry logic already exists via `AsyncHTTPTransport(retries=3)`, but timeout configuration is implicit.

**Fix Applied:** Made timeout explicit: `timeout=httpx.Timeout(connect=2.0, read=5.0, pool=10.0)`.

**Files Changed:** `src/api/routers/cache_router.py`

---

#### Comment 3: `infra/stacks/service-stack.ts:120`

**Verification:** ❌ Invalid

**Analysis:** The IAM policy follows least-privilege; the wildcard in the resource ARN is appropriate for OpenSearch collection resource patterns.

**No changes made.**

## Best Practices

- **Always verify** before fixing — don't assume comments are correct
- **Use Context7 if available** for external library/framework patterns and best practices; otherwise use official documentation and web search
- **Add tests** when comments highlight missing test coverage
- **Follow project standards** — check existing patterns in the codebase
- **Document decisions** — if a comment is invalid, explain why clearly
- **Preserve existing behaviour** — unless the comment explicitly requests a change
- **Check related code** — ensure fixes don't break other parts of the system
