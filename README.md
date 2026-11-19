# Quantum Computing Workshop

Eight one-hour lectures on quantum computing for undergraduates in mathematics, run by the Q-AICON Lab at Western University.

Live site: https://fionauwo.github.io/QuantumComputingWorkshop/

## Working on the site

The site is built with [Astro](https://astro.build). You need Node.js 22.23 or newer.

```
npm install
npm run dev
```

Then open http://localhost:4321/QuantumComputingWorkshop/. `npm run build` writes the finished site to `dist/`.

Pushing to `main` builds and publishes the site through GitHub Actions (`.github/workflows/deploy.yml`).

## Where things are

| Path | What it holds |
| --- | --- |
| `src/content/lectures/*.mdx` | Lecture notes, in Markdown with LaTeX between `$` signs |
| `src/data/lectures.ts` | The list of eight lectures shown on the home page |
| `src/pages/` | Home page, playground, and the template for lecture pages |
| `src/layouts/Base.astro` | Header and footer shared by every page |
| `src/components/` | `Statement`, `Try`, `Board` and `Teleport`, used inside lecture notes |
| `src/scripts/` | The simulators (Bloch sphere, two-qubit register) and home-page animation |
| `src/styles/site.css` | All styles |
| `public/assets/img/` | Images, copied to the site as they are |

## Adding a lecture

1. Create `src/content/lectures/<slug>.mdx`, using the `slug` already listed for that lecture in `src/data/lectures.ts` (for example `03-grover.mdx`). Copy the block between the `---` lines from an existing lecture and edit it.
2. Write the notes in Markdown. Each `## Heading` becomes a numbered section and an entry in the table of contents.
3. The home-page card and the "Next" link of the previous lecture pick the new page up on their own.
