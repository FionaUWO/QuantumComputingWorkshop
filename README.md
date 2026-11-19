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
| `src/content/lectures/<lecture>/*.mdx` | Lecture notes, one file per section, in Markdown with LaTeX between dollar signs |
| `src/data/lectures.ts` | The list of eight lectures: titles, opening text, which simulator each uses |
| `src/pages/` | Home page, playground, and the templates for lecture pages |
| `src/layouts/Base.astro` | Header and footer shared by every page |
| `src/layouts/Course.astro` | Lecture pages: contents menu on the left, one section on the right |
| `src/components/` | `Statement`, `Example`, `Try`, `Board` and `Teleport`, used inside lecture notes |
| `src/scripts/` | The simulators (Bloch sphere, two-qubit register) and home-page animation |
| `src/styles/` | `site.css` for the whole site, `course.css` for the lecture pages |
| `public/assets/img/` | Images, copied to the site as they are |

## Adding a lecture

Each lecture is a folder of section files. Every section becomes its own page, listed in the menu on the left.

1. Create the folder `src/content/lectures/<slug>/`, using the `slug` already listed for that lecture in `src/data/lectures.ts` (for example `03-grover`).
2. Add one file per section, named with a number prefix that sets the order: `01-oracles.mdx`, `02-deutsch-jozsa.mdx`, and so on. Each starts with

   ```
   ---
   title: Oracles
   ---
   ```

   followed by the notes in Markdown. Add `board: false` under the title to hide the simulator on that page. A `### Heading` becomes a subsection in the menu.
3. In `src/data/lectures.ts`, give the lecture a `heading` and `lede` for its opening page, and a `board` if it has a simulator.
4. The home-page card, the menu and the Back and Next buttons pick the new pages up on their own.

The `katex` package must stay on the same version that `rehype-katex` uses (`npm ls katex` shows both); a mismatch leaves subscripts and superscripts unsized.
