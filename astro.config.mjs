import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://zecure.net',
  // x.astro -> x.html (served at /x); dir/index.astro -> dir/index.html (served at /dir/)
  build: { format: 'preserve' },
  trailingSlash: 'ignore',
});
