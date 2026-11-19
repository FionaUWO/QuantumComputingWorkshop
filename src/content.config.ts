import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

// One file per section: src/content/lectures/<lecture-slug>/<nn>-<section-slug>.mdx
// The number prefix sets the order; lecture-level details live in src/data/lectures.ts.
const lectures = defineCollection({
  loader: glob({ pattern: '*/*.mdx', base: './src/content/lectures' }),
  schema: z.object({
    title: z.string(),
    board: z.boolean().default(true), // false hides the simulator on this page
  }),
});

export const collections = { lectures };
