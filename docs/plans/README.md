# Build plans

Numbered, in rough dependency order. Each has goal, scope, tasks (checkboxes), acceptance criteria and risks. Tick tasks as they land and update status in the root README.

| # | Plan |
|---|---|
| 00 | [Overview & architecture decisions](00-overview-architecture.md) |
| 01 | [Repo & CI skeleton](01-repo-ci-skeleton.md) |
| 02 | [Azure bootstrap](02-azure-bootstrap.md) |
| 03 | [Ingest job](03-ingest-job.md) |
| 04 | [BFF API](04-bff-api.md) |
| 05 | [React front end](05-react-frontend.md) |
| 06 | [Deployment pipeline](06-deployment-pipeline.md) |
| 07 | [Mobile-workflow experiments](07-mobile-workflow-experiments.md) |
| 08 | [Later options](08-later-options.md) |

Phases 03, 04 and 05 can proceed in parallel once 01 is done and the data model in 03 is agreed. 02 is needed before 06.

## Resolved (2026-10-07)

- Region `uksouth`; pay-as-you-go subscription, no existing free-tier Cosmos DB account.
- SWA deploy token stored as a GitHub Actions secret.
- `sources.yaml` baked into the ingest image (revisit later if needed).
- Reddit and GitHub trending deferred to plan 08; X/Twitter rejected (no free tier). v1 adds HF Daily Papers, Bluesky, Lobsters.
- PR previews: SWA built-in; per-PR Container Apps revision is an optional experiment, shared prod API otherwise.

## Open questions for the owner

1. **Log Analytics 5 GB/month:** unconfirmed on the official pricing page and possibly per billing account. Verify in the portal.
2. **Container Apps Jobs and the free grant:** unconfirmed whether job compute counts against it (assumed yes).
3. **Bluesky search:** confirm the unauthenticated endpoint and limits in the official docs before plan 03.
4. **Per-PR API revisions:** verify Container Apps revision labels, limits and billing before committing to the experiment.
5. **Tooling defaults assumed:** uv and ruff (Python), pnpm (web).
