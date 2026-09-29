# ECS and CDK patterns

Use the project's existing constructs and ownership model. These are adaptable
integration patterns, not a ready-to-deploy CDK application. Consult the
[official deployment guide](https://docs.litellm.ai/docs/proxy/deploy) and
[AWS CDK sample](https://github.com/aws-samples/sample-claude-code-with-litellm-and-bedrock).
The sample explicitly needs production hardening; neither its defaults nor the
official Terraform module supersede the project's design.

## Map the runtime into existing resources

| Concern | CDK integration pattern | Evidence to collect |
| --- | --- | --- |
| Runtime | ECS task definition and container using a pinned image/digest | Manifest architecture, entrypoint, flags, writable paths, startup logs |
| Config | Existing config pipeline renders/packages or securely fetches a LiteLLM config artefact | Proven source ownership, deterministic output, file exists before startup |
| Secrets | ECS container secret references or an explicitly chosen runtime lookup | Access role, encryption permissions, restart/rotation behaviour |
| Inference | Task role grants approved Bedrock operations/resources | Actual adapter API, model/profile and regional permissions |
| Traffic | ALB target group for LiteLLM, explicit client paths | Path preservation, listener priority, health checks, management isolation |
| Persistence | Reachable PostgreSQL and Redis where required | TLS, security groups, credentials, connection capacity and outage tests |
| Telemetry | Gateway exporter to the existing collector/export path | Export protocol, resource identity, content exclusion, correlation |

The task role belongs to application calls such as Bedrock or runtime secret
retrieval. The execution role supports the ECS agent's image pull, log delivery,
and startup secret injection. Grant permissions to the role that performs the
operation; do not put Bedrock invocation on the execution role. See AWS
[task roles](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-iam-roles.html)
and [execution roles](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_execution_IAM_role.html).

For a monolithic deployment, one LiteLLM ECS service can run multiple tasks.
For a split deployment, map gateway, backend and UI to the documented runtime
units. Choose service boundaries and client routes from the deployment design;
use sidecars for task-local helpers such as configuration delivery or telemetry.

## Deliver configuration deliberately

Choose a pattern consistent with the repo: bake non-secret generated config into
the image, download it during controlled startup, or use an existing sidecar/file
delivery mechanism. An ECS environment map does not create `/app/config.yaml`.
For sidecar delivery, define the shared volume, output path, readiness dependency,
failure handling, and reload/restart behaviour. Confirm LiteLLM can consume the
actual file format; do not assume it speaks the configuration service's protocol.

Environment-owned and instance-owned resources must follow local instructions.
Database/Redis reuse, isolation, naming, config selectors, and deployment commands
are project decisions. Do not introduce a new override layer or configuration
source merely because an upstream example uses one.

## Gate database changes and rollouts

Separate schema migration from scaled serving tasks when adopting that production
pattern. Use the selected release's migration command, package and image; inspect
them rather than assuming an arbitrary Prisma command can find the schema.
An ECS one-off task is an adaptable equivalent of a migration job: reuse network
and secret access, wait for task completion, inspect container exit codes, and
only proceed when successful. Current deployment docs set
`DISABLE_SCHEMA_UPDATE=true` on serving tasks; verify it in the chosen release
and prove startup leaves migrations to the job. Serialise simultaneous deployments.

Check whether old and new tasks can share the upgraded schema. Rehearse restore
and rollback; returning to an old image does not reverse database migrations.
Store and preserve `LITELLM_SALT_KEY` with database backups: changing or losing it
after provider credentials are stored makes those credentials unreadable.
Virtual keys are hashed; this warning concerns encrypted provider credentials.
Before any key change, identify the encryption key actually in use. Without a
salt key, the master key can also be the encryption key. Follow the selected
release's [key-rotation procedure](https://docs.litellm.ai/docs/proxy/master_key_rotations);
do not substitute ordinary secret rotation for a credential migration.

Budget database connections at maximum task count, including rolling-deployment
overlap: tasks × workers × pool limit, plus migration/admin headroom. Measure
concurrent streams, memory and provider throttling before choosing sizing or an
autoscaling signal. Avoid copying Kubernetes worker or memory prescriptions into
Fargate without workload evidence. See [production guidance](https://docs.litellm.ai/docs/proxy/prod).

For multiple tasks, verify that budget/limit enforcement uses shared state rather
than per-process counters. Current [budget guidance](https://docs.litellm.ai/docs/proxy/users)
describes Redis counters and database reconciliation; confirm the selected
release's dependency and failure contract. Test concurrent requests across tasks,
stale/missing state, and the chosen reject-or-continue policy. Do not infer a hard
spend ceiling from healthy stores or accounting records.

## Preserve long responses

Use `/health/readiness` for LiteLLM traffic admission and `/health/liveliness`
for process health, after confirming the selected release's probe contract.
Inspect readiness dependency state; a database-free ready process is insufficient
when persistence is required. Probe the LiteLLM target itself and account for
startup grace and dependency failure. Check the full streaming path:

- Client/gateway request timeouts, ALB idle timeout and edge buffering.
- Target deregistration delay and ECS shutdown time.
- Gaps between chunks, cancellation, scale-in and a rolling deployment.

Use AWS [ALB attributes](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/edit-load-balancer-attributes.html)
and [ECS draining](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/load-balancer-connection-draining.html).

Before deployment, run the repository's config validation, TypeScript checks,
CDK assertions/synth and diff where available. Review IAM, routes, resource
replacement and secret exposure. A passing synth is not a live startup or
inference test. Obtain the required authority for deployment separately.
