# 01 Repo & CI skeleton

## Goal
Working lint/test/build pipelines for each package on every PR, with empty-but-valid projects, so later phases land with CI already guarding them.

## Scope
Project skeletons (hello-world level), tooling config, GitHub Actions CI. No deploy (see 06). No product logic.

## Tasks
- [x] `api/`: `pyproject.toml` (uv), ruff config, pytest, a trivial `/health` test
- [x] `ingest/`: same toolchain, trivial test
- [ ] `web/`: Vite + React + TS (strict) + MUI, eslint, vitest, `pnpm build`
- [ ] `infra/`: placeholder `main.bicep` that passes `az bicep build`
- [ ] `.github/workflows/ci-api.yml`, `ci-ingest.yml`, `ci-web.yml`, `ci-infra.yml` with path filters; each runs lint, test, build
- [ ] A required-status "CI OK" aggregate job so path-filtered workflows don't block merging
- [ ] `sources.yaml` JSON-schema validation job (cheap and phone-friendly)
- [ ] Dependabot config (weekly, grouped)
- [ ] Pin Actions to versions or SHAs; minimal `permissions:` per workflow
- [ ] Update CLAUDE.md "Commands" with the real commands
- [ ] PR template (what / why / how verified)
- **Owner (manual):** enable branch protection on `main` requiring the CI aggregate check

## Acceptance criteria
- A PR touching only `web/` runs only web CI and passes; same for the others.
- A deliberately broken lint/test fails the PR.
- CLAUDE.md commands all work from a clean checkout.
- CI runtime under ~5 min per workflow.

## Risks
- Path filters plus required checks can deadlock merges; the aggregate job addresses this.
- Actions minutes are free only for public repos; keep the repo public or recheck.
