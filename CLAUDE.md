# CLAUDE.md

Guidance for Claude Code working in this repo (desktop or mobile).

## Project

AI Daily Digest: a consolidated daily feed of AI news with links to articles. A scheduled Python ingest job pulls from sources listed in `sources.yaml`, stores items in Cosmos DB (partitioned by day), and a FastAPI BFF serves them to a React SPA. No LLM summaries in v1 (ranking by source weight, recency and score only).

It is a tech demo hosted on Azure using **only always-free services**. Cost safety outranks features.

**Status:** scaffolding and plans only. Check `docs/plans/` for what is built and what is next; tick the checkboxes in a plan when its tasks land.

## Architecture

```
GitHub Actions --build--> GHCR images ----> Azure Container Apps (API, min replicas 0)
sources.yaml --> Container Apps Job (cron ingest) --> Cosmos DB (free tier) <-- API
Browser --> Static Web Apps (React SPA) --> API (/days, /days/{date})
```

## Layout

| Path | Purpose |
|---|---|
| `api/` | FastAPI BFF (Python) |
| `ingest/` | Scheduled ingest job (Python) |
| `web/` | React + Vite + TypeScript + MUI |
| `infra/` | Bicep (IaC) |
| `docs/plans/` | Numbered build plans, 00-08 |
| `sources.yaml` | Source registry (RSS, HN, arXiv, GitHub trending, Reddit) |

## Commands

Not implemented yet. Plan 01 will define and document them here; the intended set is:

- Python (`api/`, `ingest/`): `uv sync`, `uv run ruff check .`, `uv run ruff format .`, `uv run pytest`
- Web (`web/`): `pnpm install`, `pnpm lint`, `pnpm test`, `pnpm build`, `pnpm dev`
- Infra: `az bicep build -f infra/main.bicep`, `az deployment group what-if ...`

Update this section as soon as real commands exist. Do not document commands that don't work.

## Conventions

- Python 3.12+, type hints, ruff for lint and format, pytest. Config in `pyproject.toml` per package.
- TypeScript strict mode. MUI theme in one place; no ad-hoc inline colours.
- The API contract is OpenAPI generated from FastAPI and is the source of truth; the web client types derive from it. Keep it clean and client-agnostic so a Flutter client could be added.
- Conventional-style commit messages, small commits, one concern per PR.
- Config over code: new sources go in `sources.yaml`, not in Python.
- No secrets in the repo. Azure access is by OIDC federated credentials. Never add long-lived keys.
- Never commit to `main`; always work on a branch and open a PR.

## Free-tier constraints and cost guardrails

Allowed: Container Apps (consumption) + Jobs, Cosmos DB free tier, Static Web Apps Free, Log Analytics within its 5 GB/month free allowance, GHCR for images.

**Forbidden** (not permanently free or billable): Azure Container Registry, Azure Storage accounts, Postgres Flexible Server, Static Web Apps Standard, dedicated/workload-profile Container Apps, Application Insights beyond the free allowance, additional Cosmos accounts/databases/containers with their own throughput.

Rules:
- API container: `minReplicas: 0`, small size (0.25 vCPU / 0.5 GiB), `maxReplicas` low (1-2).
- Cosmos: one free-tier account, one shared-throughput database at most 1000 RU/s total, under 25 GB.
- Log Analytics workspace has a daily ingestion cap. Keep logs concise.
- Ingest runs at most a few times a day and exits promptly.
- A budget alert must exist before anything else is deployed.
- Free-tier numbers live in `docs/plans/00-overview-architecture.md` with a "last verified" date. Re-verify against Microsoft docs before changing anything cost-relevant. Unconfirmed items are flagged there.
- If a change might add a billable resource, stop and ask the user first.

## Ask first (do not do unprompted)

Creating or changing Azure resources, pushing to `main`, changing GitHub repo settings, adding secrets, adding any new paid or unlisted service, force-pushing, deleting branches or resources.

## Working from the Claude Code mobile app

- Keep PRs small and reviewable on a phone screen: aim for under ~100 changed lines, one concern each, with a 3-line description (what, why, how to verify).
- Prefer config and UI changes (`sources.yaml`, theme, copy, layout) over deep logic changes.
- Don't paste huge diffs in chat; summarise and link files.
- Before opening a PR, run what CI will run (once it exists) and say what you ran.
- **Verifying a deploy:** after merge, check the Actions run for `main` is green, then call the API `GET /health`, which returns the deployed git SHA and compare to the merge commit. For front end changes, load the SWA URL; PRs get a preview URL posted as a comment.
- If a deploy fails, say so with the failing step's log excerpt; do not retry blindly or "fix" by disabling checks.
- Hotfix path: branch from `main`, minimal fix, PR, merge, verify. See plan 07.
