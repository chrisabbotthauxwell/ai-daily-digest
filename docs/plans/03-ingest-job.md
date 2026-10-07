# 03 Ingest job

## Goal
A scheduled job that reads `sources.yaml`, fetches items from each source, and stores a ranked, deduplicated set per day in Cosmos DB.

## Scope
`ingest/` package and `sources.yaml` schema. No LLM. Optional summarisation is left as a hook (see 08).

## Source types
`rss` (Atom and RSS), `hackernews` (Firebase or Algolia API, AI keyword filter plus score threshold), `arxiv` (cs.AI and cs.CL via the arXiv API, respecting its rate-limit guidance), `github_trending` (no official API, so choose between scraping and a search-API proxy; see risks), `reddit` (subreddit JSON/RSS).

## Design
- Each fetcher implements `fetch(source) -> list[RawItem]`; failures are isolated per source and logged.
- Normalise to the item model in plan 00; `id` = hash of canonical URL (strip tracking params).
- Day = UTC date of `published_at` (fallback `fetched_at`).
- Rank = weighted combination of source `weight`, recency decay and normalised native score. Pure function with unit tests.
- Upsert is idempotent, so re-runs do not duplicate. Writes are batched per partition (day) to save RUs.
- Tags come from `sources.yaml` tags plus simple keyword rules.
- Exit non-zero only if all sources fail or Cosmos is unavailable.
- Config: `COSMOS_ENDPOINT`, DB and container names via env. Auth via managed identity (`DefaultAzureCredential`); a local Cosmos emulator or in-memory store for dev.

## Tasks
- [ ] Finalise `sources.yaml` schema plus JSON schema (used by CI in 01)
- [ ] Data model and storage interface with Cosmos and in-memory implementations
- [ ] Fetchers: RSS, HN, arXiv, Reddit, GitHub trending, with recorded fixtures for tests
- [ ] Dedup, canonical URL, tagging
- [ ] Ranking function with tests
- [ ] CLI entrypoint (`python -m ingest`, flags `--dry-run`, `--source <id>`)
- [ ] Dockerfile (slim, non-root)
- [ ] Structured, low-volume logging (one summary line per source)
- [ ] RU usage measured and recorded (target: a run costs well under 1000 RU/s sustained)
- [ ] Seed `sources.yaml` with 5-10 reputable sources

## Acceptance criteria
- `--dry-run` prints the day's ranked items from fixtures offline.
- Re-running yields no duplicates.
- One failing source does not stop others.
- Container image under ~200 MB; a run finishes in under 2 minutes for the seed list.
- Monthly job compute (runs x seconds x vCPU) estimated and under 10% of the free grant.

## Risks
- Reddit API terms and auth requirements (may need an app registration; public JSON is rate-limited and may be blocked from cloud IPs).
- GitHub trending has no stable API; scraping is brittle. Could drop it to a later phase if flaky.
- arXiv volume is high, so apply a cap per run.
- Cosmos RU spikes from large batches; throttle with 429 retry/backoff.
- Source-side terms of use: store only title, link and metadata, never full content.
