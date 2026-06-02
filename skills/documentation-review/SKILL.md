---
name: documentation-review
description: Review documentation to ensure it matches implementation, is correct and up-to-date, clear and concise, uses British English, and has no duplication or redundancy. Works with or without MCP; prefers Context7 / AWS docs MCP when enabled, otherwise web search and official docs. Use when reviewing documentation files, code comments, docstrings, or when documentation may be outdated. Applies to markdown files, README files, code comments, and docstrings.
---

# Documentation Review

## Overview

Documentation must match implementation, be accurate, current, and follow quality standards.

**Core principle:** Documentation is code. It must be correct, clear, and maintainable.

**Sharing this skill:** Colleagues do not need any MCP servers installed. The process below is the same either way: verify against the codebase first, then verify external claims using the best tools available in the environment. When MCP tools are present, use them for speed and accuracy; when they are not, use the listed fallbacks so outcomes stay equivalent.

## When to Use

**Mandatory reviews:**

- When code changes affect documented behaviour
- Before merging documentation updates
- When reviewing pull requests with documentation
- When documentation seems outdated or unclear
- When adding new documentation

**Use especially when:**

- Implementation changed but docs weren't updated
- Documentation is verbose or unclear
- Duplicate information exists
- Code comments/docstrings need review

## External verification: MCP-first, same results without MCP

Use this order so reviewers with only built-in tools still reach the same bar.

| Goal | If MCP is available | If MCP is not available |
| --- | --- | --- |
| Library / framework API and patterns | **Context7** (`resolve-library-id`, `get-library-docs`) for official-style snippets and APIs | **Web search** for the library name + topic; open **official docs** (project site or Read the Docs); use **web fetch** on stable doc URLs; cross-check **`pyproject.toml` / `package.json` / lock files** for pinned versions |
| AWS services, CDK, boto3 patterns | **AWS-related MCP** (e.g. CDK search / CloudFormation docs tools in your workspace) | **AWS Documentation** via web search or direct fetch of `docs.aws.amazon.com` pages; **service FAQs and API reference** for the service named in the doc |
| Link and version sanity | As above, plus MCP may surface current pages quickly | Manually open links from the doc; fix 404s; compare prose to **lock files** and **CHANGELOGs** in the repo |
| “Is this pattern still recommended?” | Context7 / AWS MCP focused queries | Official migration guides, deprecations pages, and framework release notes via search or fetch |

**Rules:**

1. **Never skip external verification** just because MCP is off—use fallbacks.
2. **Prefer primary sources:** vendor docs, official API reference, and the repo’s own dependency pins over random blogs.
3. **State uncertainty** when offline or sources conflict; suggest verifying against a specific doc URL or version.

### How to tell what you have

- If your environment lists MCP servers or tools (e.g. Context7, AWS IaC / knowledge), treat the “If MCP is available” column as in scope.
- If not, proceed with repository reads, git history, web search, and fetches only.

## The Review Process

### Phase 1: Accuracy Verification

**Verify documentation matches implementation:**

1. **Check Against Code**
   - Read actual implementation code
   - Verify documented behaviour matches code
   - Check examples work with current code
   - Verify API signatures match

2. **Check Against External Sources**
   - Verify external references are correct and version-appropriate
   - Check compatibility with dependencies as pinned in the project
   - Use the **External verification** table above: MCP if present; otherwise web search, official docs, and fetches

3. **Verify Examples**
   - Test code examples actually work (or reason through execution paths if running code is not possible)
   - Ensure examples use current APIs
   - Check examples match documented patterns
   - Verify no deprecated patterns

4. **Check Configuration**
   - Verify config examples are current
   - Check environment variables match code
   - Verify default values are correct
   - Check file paths and locations

### Phase 2: Currency Check

**Ensure documentation is up-to-date:**

1. **Check Recent Changes**
   - Review git history for related changes
   - Check if implementation changed
   - Verify breaking changes documented
   - Check migration guides are current

2. **Version Compatibility**
   - Verify version numbers are current
   - Check dependency versions match lock files or manifests
   - Verify API versions are correct
   - Check for deprecated features

3. **External References**
   - Re-verify library and cloud docs using the **External verification** table
   - Verify external links work (and replace brittle links if needed)
   - Check for newer documentation or deprecation notices

### Phase 3: Quality Standards

**Ensure documentation meets quality standards:**

1. **Clarity and Conciseness**
   - Prefer simplicity over complexity
   - Remove unnecessary words
   - Use clear, direct language
   - Avoid jargon unless necessary

2. **British English**
   - Use British spelling (colour, organise, centre)
   - Use British grammar conventions
   - Maintain consistency throughout
   - Check existing docs for style

3. **No Duplication**
   - Remove repeated information
   - Reference instead of duplicating
   - Consolidate similar sections
   - Use links to avoid repetition

4. **No Redundancy**
   - Remove low-value content
   - Eliminate obvious statements
   - Cut filler words and phrases
   - Remove outdated information

5. **Structure and Organisation**
   - Logical flow and organisation
   - Clear headings and sections
   - Appropriate detail level
   - Easy to navigate

### Phase 4: Code Documentation Review

**Review code comments and docstrings:**

1. **Docstrings**
   - Match function/class behaviour
   - Use current parameter names
   - Document all parameters
   - Include return types and exceptions
   - Use British English

2. **Code Comments**
   - Explain why, not what
   - Remove obvious comments
   - Update when code changes
   - Use clear, concise language

3. **Inline Documentation**
   - No redundant comments
   - Comments add value
   - Match implementation
   - Use British English

## Quality Checklist

**Before approving documentation:**

- [ ] Matches actual implementation
- [ ] Examples work with current code
- [ ] External references verified (MCP **or** web search / official docs / lock files, as available)
- [ ] No outdated information
- [ ] Clear and concise (prefers simplicity)
- [ ] British English throughout
- [ ] No duplication
- [ ] No redundant or low-value content
- [ ] Code comments/docstrings reviewed
- [ ] Structure is logical and navigable

## Red Flags - Fix These

**Accuracy Issues:**

- Documentation describes old behaviour
- Examples don't work
- API signatures don't match
- Configuration examples are wrong
- External references are outdated

**Quality Issues:**

- Verbose or unclear language
- American English spelling
- Duplicate information
- Redundant statements
- Obvious or low-value content
- Code comments explain what, not why
- Outdated docstrings

**Structure Issues:**

- Poor organisation
- Unclear headings
- Too much detail in wrong places
- Hard to navigate

## Examples

**Good - Accurate and Clear:**

````markdown
# User Authentication

Authenticates users using JWT tokens. Tokens expire after 24 hours.

## Usage

```python
from api.auth import authenticate_user

token = authenticate_user(username, password)
```

## Configuration

Set `JWT_SECRET_KEY` in environment variables.
````

**Bad - Outdated and Verbose:**

````markdown
# User Authentication System

This system provides authentication functionality for users. It uses JWT tokens
which are JSON Web Tokens that provide a way to securely transmit information
between parties. The tokens expire after a period of time, specifically 24 hours
from when they are created. This is a security feature.

## How to Use It

You can use this by importing the function and calling it with username and password:

```python
from api.auth import authenticate_user  # This is the function you need

token = authenticate_user(username, password)  # Call it like this
```

## Configuration Settings

You need to configure the JWT_SECRET_KEY environment variable. This is required.
````

**Good - Docstring:**

```python
def authenticate_user(username: str, password: str) -> str:
    """Authenticate user and return JWT token.

    Args:
        username: User's username
        password: User's password

    Returns:
        JWT token string

    Raises:
        AuthenticationError: If credentials are invalid
    """
```

**Bad - Docstring:**

```python
def authenticate_user(username: str, password: str) -> str:
    """This function authenticates a user.

    It takes a username and password and returns a token.
    The username is the user's username.
    The password is the user's password.
    It returns a JWT token.
    """
```

## MCP tools (optional enhancement)

When MCP is enabled, use it to shorten the feedback loop; it does **not** change the definition of “done.”

1. **Context7** — Library/framework usage (e.g. FastAPI, boto3, CDK), API patterns, version-specific notes.
2. **AWS documentation / CDK MCP** (if configured) — Service behaviour, configuration, CloudFormation/CDK references.

**Example workflow (MCP available):**

1. Read implementation code.
2. Use AWS docs MCP to sanity-check DynamoDB (or other service) patterns.
3. Use Context7 for client library patterns (e.g. boto3).
4. Align documentation with verified patterns; run or trace examples against the repo.

**Same workflow without MCP:**

1. Read implementation code.
2. Fetch or search official AWS documentation for the same patterns.
3. Use official Python/TypeScript docs and the repo’s dependency versions for client usage.
4. Align documentation; run or trace examples against the repo.

## Documentation Types

**Markdown Files:**

- Architecture documentation
- API documentation
- Configuration guides
- README files
- Deployment guides

**Code Documentation:**

- Module docstrings
- Function/class docstrings
- Inline comments
- Type hints and annotations

**All must:**

- Match implementation
- Be accurate and current
- Be clear and concise
- Use British English
- Avoid duplication
- Remove redundancy

## Integration with Other Skills

**Works with:**

- `architecture-compliance-check` - Verify docs match architecture
- `verification-before-completion` - Verify docs before claiming done
- `systematic-debugging` - Document fixes accurately

## The Bottom Line

**Documentation must be:**

- Accurate (matches implementation)
- Current (up-to-date)
- Clear (simple and concise)
- Consistent (British English)
- Non-redundant (no duplication or filler)

**Verify against code. Check external sources (MCP if you have it, otherwise official docs and search). Remove redundancy. Use British English.**
