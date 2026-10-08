// Page sources live in src/site/<lang>/<key>.html:
//   <!--meta {json} -->  <!--head--> page head HTML  <!--body--> page body HTML
// English is the source of truth; a page exists in Arabic when src/site/ar/<key>.html exists.

export const SITE = 'https://zecure.net';
export const LANGS = ['en', 'ar'] as const;
export type Lang = (typeof LANGS)[number];

export interface PageMeta {
  title: string;
  description?: string;
  keywords?: string;
  robots?: string;
  ogType?: string;
  ogTitle?: string;
  ogDescription?: string;
  sitemap?: boolean;
}

export interface Page {
  lang: Lang;
  key: string; // 'index', 'password-generator', 'blog/index', 'blog/aes-256-explained'
  meta: PageMeta;
  head: string;
  body: string;
}

const raw = import.meta.glob('/src/site/*/**/*.html', { query: '?raw', import: 'default', eager: true }) as Record<string, string>;

function parse(file: string, src: string): Page {
  const m = file.match(/^\/src\/site\/(en|ar)\/(.+)\.html$/);
  if (!m) throw new Error(`Unexpected page source path: ${file}`);
  const parts = src.match(/^<!--meta\n([\s\S]*?)\n-->\n<!--head-->\n([\s\S]*?)<!--body-->\n([\s\S]*)$/);
  if (!parts) throw new Error(`Malformed page source: ${file}`);
  return { lang: m[1] as Lang, key: m[2], meta: JSON.parse(parts[1]), head: parts[2], body: parts[3] };
}

export const pages: Page[] = Object.entries(raw).map(([f, s]) => parse(f, s));

const byLang = (lang: Lang) => new Set(pages.filter((p) => p.lang === lang).map((p) => p.key));
const keys: Record<Lang, Set<string>> = { en: byLang('en'), ar: byLang('ar') };

export function hasPage(lang: Lang, key: string) {
  return keys[lang].has(key);
}

/** Clean URL path the server answers 200 on: 'index' -> '/', 'blog/index' -> '/blog/', 'x' -> '/x' */
export function urlPath(lang: Lang, key: string) {
  const prefix = lang === 'en' ? '' : `/${lang}`;
  if (key === 'index') return `${prefix}/`;
  if (key.endsWith('/index')) return `${prefix}/${key.slice(0, -'index'.length)}`;
  return `${prefix}/${key}`;
}

/** Inverse of urlPath for English paths: '/blog/' -> 'blog/index', '/x' -> 'x' */
function keyFromPath(path: string) {
  if (path === '/' || path === '') return 'index';
  const p = path.replace(/^\//, '');
  return p.endsWith('/') ? `${p}index` : p;
}

/**
 * Point site links in a translated page at the same-language page when one exists.
 * Sources use English root-relative URLs; links to untranslated pages stay on English.
 */
export function localizeLinks(lang: Lang, html: string) {
  if (lang === 'en') return html;
  const swap = (path: string) => {
    const key = keyFromPath(path);
    return hasPage(lang, key) ? urlPath(lang, key) : path;
  };
  return html
    .replace(/(href\s*[=:]\s*)(["'])(\/(?!\/)[^"'#?]*)/g, (_, a, q, path) => a + q + swap(path))
    .replace(/(https:\/\/zecure\.net)(\/[A-Za-z0-9_./-]*)/g, (_, host, path) => host + swap(path));
}

export function alternates(key: string) {
  return LANGS.filter((l) => hasPage(l, key)).map((l) => ({ lang: l, href: SITE + urlPath(l, key) }));
}
