# Zecure

**Free cryptographically secure password and key generator — runs 100% in your browser.**

No signup. No server. No data collection. Everything is generated locally using `window.crypto.getRandomValues()` — the same CSPRNG your browser uses for TLS.

---

## Features

- **12 key types** across 4 categories
- **100% client-side** — nothing is ever sent to a server
- **Bias-free** — uses rejection sampling to eliminate modulo bias
- **Light / dark mode** with `localStorage` persistence
- **Fully accessible** — ARIA labels, keyboard navigation, skip link, `prefers-reduced-motion`
- **Mobile responsive** — works on all screen sizes
- **No build step** — open `index.html` directly in any browser

### Key Types

| Category | Types |
|---|---|
| Passwords | Random (8–15 chars), Memorable, Strong (20 chars), Fort Knox (32 chars) |
| Keys | UUID v4, JWT Secret, AES-256, Database Password, Secret Token |
| WiFi | WPA2 (63 chars), WEP-128, WEP-256 |

---

## How It Works

```js
// Cryptographically secure integer in [0, max) — no modulo bias
function secureInt(max) {
  const limit = Math.floor(0xFFFFFFFF / max) * max;
  let n;
  do {
    n = new Uint32Array(1);
    crypto.getRandomValues(n);
  } while (n[0] >= limit); // rejection sampling
  return n[0] % max;
}
```

All generators draw from this function. No `Math.random()` is used anywhere.

---

## Tech Stack

| Layer | Choice |
|---|---|
| HTML | Semantic HTML5, single file |
| CSS | Custom properties (design tokens), no framework |
| JS | Vanilla ES2020, Web Crypto API |
| Fonts | Inter + JetBrains Mono (Google Fonts) |
| Icons | Inline SVG (Heroicons / Lucide style) |

---

## Blog

Three in-depth security articles in `blog/`:

- [How to Create an Unbreakable Password in 2025](blog/unbreakable-password-2025.html)
- [AES-256 Encryption Explained in Plain English](blog/aes-256-explained.html)
- [API Keys vs. Passwords: What's the Difference?](blog/api-keys-vs-passwords.html)

---

## Getting Started

```bash
git clone https://github.com/majmalnm/zecure.git
cd zecure
open index.html   # macOS
# or just double-click index.html on any OS
```

No `npm install`. No build step. No dependencies.

---

## Hosting

### GitHub Pages

1. Go to **Settings → Pages**
2. Source: Deploy from branch `main`, folder `/ (root)`
3. Live at `https://majmalnm.github.io/zecure/`

### Any Static Host

Drop the folder on Netlify, Vercel, Cloudflare Pages, or any web server — it's all static files.

---

## Project Structure

```
zecure/
├── index.html                          # Main app — generator + FAQ + blog index
├── blog/
│   ├── unbreakable-password-2025.html  # Security guide article
│   ├── aes-256-explained.html          # AES-256 explainer article
│   └── api-keys-vs-passwords.html      # Developer article
├── .gitignore
├── CHANGELOG.md
└── README.md
```

---

## Security

- No analytics, no tracking, no external requests (except Google Fonts)
- Fonts can be self-hosted to make it fully offline-capable
- Content Security Policy compatible — no `eval`, no `innerHTML` on user input
- All generated values exist only in the browser's memory and are discarded on page close

---

## License

MIT — free to use, modify, and self-host.
