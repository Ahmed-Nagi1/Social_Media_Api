// @ts-check
import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import htmx from 'astro-htmx'

import preact from '@astrojs/preact';

// https://astro.build/config
export default defineConfig({
    integrations: [tailwind(), htmx(), preact()],
});