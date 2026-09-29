# Local development

Use this for a short feedback loop before changing cloud resources. Commands
below are adaptable examples; they have not been run against a live gateway.
Use repository recipes when available. Official basis: [configuration](https://docs.litellm.ai/docs/proxy/configs),
[deployment](https://docs.litellm.ai/docs/proxy/deploy), and
[Bedrock adapter](https://docs.litellm.ai/docs/providers/bedrock).

## Prepare a small working configuration

First choose a supported release and approved model/region. Keep the public
alias separate from the provider model identifier. This example uses locally
chosen environment-variable names; they are not required repository fields.

```yaml
model_list:
  - model_name: coding
    litellm_params:
      model: os.environ/LITELLM_PROVIDER_MODEL
      aws_region_name: os.environ/AWS_REGION
general_settings:
  master_key: os.environ/LITELLM_MASTER_KEY
```

Set `LITELLM_PROVIDER_MODEL` to the exact approved LiteLLM Bedrock adapter string,
including its provider prefix and any inference profile. Verify these environment
references resolve in the selected release. Do not add static AWS keys to YAML.
Use non-production AWS credentials locally; an ECS task role supplies credentials
in deployment. Host credentials are not automatically available inside Docker.
Choose an approved local credential mechanism and test it inside the container.

For keys, teams, budgets, or spend persistence, add the selected release's database
configuration and a local PostgreSQL service with a persistent volume. Add Redis
when testing shared limits/router state across replicas. A database-free process
is a limited inference smoke test, not the complete gateway baseline. Reuse an
existing Compose setup or adapt the upstream one; pin its images and wait for
dependency readiness. Do not replace cloud dependencies with local containers.

The persistent local setup is incomplete until the selected release's database
URL configuration and migration command are confirmed, the migration finishes
successfully, and the proxy connects to that database. If the release is not yet
selected, identify those prerequisites rather than inventing a migration command
or claiming persistence is ready.

## Start the same runtime you intend to deploy

With a trusted, untracked local environment file, a prepared `config.yaml`, and
`LITELLM_IMAGE` set to the chosen image reference:

```bash
docker run --rm --entrypoint litellm "$LITELLM_IMAGE" --help
docker run --rm --name litellm-dev \
  -p 127.0.0.1:4000:4000 \
  --env-file .env.litellm \
  -v "$PWD/config.yaml:/app/config.yaml:ro" \
  "$LITELLM_IMAGE" --config /app/config.yaml --port 4000
```

The first command checks CLI flags without starting inference. Confirm the image
entrypoint before using the second command. In Compose, use the dependency's
service name rather than `localhost` for database/Redis endpoints. Bind local
ports to loopback. Do not publish management credentials in terminal output.

## Exercise the real client boundary

Set `LITELLM_BASE_URL` to the trusted local proxy root and `LITELLM_API_KEY` to an
appropriate inference credential. The example alias is `coding` as above:

```bash
curl --fail-with-body --silent --show-error \
  "$LITELLM_BASE_URL/health/readiness"
curl --fail-with-body --silent --show-error \
  -H "Authorization: Bearer $LITELLM_API_KEY" \
  "$LITELLM_BASE_URL/v1/models"
curl --fail-with-body --silent --show-error --max-time 120 \
  -H "Authorization: Bearer $LITELLM_API_KEY" \
  -H 'Content-Type: application/json' \
  --data '{"model":"coding","messages":[{"role":"user","content":"Reply with OK"}],"stream":false}' \
  "$LITELLM_BASE_URL/v1/chat/completions"
curl --fail-with-body --silent --show-error --no-buffer \
  --max-time 120 \
  -H "Authorization: Bearer $LITELLM_API_KEY" \
  -H 'Content-Type: application/json' \
  --data '{"model":"coding","messages":[{"role":"user","content":"Reply with OK"}],"stream":true}' \
  "$LITELLM_BASE_URL/v1/chat/completions"
```

The 120-second bound limits this smoke check; it is not a production timeout
recommendation. Only send synthetic content. Inference consumes provider quota
and may incur cost; run it within the user's authorised test scope. Use a
disposable local admin credential only for initial bootstrap, then a restricted
virtual key for access and budget checks. These direct API requests precede a
real client test; they do not prove the client's API/features work.

Verify non-streaming first, then streaming, then a tool-call round trip through
the chosen client. For Responses API clients, test that surface, continuation,
and tool calls rather than assuming Chat Completions is equivalent. Record the
release, route, alias, provider, elapsed time, and redacted outcome. Preserve a
small synthetic request as a reproducible regression case.
