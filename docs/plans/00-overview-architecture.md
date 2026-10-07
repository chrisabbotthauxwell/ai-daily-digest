# 00 Overview & architecture decisions

## Goal
Define what we are building, the Azure free-tier mapping, and the guardrails that keep it at $0.

## Scope
Architecture, decisions, cost guardrails. No code.

## Architecture
- **Ingest** (Python, Container Apps Job, cron): reads `sources.yaml`, fetches, normalises, dedups, ranks, upserts into Cosmos DB.
- **API / BFF** (Python, FastAPI, Container Apps): `GET /days`, `GET /days/{date}`, filters `?tag=` and `?source=`, `GET /health` (returns git SHA).
- **Web** (React + Vite + TS + MUI, Static Web Apps Free): responsive SPA, drawer on mobile, day picker.
- **Data**: Cosmos DB (NoSQL API), one shared-throughput database, container partitioned by `/day` (`YYYY-MM-DD`).
- **Images**: GHCR. **CI/CD**: GitHub Actions + OIDC.

### Data model (draft, finalised in plan 03)
Item: `id` (hash of canonical URL), `day`, `source_id`, `title`, `url`, `published_at`, `score` (source-native), `rank`, `tags[]`, `fetched_at`.

## Free-tier mapping

Last verified: 2026-10-07 against Microsoft Learn / pricing pages. Re-verify before relying on numbers.

| Need | Service | Free allowance | Confidence |
|---|---|---|---|
| API | Container Apps consumption | 180,000 vCPU-s, 360,000 GiB-s, 2M requests / subscription / month | Verified (pricing page) |
| Ingest | Container Apps Jobs | No request charge; compute presumably counts against the same grants | **Uncertain**: page doesn't say explicitly |
| Database | Cosmos DB free tier | 1000 RU/s + 25 GB for the life of the account; one free account per subscription; opt-in at creation; provisioned/autoscale only (not serverless) | Verified (Learn) |
| Front end | Static Web Apps Free | 100 GB bandwidth/month (no overage on Free), 10 apps, 3 preview envs, 250 MB/env, 500 MB total, 2 custom domains, no SLA | Verified (Learn) |
| Images | GHCR | Free for public packages | Verified by GitHub docs knowledge; confirm at setup |
| Logs | Log Analytics | 5 GB/month ingestion, 31 days retention | **Uncertain**: seen only in Microsoft Q&A and third-party sources, and possibly per billing account rather than per workspace |
| CI | GitHub Actions | Free for public repos | Verify current terms |

**Not used** (not permanently free): Azure Container Registry, Azure Storage, Postgres Flexible Server, SWA Standard, App Insights beyond allowance, Key Vault (not needed; OIDC means no secrets).

### Design consequences
- API scales to zero, so the first request after idle has a cold start of a few seconds. The SPA shows a loading state and retries once.
- Everything lives in one Cosmos database with shared throughput at most 1000 RU/s. Any extra throughput-bearing database or container is billed.
- No SWA managed Functions; SWA serves static assets only. The SPA calls the API directly (CORS locked to the SWA origin).
- 100 GB SWA bandwidth is a hard cap, and the site stops serving if it is exceeded. Fine for a demo; note it.

## Cost guardrails
- [ ] Budget alert (e.g. $1 and $5) on the subscription before any other resource.
- [ ] Log Analytics daily cap set (about 0.1 GB/day to stay inside 5 GB/month).
- [ ] API `minReplicas: 0`, `maxReplicas: 2`, 0.25 vCPU / 0.5 GiB.
- [ ] Ingest job: timeout set, at most 4 runs/day, `replicaTimeout` ~10 min, no retries beyond 1.
- [ ] Cosmos: create with `enableFreeTier: true`, shared database at 1000 RU/s max (or lower), TTL on items (e.g. 90 days) to bound storage.
- [ ] Bicep what-if reviewed for every infra PR; reviewer checks no new billable resource types.
- [ ] Monthly check of Cost Management and Container Apps usage vs. grants (calendar reminder).
- [ ] LLM calls (phase 08) are off by default with a hard monthly cap.

## Decision log
| Decision | Rationale |
|---|---|
| Monorepo | One PR can touch config, API and UI; simple for mobile |
| FastAPI | Auto OpenAPI contract, reusable by Flutter later |
| Cosmos free tier over alternatives | Only always-free managed DB on Azure that fits |
| GHCR | ACR isn't free; public repo, so public packages need no pull secret |
| Bicep | Native, no state file to host |
| OIDC | No long-lived secrets |
| `sources.yaml` baked into the ingest image | Simple; a merge triggers redeploy. Alternative (fetch from GitHub raw at runtime) is in open questions |

## Acceptance criteria
- Free-tier table reviewed and uncertain items resolved or accepted by the owner.
- Guardrail checklist copied into plan 02 tasks.

## Risks
- Free allowances change; mitigated by the verify date and monthly check.
- Cosmos free tier opt-in can't be added later; a mistake means recreating the account.
- Bluesky search endpoint/limits are unconfirmed against official docs (check before plan 03). X/Twitter was rejected: no free API tier for reads/search as of 2026 (third-party sources; verify in the X console).
- Subscription-wide grants are shared with anything else running in the subscription.

## Decisions confirmed by the owner (2026-10-07)
- Region `uksouth`; pay-as-you-go subscription with no existing free-tier Cosmos DB account.
- `sources.yaml` baked into the ingest image (revisit if it becomes a problem).
- SWA deploy token stored as a GitHub Actions repo secret (`AZURE_STATIC_WEB_APPS_API_TOKEN`); the only stored secret.
- Reddit and GitHub trending dropped from v1 (moved to plan 08); X/Twitter rejected on cost.
- PR previews: SWA built-in previews; an ephemeral Container Apps revision per PR is an optional experiment (plan 06), with the shared production API as fallback.
