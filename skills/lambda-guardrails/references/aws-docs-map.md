# AWS Documentation Map

Use official AWS documentation for Lambda-specific claims when current docs are available. Prefer these pages before relying on memory.

## Best Practices

- Lambda best practices: https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html
- Lambda quotas: https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html

Use for:

- Idempotent code
- Execution environment reuse
- Function configuration
- Scalability
- Metrics and alarms
- Security best practices
- Service limits and maximum execution duration

## Invocation And Error Handling

- Asynchronous invocation errors and retries: https://docs.aws.amazon.com/lambda/latest/dg/invocation-async-error-handling.html
- Configuring async error handling: https://docs.aws.amazon.com/lambda/latest/dg/invocation-async-configuring.html
- Capturing async invocation records, destinations, and DLQs: https://docs.aws.amazon.com/lambda/latest/dg/invocation-async-retain-records.html
- Lambda invocation modes: https://docs.aws.amazon.com/lambda/latest/dg/lambda-invocation.html

Use for:

- Async retry attempts
- Maximum event age
- On-failure destinations
- Dead-letter queues
- Duplicate events and failed invocation records

## Event Source Mappings

- How Lambda processes stream and queue event sources: https://docs.aws.amazon.com/lambda/latest/dg/invocation-eventsourcemapping.html
- Using Lambda with Amazon SQS: https://docs.aws.amazon.com/lambda/latest/dg/with-sqs.html
- Creating and configuring SQS event source mappings: https://docs.aws.amazon.com/lambda/latest/dg/services-sqs-configure.html
- SQS event source parameters: https://docs.aws.amazon.com/lambda/latest/dg/services-sqs-parameters.html
- SQS error handling and partial batch responses: https://docs.aws.amazon.com/lambda/latest/dg/services-sqs-errorhandling.html
- SQS scaling and maximum concurrency: https://docs.aws.amazon.com/lambda/latest/dg/services-sqs-scaling.html
- Troubleshooting event source mappings: https://docs.aws.amazon.com/lambda/latest/dg/troubleshooting-event-source-mapping.html

Use for:

- Batch size and batching windows
- Partial batch responses
- Visibility timeout guidance
- Scaling behaviour
- Maximum concurrency
- Backpressure, throttling, and poison messages

## Service Integrations And HTTP Triggers

- Lambda invocation methods: https://docs.aws.amazon.com/lambda/latest/dg/lambda-invocation.html
- API Gateway integration: https://docs.aws.amazon.com/lambda/latest/dg/services-apigateway.html
- Function URLs: https://docs.aws.amazon.com/lambda/latest/dg/urls-configuration.html
- EventBridge Scheduler: https://docs.aws.amazon.com/lambda/latest/dg/with-eventbridge-scheduler.html
- Step Functions with Lambda: https://docs.aws.amazon.com/lambda/latest/dg/with-step-functions.html
- Event-driven architecture design: https://docs.aws.amazon.com/lambda/latest/dg/concepts-event-driven-architectures.html
- Lambda application design: https://docs.aws.amazon.com/lambda/latest/dg/concepts-application-design.html

Use for:

- API Gateway event and response format
- Function URL auth, CORS, and throttling
- EventBridge Scheduler retry policy and schedule setup
- EventBridge and async-style event-driven patterns
- Step Functions retry/catch orchestration
- Choosing orchestration versus function chaining

## Configuration, Concurrency, And Performance

- Lambda function configuration: https://docs.aws.amazon.com/lambda/latest/dg/configuration-function-common.html
- Configuring memory: https://docs.aws.amazon.com/lambda/latest/dg/configuration-memory.html
- Configuring ephemeral storage: https://docs.aws.amazon.com/lambda/latest/dg/configuration-ephemeral-storage.html
- Configuring reserved concurrency: https://docs.aws.amazon.com/lambda/latest/dg/configuration-concurrency.html
- Configuring provisioned concurrency: https://docs.aws.amazon.com/lambda/latest/dg/provisioned-concurrency.html
- Lambda execution environment lifecycle: https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtime-environment.html

Use for:

- Timeout and memory settings
- Ephemeral storage
- Reserved and provisioned concurrency
- Cold starts and execution environment reuse
- Runtime initialisation assumptions

## Packaging, Runtime, And Deployment

- Deploying .zip file archives: https://docs.aws.amazon.com/lambda/latest/dg/configuration-function-zip.html
- Creating Lambda container images: https://docs.aws.amazon.com/lambda/latest/dg/images-create.html
- Lambda code signing: https://docs.aws.amazon.com/lambda/latest/dg/governance-code-signing.html
- Creating code signing configurations: https://docs.aws.amazon.com/lambda/latest/dg/configuration-codesigning-create.html
- Python .zip packages and native dependencies: https://docs.aws.amazon.com/lambda/latest/dg/python-package.html
- Python container images: https://docs.aws.amazon.com/lambda/latest/dg/python-image.html
- Node.js container images: https://docs.aws.amazon.com/lambda/latest/dg/nodejs-image.html
- CreateFunction API package options: https://docs.aws.amazon.com/lambda/latest/api/API_CreateFunction.html

Use for:

- .zip versus container image deployment
- Native dependencies and build environment
- Runtime and architecture changes
- ECR permissions
- Runtime interface clients
- Code signing and signed deployment controls
- Package size and dependency layout

## Runtime-Specific Handler Docs

- Node.js handlers: https://docs.aws.amazon.com/lambda/latest/dg/nodejs-handler.html
- Python handlers: https://docs.aws.amazon.com/lambda/latest/dg/python-handler.html
- Java handlers: https://docs.aws.amazon.com/lambda/latest/dg/java-handler.html
- Python runtime guide: https://docs.aws.amazon.com/lambda/latest/dg/lambda-python.html

Use for:

- Handler signatures
- Runtime-specific event and context handling
- Runtime initialisation and global state
- SDK client reuse
- Environment variable access

## IAM, Environment, Secrets, And VPC

- Lambda execution role permissions: https://docs.aws.amazon.com/lambda/latest/dg/lambda-intro-execution-role.html
- Lambda resource-based policies: https://docs.aws.amazon.com/lambda/latest/dg/access-control-resource-based.html
- Lambda environment variables: https://docs.aws.amazon.com/lambda/latest/dg/configuration-envvars.html
- Lambda VPC access: https://docs.aws.amazon.com/lambda/latest/dg/configuration-vpc.html
- Secrets Manager with Lambda: https://docs.aws.amazon.com/secretsmanager/latest/userguide/retrieving-secrets_lambda.html

Use for:

- Least-privilege execution roles
- Invoke permissions and source scoping
- Environment variable limits and encryption
- Secret retrieval patterns
- VPC subnets, security groups, routes, DNS, and service access

## Observability

- Monitoring Lambda functions: https://docs.aws.amazon.com/lambda/latest/dg/monitoring-functions.html
- Lambda CloudWatch metrics: https://docs.aws.amazon.com/lambda/latest/dg/monitoring-metrics.html
- Lambda logging: https://docs.aws.amazon.com/lambda/latest/dg/monitoring-cloudwatchlogs.html
- Lambda tracing with X-Ray: https://docs.aws.amazon.com/lambda/latest/dg/services-xray.html
- Powertools for AWS Lambda: https://docs.aws.amazon.com/powertools/

Use for:

- Logs
- Metrics
- Alarms
- Traces
- Correlation IDs
- Operational diagnostics

## Documentation Discipline

- Cite the AWS page used when reporting a Lambda behavioural finding.
- If docs are inaccessible, state the unchecked assumption and keep the recommendation conservative.
- Prefer runtime-specific and SDK-specific docs for language-specific client reuse, retry, marshalling, packaging, and exception behaviour.
