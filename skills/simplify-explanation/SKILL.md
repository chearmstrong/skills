---
name: simplify-explanation
description: Use when the user asks to simplify an explanation, explain something in plain English, or says an answer is confusing, too technical, or has lost them. Applies to explanations rather than requests to simplify code, architecture, or processes.
metadata:
  author: "chearmstrong"
  canonical-source: "https://github.com/chearmstrong/skills"
---

# Simplify Explanation

Repair what prevents understanding; shortening alone may leave the same gap.

- Use the explanation or passage identified by the user; otherwise use the last relevant answer. Infer their knowledge from the conversation. Ask only if the intended subject is unclear.
- Identify the missing link before rewriting: context (what problem this addresses), vocabulary (what a term means), or causality (how one thing leads to another). Repair that gap first; defining familiar terms will not explain a missing causal link.
- Lead with the main point. Add the missing context, define unfamiliar terms, or walk through the cause and effect as needed. Retain exact identifiers and established project terms where precision matters.
- Use one concrete example when it makes an abstract relationship easier to follow. Label illustrative details so they cannot be mistaken for verified behaviour.
- Preserve conditions, uncertainty, important trade-offs and the distinction between a proposal and an agreed decision. If the original explanation is wrong, correct it explicitly.
- Match the reader's demonstrated knowledge and requested language.

Return the explanation directly. Check that it answers the original question and retains conditions that could change the reader's decision or action. File edits and implementation changes require a separate request.
