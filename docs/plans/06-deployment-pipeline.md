# 06 Deployment pipeline

## Goal
Merging to `main` builds, publishes and deploys everything automatically and safely; PRs get preview front ends.

## Scope
GitHub Actions workflows, GHCR publishing, Container Apps and Job rollout, SWA deploy and previews.

## Design
- **Images:** `ghcr.io/chrisabbotthauxwell/ai-daily-digest-api` and `-ingest`, tagged with the commit SHA (and `latest` for convenience; deploys always use the SHA). Built with Buildx and GHA cache; `GIT_SHA` build arg. Packages are public, so Azure pulls without a secret.
- **API deploy:** `az containerapp update --image ...:<sha>` using OIDC login; new revision with single-revision mode; wait for `/health` to return the new SHA, otherwise fail and leave the previous revision active.
- **Ingest deploy:** `az containerapp job update --image ...:<sha>`. `sources.yaml` is baked into the image, so a sources-only PR rebuilds ingest only.
- **Web deploy:** build with `VITE_API_BASE_URL`, deploy with the SWA deploy action (deployment token held as a repo secret, since SWA tokens aren't OIDC-based; confirm current options). PRs get an auto preview environment (limit of 3 concurrent on Free) and the URL is commented on the PR; preview is closed when the PR closes.
- **API for previews:** previews share the production API (read-only), so CORS must allow `*.azurestaticapps.net` for this app; no per-PR backend.
- **Concurrency:** one deploy at a time per environment; cancel superseded PR runs.
- **Rollback:** re-run the deploy workflow with an earlier SHA (`workflow_dispatch` input), or activate the previous revision.
- **Path filtering:** only rebuild what changed.
- **Security:** least-privilege `permissions:`, OIDC only, no deploy from forks, `pull_request_target` avoided.

## Tasks
- [ ] `build-images.yml`: build and push api and ingest to GHCR on `main`
- [ ] `deploy-api.yml` with health-SHA gate
- [ ] `deploy-ingest.yml`
- [ ] `deploy-web.yml` plus PR previews and cleanup
- [ ] `workflow_dispatch` rollback input
- [ ] Manual trigger for the ingest job (`az containerapp job start`) workflow
- [ ] Deployment summary in the Actions run (SHA, URLs)
- [ ] Document the SWA token handling and rotation
- [ ] Image size and vulnerability scan step (Trivy, non-blocking at first)
- [ ] Update CLAUDE.md "verify a deploy" steps with real URLs

## Acceptance criteria
- A merged change reaches production with no manual steps, and `/health` shows the new SHA.
- A PR touching `web/` gets a preview URL comment, and the preview is removed on close.
- A failing health gate leaves the old revision serving traffic.
- Rollback to a prior SHA works in under 5 minutes.
- No long-lived Azure credentials stored in GitHub.

## Risks
- SWA deployment token is a stored secret (the one exception to the no-secrets goal); rotate it and keep it repo-scoped.
- Only 3 SWA previews on Free; stale ones must be cleaned up.
- GHCR public package visibility has to be set manually the first time.
- Deploys to a scale-to-zero app need a cold start, so health checks need generous timeouts.
- Image storage in GHCR is free for public packages; confirm current terms.
