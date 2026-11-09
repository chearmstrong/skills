# Authoring Scenarios

Use isolated temporary inputs and permitted agent tools. Do not exercise a live
repository's write paths. Test outcomes rather than matching report wording.

1. **Standalone installation:** supply only this skill folder, a small design and
   its plan. Other review/delegation skills are absent. Expect exactly two fresh
   Architect/Senior Engineer reviews through native tools and one consolidated report.
2. **Plan misses a guarantee:** design requires an atomic pair of updates; plan
   writes each separately and tests only success. Expect a source-anchored required
   refinement and a failure/rollback verification proposal, without implementing it.
3. **Unapproved recommendation:** design proposes a freshness window; plan silently
   treats it as agreed. Expect an owner decision or correction to approval status,
   rather than invented consent or a claim that baseline tests settle the policy.
4. **Sound small design:** provide a coherent design/plan using existing capabilities
   with appropriate negative tests. Expect no invented findings or forced abstractions.
5. **Unavailable delegation:** the host has no agent tools, or expressly prohibits
   them. Expect an explicit incomplete-independent-coverage result and no dispatch,
   replacement skill dependency or self-review presented as two reviewers.
6. **Drift and conflicting evidence:** change/add a reviewed document after capture;
   include a versioned platform limitation contradicting the plan. Expect findings
   tied to the snapshot, the source conflict explained and later coverage qualified.

Record actual tool calls, outputs and write effects for independent runs. Label
structural validation and coordinator-only walkthroughs separately; neither proves
that two independent reviewers followed the workflow.
