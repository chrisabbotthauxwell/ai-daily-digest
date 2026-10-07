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

## Open questions for the owner

1. **Region:** assumed `uksouth`. Confirm, or pick another (check Cosmos free tier and Container Apps availability).
2. **Subscription:** is it pay-as-you-go with no existing free-tier Cosmos DB account?
3. **Log Analytics 5 GB/month:** unconfirmed on the official pricing page and possibly per billing account. Verify in the portal.
4. **Container Apps Jobs and the free grant:** unconfirmed whether job compute counts against it (assumed yes).
5. **SWA deploy token:** the one stored secret (plan 06). Acceptable?
6. **`sources.yaml` delivery:** baked into the ingest image (default) or fetched from GitHub at runtime (faster source changes, no redeploy, but an extra runtime dependency)?
7. **Reddit and GitHub trending:** both are fragile (API terms, no official trending API). Keep in v1 or defer?
8. **Previews:** share the production API (default) or accept no previews that need a backend?
9. **Tooling defaults assumed:** uv and ruff (Python), pnpm (web).
