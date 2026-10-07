# 07 Mobile-workflow experiments

## Goal
Learn how far real development can go from the Claude Code mobile app, with a graded set of changes and a way to observe the running service.

## Scope
Experiments on the finished (or partly finished) system. Record findings in `docs/mobile-notes.md` as you go.

## Graded experiments

| Level | Change | Example | Done when |
|---|---|---|---|
| 1 Config | Edit `sources.yaml` | Add or disable a feed | PR passes schema check; after merge and the next ingest run, items from it appear |
| 2 Small UI tweak | Theme or copy change | Change the accent colour, card density or empty-state text | PR preview URL shows it on the phone; merge deploys it |
| 3 New feature | Small end-to-end feature | A "Hide source" toggle (UI only), or a `?min_score=` filter across API and UI | Tests added, contract updated, preview verified, production verified |
| 4 Hotfix | Fix a deliberately introduced or real bug | Break a parser or a date format, then fix from the phone | Time from report to verified deploy is recorded |
| 5 Stretch | Ops change | Adjust the ingest cron or the log retention via Bicep | what-if reviewed on phone; owner approves; deploy verified |

For each: note PR size, readability on a small screen, how many round trips were needed, what was awkward (diff review, log reading, approvals), and what to change in CLAUDE.md as a result.

## Observing the running service
- **Health:** `GET <api>/health` shows SHA and time. Compare with the merge commit.
- **Deploy status:** the GitHub Actions run summary and the PR checks.
- **Ingest runs:** `az containerapp job execution list` (via a workflow with `workflow_dispatch` that prints status, since the phone has no az CLI); the Azure portal mobile app also shows job executions.
- **Logs:** a small "show recent logs" workflow that queries Log Analytics (KQL) and prints the last N error lines to the run summary.
- **Cost:** the Azure mobile app, Cost Management and budget alert emails.
- **Data freshness:** the UI footer shows "last ingested at" (from the API), a cheap visible signal.

## Tasks
- [ ] Add `workflow_dispatch` helper workflows: trigger ingest, job status, recent logs (read-only)
- [ ] Add "last ingested" to the API and UI footer
- [ ] Add PR template checklist for mobile (what, why, verify)
- [ ] Run each level and record notes
- [ ] Fold learnings back into CLAUDE.md

## Acceptance criteria
- Levels 1-4 completed entirely from the mobile app.
- Each has a recorded outcome and a time.
- Observation workflows work from the phone.

## Risks
- The workflows' Azure read access must stay read-only (separate federated subject and Reader role).
- Reviewing diffs on a phone is hard, so keep PRs small; split any that grow.
- Hotfix experiments must not break production for long. Introduce bugs only on a branch, with a preview, never on main.
