import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const lectures = defineCollection({
  loader: glob({ pattern: '*.mdx', base: './src/content/lectures' }),
  schema: z.object({
    num: z.number(),
    short: z.string(),                 // browser tab title
    heading: z.string(),               // page headline
    lede: z.string(),
    board: z.enum(['bloch', 'pair']),  // simulator pinned beside the notes
    boardLabel: z.string(),
    nextNote: z.string().optional(),   // sentence shown after the pointer to the next lecture
  }),
});

export const collections = { lectures };
