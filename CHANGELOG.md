# Changelog

All notable changes to Zecure are documented here.

---

## [0.4.0] — 2026-04-12

### Added
- **3 full blog post pages** — each a standalone HTML file with article layout, callout boxes, syntax-highlighted code examples, stat strips, and related-posts navigation
  - `blog/unbreakable-password-2025.html` — Security Guide: modern NIST guidelines, entropy math, CSPRNG explanation
  - `blog/aes-256-explained.html` — Explainer: how AES works, key size comparison, GCM vs ECB vs CBC, AES flow diagram
  - `blog/api-keys-vs-passwords.html` — Developer: side-by-side comparison table, server-side storage patterns, rotation strategy
- **README.md** — project overview, tech stack, hosting instructions, security notes
- **CHANGELOG.md** — this file
- **`.gitignore`** — excludes `.DS_Store`, `.env`, `node_modules`
- **GitHub repository** — `https://github.com/majmalnm/zecure`

### Changed
- Blog cards on homepage now link to real article pages (previously all pointed to `#blog` anchor)
- Blog post `href` added as a property to the `POSTS` data array

### Notes
- Dark mode was already the default (`data-theme="dark"` on `<html>`); confirmed no change needed
- Theme persistence via `localStorage` only overrides the dark default if the user explicitly toggles

---

## [0.3.0] — 2026-04-12

### Changed (Full Redesign — from scratch)
- **Complete rewrite** of `index.html` — previous cyberpunk/neon aesthetic replaced entirely
- New design system: shadcn / Linear / Vercel aesthetic
  - Zinc-950 dark background, white light background
  - Indigo-500 accent color
  - Inter (UI text) + JetBrains Mono (generated output) typography
  - Full CSS custom properties with `[data-theme="light"]` overrides

### Added
- **Dot-grid hero** — pure CSS `radial-gradient` + `mask-image` fade, no images
- **Category filter tabs** — All / Passwords / Keys / WiFi with live count badges
- **4-segment strength meter** — replaced thin progress bar
- **Icon-only copy button** — clipboard SVG swaps to checkmark on success, 1.5s timeout
- **6 card accent colors** — `c-indigo`, `c-violet`, `c-green`, `c-amber`, `c-red`, `c-sky` with separate dark/light overrides
- **Frosted glass navbar** — `backdrop-filter: blur(16px)` with `color-mix()` transparency
- **Mobile hamburger menu**
- **Skip-to-content link** for keyboard users
- **`prefers-reduced-motion`** respected throughout
- **`keyboard shortcut `R`** to regenerate all keys
- Keyboard shortcut hint (<kbd>R</kbd>) displayed in navbar

### Preserved
- All 12 key types and their generators
- Light/dark toggle with `localStorage`
- Step-by-step FAQ section
- Blog card section

---

## [0.2.0] — 2026-04-12

### Added
- **Light / dark theme toggle** — `[data-theme]` attribute on `<html>`, persisted to `localStorage`
- **Blog section** — 3 article cards (Security Guide, Explainer, Developer) with gradient covers
- **Step-by-step FAQ answers** — 5 of 8 FAQ items now render numbered step guides instead of plain paragraphs
  - Data structure: `{ q, steps: [{ t, b }] }` vs `{ q, a }`
  - `renderFAQ()` supports both formats

### Changed
- Meta `<title>` updated to use common user search terms ("free password generator", "create strong passwords")
- Meta `description` rewritten for search intent ("Create strong random passwords and secret keys in seconds")
- Added `keywords` meta tag with long-tail search terms
- Typography improvements: tighter letter-spacing on headings, improved line-height on body

### Fixed
- FAQ step list border-top: added `.faq-item.open .faq-a .step-list { border-top: 1px solid var(--border); }` to restore visual separator for step-based answers
- Changed `.faq-a p` selector to `.faq-a > p` to prevent step content paragraphs from inheriting the wrong top border style

---

## [0.1.0] — 2026-04-12

### Initial build
- Single-file SPA (`index.html`) — all CSS, HTML, and JS inline
- **Web Crypto API** (`window.crypto.getRandomValues()`) for CSPRNG-based generation
- **Rejection sampling** (`secureInt`) to eliminate modulo bias
- **12 key types** across 3 groups: Passwords (4), Keys (5), WiFi (3)
- Cyberpunk / neon dark aesthetic — cyan and magenta accents on near-black background
- Accordion FAQ section (8 questions)
- Responsive layout, accessible markup
- Copy-to-clipboard on each generated value
- Strength indicator per password card
- SEO meta tags, Open Graph, JSON-LD structured data (WebSite, WebApplication, FAQPage)
