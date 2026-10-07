# 02 Azure bootstrap

## Goal
Reproducible, free-tier-only Azure infrastructure defined in Bicep, with GitHub able to deploy via OIDC and no stored secrets.

## Scope
`infra/` Bicep, OIDC federation, budget alert. Region default: `uksouth` (open question).

## Resources
Resource group; Log Analytics workspace (daily cap); Container Apps environment (consumption only, no workload profiles); Container App for the API (placeholder image, min 0); Container Apps Job for ingest (cron, placeholder image); Cosmos DB account (`enableFreeTier: true`, provisioned throughput) with one shared-throughput database and container partitioned by `/day`, TTL enabled; Static Web App (Free); user-assigned managed identity for the apps (Cosmos data-plane RBAC, no keys); budget with alerts.

## Manual vs automated

| Step | Who |
|---|---|
| Confirm subscription is eligible and has no existing free-tier Cosmos account | **You** |
| `az login`, create the resource group, create the Entra app registration and federated credentials (subjects: `repo:chrisabbotthauxwell/ai-daily-digest:ref:refs/heads/main`, `:pull_request`, and an `environment:` subject if used) | **You** (one-off script in `infra/bootstrap.sh`, reviewed first) |
| Grant the app `Contributor` scoped to the resource group (plus `User Access Administrator` or a narrower role only if Bicep assigns RBAC) | **You** |
| Add repo variables `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID` (not secrets) | **You** |
| Create budget and alert emails | Bicep, with the email address supplied by **you** |
| All other resources, what-if on PRs, deploy on merge | Automation |
| Make the GHCR packages public after first push | **You** |

## Tasks
- [ ] Write `infra/bootstrap.sh` (idempotent, prints what it will do, requires confirmation)
- [ ] `infra/main.bicep` plus modules: `monitoring`, `cosmos`, `containerapps`, `swa`, `budget`
- [ ] Parameters file for `prod`; no secrets in params
- [ ] Cosmos data-plane role assignment for the managed identity
- [ ] `az deployment group what-if` workflow on PRs touching `infra/`
- [ ] Deploy workflow (manual `workflow_dispatch` first, then on merge)
- [ ] Record outputs (API URL, SWA name) in docs
- [ ] Verify in the portal: Cosmos shows "Free tier applied", Log Analytics cap set, no unexpected resources
- [ ] Teardown doc: how to delete the resource group

## Acceptance criteria
- `az deployment group create` from a clean group builds everything, and re-running is a no-op.
- Cosmos free tier applied; Cost Management shows $0 after 24-48h.
- A workflow authenticates to Azure with OIDC and no secrets.
- Budget alert emails confirmed received (test with a low threshold).

## Risks
- Cosmos free tier is opt-in only at creation; if it fails because one exists, stop and ask.
- Container Apps environment may default to a workload-profiles type, so make sure it is consumption-only.
- Placeholder images and a public GHCR pull must work before the first real image exists. Use Microsoft's hello-world image initially.
- Over-broad RBAC on the OIDC app; scope to the resource group.
- Federated-credential subjects are exact-match; typos give confusing failures.
- Cosmos does not allow RU/s reductions below a floor per container, so check minimums when sizing.
