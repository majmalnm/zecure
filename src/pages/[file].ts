import { pages, urlPath } from '../lib/site';

// Cloudflare Workers static assets config files. Astro skips _-prefixed pages, hence the dynamic route.
export function getStaticPaths() {
  return [{ params: { file: '_redirects' } }];
}

// The old canonical/sitemap URLs ended in .html; send them to the clean URLs with a permanent redirect.
export function GET() {
  const lines = pages
    .filter((p) => p.lang === 'en')
    .map((p) => `/${p.key}.html ${urlPath('en', p.key)} 301`)
    .sort();
  return new Response(lines.join('\n') + '\n');
}
