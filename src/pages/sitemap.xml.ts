import { pages, SITE, urlPath, alternates } from '../lib/site';

// Only pages flagged for the sitemap (the joke generators and the Linux cheat sheet were never listed).
export function GET() {
  const listed = pages.filter((p) => p.meta.sitemap);
  const urls = listed
    .sort((a, b) => (a.lang + a.key).localeCompare(b.lang + b.key))
    .map((p) => {
      const alts = alternates(p.key);
      const links = alts.length > 1
        ? alts.map((a) => `\n    <xhtml:link rel="alternate" hreflang="${a.lang}" href="${a.href}"/>`).join('') +
          `\n    <xhtml:link rel="alternate" hreflang="x-default" href="${alts.find((a) => a.lang === 'en')!.href}"/>`
        : '';
      return `  <url>\n    <loc>${SITE}${urlPath(p.lang, p.key)}</loc>${links}\n  </url>`;
    })
    .join('\n');
  const xml = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n${urls}\n</urlset>\n`;
  return new Response(xml, { headers: { 'Content-Type': 'application/xml' } });
}
