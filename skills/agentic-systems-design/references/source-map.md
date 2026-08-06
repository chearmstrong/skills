# Source Map

Use original sources for claims about their products. The links below are also
the evidence base for the cross-provider pattern guidance in this skill.

| Source | Type | Use for | Caveat |
| --- | --- | --- | --- |
| [Google Cloud Well-Architected Framework: AI and ML perspective](https://docs.cloud.google.com/architecture/framework/perspectives/ai-ml) | Official provider framework | Cross-cutting operational, security, reliability, cost, and performance review. | Provider-specific implementation guidance; balance the pillars for the target system. |
| [AWS Prescriptive Guidance: Agentic AI patterns and workflows](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-patterns/introduction.html) | Official provider pattern catalogue | Agent, workflow, state, tool, observability, and control boundaries. | AWS service mappings are illustrative outside AWS. |
| [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) | Engineering article | Workflow-versus-agent distinction and composable pattern selection. | Experience-based guidance, not a governance standard. |
| [Databricks: Agent system design patterns](https://docs.databricks.com/aws/en/agents/agent-system-design-patterns) | Live product documentation | Autonomy continuum and production considerations. | Recheck before platform-specific decisions; some guidance is Databricks or MLflow specific. |
| [Bandara et al.: A Practical Guide for Designing, Developing, and Deploying Production-Grade Agentic AI Workflows](https://arxiv.org/abs/2512.08769) ([PDF](https://arxiv.org/pdf/2512.08769)) | December 2025 arXiv preprint | Hypotheses about focused roles, deterministic operations, prompt management, and deployment. | Unreviewed and case-study-specific; not a universal design rule. |
| [MongoDB: 7 Practical Design Patterns for Agentic Systems](https://www.mongodb.com/resources/basics/artificial-intelligence/agentic-systems) | Vendor engineering article | Accessible taxonomy of controlled flow, routing, evaluation, human review, and multi-agent patterns. | Non-normative and overlaps stronger primary guidance. |
| [Vectorize: Designing Agentic AI Systems, Part 1](https://vectorize.io/blog/designing-agentic-ai-systems-part-1-agent-architectures) | Vendor engineering article | Tool, reasoning, and action-layer vocabulary. | Conceptual reading, not a standard; examples can age. |
