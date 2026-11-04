---
name: simplify-explanation
description: Use when the user asks to simplify an explanation, explain something in plain English, or says an answer is confusing, too technical, or has lost them. Applies to explanations rather than requests to simplify code, architecture, or processes.
metadata:
  author: "chearmstrong"
  canonical-source: "https://github.com/chearmstrong/skills"
---

# Simplify Explanation

Rebuild the explanation around what the reader needs to understand. Optimise for understanding; a shorter answer alone may leave the same gaps.

- Use the explanation or passage identified by the user; otherwise use the last relevant answer. Infer their knowledge from the conversation. Ask only if the intended subject is unclear.
- Start with the main point and enough context to show what problem it addresses and why it matters.
- Explain one idea at a time in everyday language. Define necessary technical terms when first used, retaining exact identifiers and established project terms where precision matters.
- Use one concrete example when it makes an abstract relationship easier to follow. Label illustrative details so they cannot be mistaken for verified behaviour.
- Preserve conditions, uncertainty, important trade-offs and the distinction between a proposal and an agreed decision. If the original explanation is wrong, correct it explicitly.
- Match the reader's level and requested language. Keep a natural, respectful tone without assuming that confusion means inexperience.

Return the explanation directly, with only the detail needed to make it understandable. Check that it answers the original question and preserves every condition that could change the reader's decision or action. Keep file edits and implementation changes outside this skill unless separately requested.
