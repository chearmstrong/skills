---
name: architecture-compliance-check
description: Verify architecture and implementation follow documented best practices, project patterns, and user rules. Check against project documentation, ensure no assumptions are made, and verify implementation matches documented patterns. Use when reviewing code, implementing features, making architectural decisions, or before committing changes.
---

# Architecture Compliance Check

## Overview

Code must match documented architecture, follow established patterns, and never make assumptions without verification.

**Core principle:** Verify against documentation, not assumptions. If it's not documented, document it or ask.

## When to Use

**Mandatory checks:**
- Before committing architectural changes
- When implementing new features
- When reviewing code for merge
- When making design decisions
- When refactoring existing code

**Use especially when:**
- Implementing patterns from documentation
- Working with multi-component systems
- Making assumptions about behaviour
- Code doesn't match existing patterns

## The Verification Process

### Phase 1: Documentation Review

**BEFORE implementing or reviewing:**

1. **Identify Relevant Documentation**
   - Check `docs/` directory for architecture guides (if exists)
   - Review `.github/copilot-instructions.md` for project patterns (if exists)
   - Check component-specific README files
   - Review user rules (DynamoDB, Python/FastAPI, CDK/IaC)
   - **Use the best available external documentation source:**
     - Context7 MCP for library/framework documentation if available
     - AWS documentation or AWS API MCP tools if available
     - Otherwise use official documentation, stable web sources, and project lock files

2. **Read Documentation Completely**
   - Don't skim - read every relevant section
   - Understand the full pattern, not just snippets
   - Note all requirements and constraints
   - Identify dependencies and assumptions
   - **For external libraries/frameworks:** Use Context7 if available; otherwise use official documentation and versioned project files
   - **For AWS services:** Use AWS documentation tooling if available; otherwise use official AWS documentation

3. **Verify Documentation Exists**
   - If pattern isn't documented → document it first
   - If unclear → ask for clarification
   - Don't assume undocumented patterns
   - **For external tools:** Always check official documentation before assuming behaviour

### Phase 2: Pattern Verification

**Check implementation matches documented patterns:**

1. **Architectural Patterns**
   - Does it follow documented architecture?
   - Are design patterns used correctly?
   - Does it match existing implementations?

2. **Project-Specific Patterns**
   - File organisation matches project structure?
   - Naming conventions followed?
   - Integration points correct?

3. **Component Integration**
   - Follows documented integration patterns?
   - Uses correct APIs/interfaces?
   - Respects component boundaries?

### Phase 3: Assumption Verification

**Eliminate all assumptions:**

1. **Verify, Don't Assume**
   - Don't assume behaviour - check code/docs
   - Don't assume requirements - read them
   - Don't assume patterns - verify them

2. **Check Against Reality**
   - Read actual implementation code
   - Check actual configuration
   - Verify actual behaviour

3. **Question Unclear Areas**
   - If unclear → ask, don't guess
   - If undocumented → document or ask
   - If inconsistent → flag it

### Phase 4: Best Practices Check

**Verify against established standards:**

1. **User Rules Compliance**
   - DynamoDB guardrails followed?
   - Python/FastAPI standards met?
   - CDK/IaC best practices applied?

2. **External Library/Framework Best Practices**
   - Use Context7 MCP to verify library/framework patterns if available
   - Otherwise check official documentation and versioned project files
   - Check FastAPI, boto3, AWS CDK, TypeScript, and pytest patterns against the relevant version
   - Don't assume - always check official documentation

3. **AWS Service Best Practices**
   - Use AWS Documentation MCP to verify AWS service patterns if available
   - Otherwise use official AWS documentation and API references
   - Check AWS service-specific best practices
   - Verify API usage patterns
   - Confirm configuration best practices

4. **Code Quality**
   - Error handling comprehensive?
   - Tests adequate?
   - Observability included?

5. **Security & Performance**
   - Security best practices followed?
   - Performance considerations addressed?
   - Resource usage appropriate?

## Common Documentation Sources

**Project Documentation (check if exists):**
- `docs/` - Architecture, deployment, configuration guides
- `.github/copilot-instructions.md` - Project patterns and workflows
- Component README files - Component-specific patterns
- Architecture diagrams - Visual architecture references

**User Rules (in system):**
- DynamoDB guardrails - Pagination, GSI usage, cost patterns
- Python/FastAPI standards - Async patterns, error handling, testing
- CDK/IaC best practices - Stack organisation, security, testing

**External Documentation:**
- **MCP tools, if available** - Context7 for library/framework documentation; AWS documentation/API tools for AWS service patterns
- **Official documentation fallback** - Project documentation sites, AWS documentation, API references, release notes, and versioned lock files

**Code References:**
- Existing implementations - Working examples in codebase
- Test files - Expected behaviour and patterns
- Configuration files - Actual configuration patterns

## Verification Checklist

**Before claiming compliance, verify:**

- [ ] Relevant documentation read completely
- [ ] **External libraries/frameworks verified via available documentation tools or official sources**
- [ ] **AWS services verified via available documentation tools or official AWS documentation**
- [ ] Implementation matches documented patterns
- [ ] No assumptions made without verification
- [ ] User rules followed (DynamoDB, Python/FastAPI, CDK)
- [ ] Existing patterns referenced and followed
- [ ] Integration points verified
- [ ] Error handling comprehensive
- [ ] Tests cover implementation
- [ ] Observability included (if applicable)
- [ ] Security considerations addressed

## Red Flags - STOP and Verify

**If you catch yourself:**
- Assuming behaviour without checking code
- Skipping documentation review
- Implementing without reading full pattern
- Guessing at requirements
- Using patterns without understanding them
- Making architectural decisions without documentation
- Ignoring user rules
- Proceeding with unclear requirements

**STOP. Return to Phase 1 and verify.**

## Examples

**Good - Verified Against Documentation:**
```
[Implementing feature]

1. Checked docs/ directory for architecture guides
2. Found pattern: [specific pattern from documentation]
3. Verified existing implementations follow this pattern
4. Checked user rules for [relevant standards]
5. Used available documentation tools or official sources to verify [library] patterns
6. Implementation matches documented pattern exactly
```

**Bad - Assumed Pattern:**
```
[Implementing workflow node]

1. Saw similar code, assumed pattern
2. Implemented without reading documentation
3. Used pattern incorrectly
4. Doesn't match documented architecture
```

**Good - No Assumptions:**
```
[Using DynamoDB query]

1. Read DynamoDB guardrails user rule
2. Used available documentation tools or official AWS documentation to verify DynamoDB Query API patterns
3. Verified pagination preserves LastEvaluatedKey exactly
4. Checked existing queries follow pattern
5. Ensured PK/SK projected for mutations
6. Added test for multi-page traversal
```

**Bad - Made Assumptions:**
```
[Using DynamOBD query]

1. Assumed pagination works like other databases
2. Simplified LastEvaluatedKey (dropped attributes)
3. Didn't check guardrails
4. Broke pagination silently
```

## Documentation Gaps

**If documentation is missing or unclear:**

1. **Document it first** - Add to appropriate docs file
2. **Or ask for clarification** - Don't proceed with assumptions
3. **Flag the gap** - Note what's missing in review

**Never:**
- Proceed with undocumented assumptions
- Create new patterns without documenting
- Ignore documentation gaps

## Integration with Other Skills

**Works with:**
- `systematic-debugging` - Verify root cause before fixing
- `verification-before-completion` - Verify compliance before claiming done
- `receiving-code-review` - Verify feedback against documentation
- `requesting-code-review` - Include compliance check in review

## The Bottom Line

**Documentation is the source of truth.**

Verify against it. Never assume. Always check.

If it's not documented, document it or ask.
