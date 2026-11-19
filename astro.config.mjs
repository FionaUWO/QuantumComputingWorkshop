import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import { unified } from '@astrojs/markdown-remark';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

// Published at https://fionauwo.github.io/QuantumComputingWorkshop/
export default defineConfig({
  site: 'https://fionauwo.github.io',
  base: '/QuantumComputingWorkshop',
  trailingSlash: 'always',
  integrations: [mdx()],
  // Lecture notes are Markdown with LaTeX; KaTeX renders the formulas at build time.
  markdown: {
    processor: unified({
      remarkPlugins: [remarkMath],
      rehypePlugins: [rehypeKatex],
    }),
  },
});
