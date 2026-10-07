# 04 BFF API

## Goal
A small, clean, client-agnostic HTTP API that serves the digest to the SPA (and later Flutter).

## Scope
`api/` FastAPI app. Read-only in v1.

## Contract (draft)
- `GET /days?limit=&before=`: list of available days with item counts (newest first)
- `GET /days/{date}?tag=&source=&limit=&cursor=`: ranked items for a day, with `sources` and `tags` facets
- `GET /sources`: enabled sources (id, name, tags), for filter UI
- `GET /health`: `{status, sha, time}`; no DB call by default, `?deep=1` checks Cosmos
- Errors as RFC 9457 problem+json. Versioning via the OpenAPI document; no `/v1` prefix until needed.
- OpenAPI JSON committed to `api/openapi.json` and checked in CI for drift.

## Design
- Reads from Cosmos with the partition key (`day`), so every query is single-partition and cheap.
- Cache headers (`Cache-Control: public, max-age=300`, ETag) so repeated loads cost no RUs and fewer requests.
- Small in-process cache; the app can scale to zero, so no reliance on it.
- CORS allow-list: the SWA origin(s) and localhost for dev.
- Managed identity auth to Cosmos; fake in-memory repo for tests and local dev.
- Rate limiting: basic per-IP limit to protect the free grants, with a hard cap on `limit`.
- No auth in v1 (public read-only data).

## Tasks
- [ ] Pydantic models matching the ingest item model (shared via a small package or duplicated and tested for parity)
- [ ] Repository interface, Cosmos and in-memory implementations
- [ ] Endpoints above, plus tests with the in-memory repo
- [ ] Problem+json error handlers
- [ ] CORS, cache headers, request limits
- [ ] `GIT_SHA` build arg surfaced by `/health`
- [ ] OpenAPI export script and CI drift check
- [ ] Dockerfile (slim, non-root, uvicorn, 1 worker)
- [ ] Measure cold start and RU per request; record in this doc

## Acceptance criteria
- All endpoints covered by tests; OpenAPI is valid and stable.
- Typical `GET /days/{date}` costs under ~10 RU.
- Cold start under ~5s on Container Apps.
- `/health` reports the deployed SHA.

## Risks
- Cold starts hurt the UX, so keep the image small and imports light.
- Public endpoint abuse can burn the free request grant; a rate limit and caching mitigate it. Consider a Container Apps IP restriction if needed.
- Contract changes break the SPA, so generate client types from OpenAPI and break CI on drift.
