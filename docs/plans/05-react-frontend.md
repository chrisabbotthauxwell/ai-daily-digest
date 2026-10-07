# 05 React front end

## Goal
A responsive, Material 3-styled SPA to browse the digest by day, comfortable on phone and desktop.

## Scope
`web/`: React + Vite + TypeScript (strict) + MUI. Read-only UI against the API contract in 04.

## UX
- **Mobile:** app bar with menu button, left drawer for filters (tags, sources) and the day list; day picker as a bottom sheet or date control; single-column feed.
- **Desktop:** permanent drawer or sidebar for filters, content column with the day header and a day picker; wider cards with source, time and score.
- Item card: title (external link, `rel="noopener noreferrer"`), source chip, tags, relative time, score.
- States: loading skeletons, empty day, error with retry, cold-start hint after ~2s.
- Light and dark by system preference. MUI theme with Material 3 look (custom tokens in a single `theme.ts`; MUI's native M3 support is limited, so verify what is currently available).
- Filters and selected day live in the URL (`/2026-10-07?tag=research`), so links are shareable.
- Accessibility: keyboard navigation, focus management for the drawer, contrast checks.

## Design
- API client types generated from `api/openapi.json` (e.g. openapi-typescript) plus a thin fetch wrapper.
- TanStack Query for caching and retries; React Router for URLs.
- `VITE_API_BASE_URL` at build time; SWA config for SPA fallback routing (`staticwebapp.config.json`).
- No analytics or third-party scripts in v1.

## Tasks
- [ ] Theme and layout shell: responsive app bar and drawer
- [ ] Generated API client and query hooks
- [ ] Day picker (prev/next plus calendar limited to available days)
- [ ] Feed list, item card and filter controls (tag and source)
- [ ] URL-synced state
- [ ] Loading, empty, error and cold-start states
- [ ] Component tests (vitest and Testing Library) and a few Playwright smoke tests at mobile and desktop widths
- [ ] `staticwebapp.config.json`: SPA fallback, security headers (CSP restricted to the API origin)
- [ ] Lighthouse pass (performance and accessibility at least 90)

## Acceptance criteria
- Usable at 360px and 1440px widths with no horizontal scroll.
- Works against the in-memory or mock API locally (`pnpm dev` with MSW or the API running locally).
- Build output well under the 250 MB SWA limit (expected under 2 MB).
- Deep links and refresh work.

## Risks
- MUI isn't natively Material 3, so a pure M3 look takes theming effort; accept "M3-inspired".
- API cold starts make the first paint slow; skeletons and a retry mitigate it.
- CSP and CORS misconfiguration; test against the deployed API in a preview.
- Keep the API contract free of web-specific assumptions to preserve the Flutter option.
