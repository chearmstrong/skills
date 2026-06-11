# AWS Documentation Map

Use official AWS documentation for DynamoDB-specific claims when current docs are available. Prefer these pages before relying on memory.

## Pagination

- Query pagination: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Query.Pagination.html
- Query API reference: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_Query.html
- Scan API reference: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_Scan.html

Use for:

- `LastEvaluatedKey`
- `ExclusiveStartKey`
- 1 MB page boundaries
- `Limit`
- Query and Scan result pagination

## Query, Scan, And Access Patterns

- Best practices for querying and scanning: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-query-scan.html
- Querying tables: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Query.html
- Scanning tables: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Scan.html
- Filter expressions: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Query.FilterExpression.html

Use for:

- `Query` versus `Scan`
- Scan cost and throughput impact
- Filter expressions being applied after reads
- Parallel scan cautions

## Keys And Indexes

- Core components: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.CoreComponents.html
- Secondary indexes: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/SecondaryIndexes.html
- Global secondary indexes: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GSI.html
- Index projections: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GSI.Projections.html

Use for:

- Primary key behaviour
- GSI and LSI key schema
- Projection choices
- Base-table attributes available from index reads

## Writes And Conditions

- Condition expressions: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.ConditionExpressions.html
- Update expressions: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.UpdateExpressions.html
- Optimistic locking with version numbers: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBMapper.OptimisticLocking.html
- Transactions: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/transactions.html

Use for:

- Create-without-overwrite semantics
- Conditional updates and deletes
- State transitions
- Optimistic locking
- Multi-item write consistency

## Errors And Retries

- Error handling with DynamoDB: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Programming.Errors.html
- AWS SDK retry behaviour should be checked in the SDK-specific documentation for the project language and version.

Use for:

- Retryable errors
- Throttling behaviour
- Conditional check failures
- AWS request IDs and diagnostics

## Capacity, Hot Partitions, And Cost

- Read and write capacity mode: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadWriteCapacityMode.html
- Partition key design: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-partition-key-design.html
- Throttling diagnosis: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/throttling-diagnosing-workflow.html
- CloudWatch metrics: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/metrics-dimensions.html

Use for:

- Hot partitions
- Capacity mode assumptions
- Throttling and latency findings
- Metrics and alarms

## Documentation Discipline

- Cite the AWS page used when reporting a DynamoDB behavioural finding.
- If docs are inaccessible, state the unchecked assumption and keep the recommendation conservative.
- Prefer SDK-specific docs for language-specific paginator, marshalling, retry, and exception behaviour.
