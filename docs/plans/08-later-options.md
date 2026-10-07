# 08 Later options

Not committed work. Each is independent and must respect the free-tier guardrails in plan 00.

## A. LLM summaries behind a cost cap
- **Goal:** one-line summary and better tags per top-N item per day.
- **Design:** optional ingest step, off by default (`SUMMARIZE=true`); only top N items per day (e.g. 20); small, cheap model; cache by item id so nothing is summarised twice; store in the item as `summary`.
- **Cost cap:** a hard monthly budget in code (token counting plus a counter document in Cosmos), failing closed; plus a provider-side spend limit. This is not an Azure free service, so it is **explicitly paid**; the owner must opt in and set the cap.
- **Tasks:** [ ] summariser interface and null implementation [ ] cap and counter [ ] prompt and eval on 20 samples [ ] UI shows the summary when present [ ] cost report in the job log.
- **Acceptance:** with the cap set to $0, no calls are made; spend never exceeds the cap in a forced-overrun test.
- **Risks:** summaries misrepresent articles, so label them as generated and link the source; prompt injection from article titles; secret handling for the API key (Container Apps secret, the first real secret).

## B. AI Release Radar (second ingest source)
- **Goal:** track model, library and tool releases (GitHub releases, model hubs, changelog feeds) as a distinct feed.
- **Design:** a new item `kind: release` in the same container, a new fetcher type in `sources.yaml` (`github_releases`), and a UI tab or filter. Reuses the API with `?kind=`.
- **Tasks:** [ ] extend the schema [ ] fetchers [ ] ranking for releases (version and recency) [ ] UI tab [ ] tests.
- **Risks:** GitHub API rate limits (use a token only if needed); noise from minor releases, so apply allow-lists and thresholds.

## C. Flutter client (comparison)
- **Goal:** compare the React and Flutter developer experience against the same API.
- **Design:** `app/` or `flutter/` folder, client generated from OpenAPI, deployed as Flutter web to a second SWA app (Free allows 10 apps), or just run locally.
- **Tasks:** [ ] confirm that the contract needs no changes [ ] scaffold and generate the client [ ] feed and day picker [ ] write up a comparison (effort, bundle size, mobile editing experience).
- **Risks:** Flutter web bundle size against the 250 MB limit (fine) and load time; the mobile-editing experience of Dart is a point of the comparison.

## D. Smaller ideas
- Custom domain on SWA (2 free), RSS output of the digest, weekly digest page, cross-day trending, email digest (needs a mail service, so likely not free).
