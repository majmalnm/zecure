# Translating a page to Arabic (RTL)

English pages in `src/site/en/` are the source of truth. The Arabic page for `src/site/en/<key>.html` is
`src/site/ar/<key>.html`. The layout (`src/layouts/Page.astro`) already sets `lang="ar" dir="rtl"`, loads
IBM Plex Sans Arabic, generates canonical/hreflang/og:url, adds the language switcher, and points links at
Arabic pages when they exist. Don't hand-edit any of that.

## What to translate

- **Meta block** (`<!--meta {json} -->`): `title`, `description`, `keywords`, `ogTitle`, `ogDescription`.
  Keep `robots`, `ogType`, `sitemap` as they are. Keywords: natural phrasing Arabic users actually search
  (e.g. "مولد كلمات المرور", "كلمة سر قوية", "إنشاء كلمة مرور قوية"), not literal translations. Keep the
  `| Zecure` suffix pattern in titles.
- **JSON-LD**: translate human-readable strings (`name`, `headline`, `description`, FAQ `name`/`text`) and add
  `"inLanguage": "ar"` to the top-level WebPage/Article/etc. object(s). Leave URLs as they are (the build
  localizes them). FAQ JSON-LD text must match the visible FAQ text on the page.
- **Body**: every piece of visible text, plus `aria-label`, `title`, `alt`, `placeholder` attributes.
- **JavaScript**: only user-facing strings (toast text, labels, badges, strength words, button text, error
  messages, text built with template literals). Logic stays byte-for-byte the same otherwise.

## What NOT to change

- Markup structure, classes, IDs, `onclick` handlers, link `href`s, CSS rules, script logic.
- Code, commands, file names, generated values, character-set labels (`A-Z`, `!@#`), and technical names:
  UUID, JWT, AES-256, SHA-256, Base64, bcrypt, Argon2, HMAC, CSPRNG, API, WPA2, NIST, `getRandomValues()`.
  Use the Latin term, and on first mention in prose you may add a short Arabic explanation.
- Word lists used to build passwords/passphrases (themed generators, passphrase words): they stay as they
  are. Passwords must stay ASCII so they work on every system.
- Facts. Translate faithfully: add no new claims, no prices, no "best/#1" claims, no statistics that are not
  in the English page. Keep the brand as `Zecure` (Latin).

## RTL rules

- Elements that display generated values, keys, hashes, passwords, code, or URLs: add `dir="ltr"` to the
  existing element (don't wrap in new elements). `pre`/`code`/`kbd` are already forced LTR by the layout.
- Free-text inputs/textareas where users type their own content: add `dir="auto"`.
- Arrow/chevron icons that point forward or back (e.g. `points="9 18 15 12 9 6"`, `points="15 18 9 12 15 6"`,
  arrow-right lines): add `class="flip-rtl"` to the `<svg>` (merge with any existing class).
- If the page CSS uses physical directions that look wrong in RTL (`left`/`right`, `margin-left`,
  `padding-right`, `border-left` on callouts, `text-align:left`, `translateX` slide-ins), do NOT edit the
  existing CSS. Append one extra `<style>` block at the end of the head section with overrides scoped to
  `html[dir=rtl]`, e.g. `html[dir=rtl] .callout{border-left:none;border-right:3px solid var(--accent)}`.
- Use Western digits (0–9). Arabic month names for dates (يناير، فبراير، مارس، أبريل، مايو، يونيو، يوليو،
  أغسطس، سبتمبر، أكتوبر، نوفمبر، ديسمبر). Arabic punctuation (، ؛ ؟) in Arabic sentences.

## Style

Modern Standard Arabic, clear and natural for a Gulf/Arab tech audience; translate meaning, not word order.
Keep it as direct as the English. Headings short.

## Glossary (use consistently)

| English | Arabic |
|---|---|
| password | كلمة المرور |
| strong password | كلمة مرور قوية |
| passphrase | عبارة مرور |
| generator | مولّد |
| password generator | مولّد كلمات المرور |
| key / secret key | مفتاح / مفتاح سري |
| secret (JWT secret etc.) | سرّ / المفتاح السري |
| encryption / decryption | التشفير / فك التشفير |
| hash / hashing | التجزئة (hash) / دالة التجزئة |
| encoding / decoding | الترميز / فك الترميز |
| entropy | الإنتروبيا (مقدار العشوائية) |
| brute-force attack | هجوم القوة الغاشمة |
| dictionary attack | هجوم القاموس |
| random / randomness | عشوائي / العشوائية |
| cryptographically secure | آمن تشفيريًا |
| client-side / in your browser | داخل متصفحك |
| no signup | دون تسجيل |
| two-factor authentication (2FA) | المصادقة الثنائية (2FA) |
| password manager | مدير كلمات المرور |
| uppercase / lowercase | أحرف كبيرة / أحرف صغيرة |
| numbers / symbols | أرقام / رموز |
| length | الطول |
| character pool / set | مجموعة الأحرف |
| copy / copied | نسخ / تم النسخ |
| regenerate | إعادة التوليد |
| all generators | كل المولّدات |
| blog | المدونة |
| privacy policy / terms | سياسة الخصوصية / شروط الاستخدام |
| WiFi | الواي فاي |
| developer | المطوّر |
| read time "8 min read" | "قراءة 8 دقائق" |

## Check your page

```bash
python3 scripts/check-ar.py <key>     # e.g. password-generator, blog/aes-256-explained
```

It verifies structure, IDs/classes, script syntax, JSON validity, and lists any leftover English sentences.
Fix everything it reports (leftover Latin that is a technical term or code is fine).
