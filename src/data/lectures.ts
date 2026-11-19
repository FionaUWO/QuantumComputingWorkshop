// The eight lectures, in order. A lecture gets a page when a file named
// `<slug>.mdx` exists in src/content/lectures/; until then it shows as "In preparation".
export interface LectureInfo {
  num: number;
  slug: string;
  part: string;
  title: string; // may contain inline HTML such as <sub>
  blurb: string;
  art: string;
}

export const lectures: LectureInfo[] = [
  { num: 1, slug: '01-qubit', part: 'Foundations', title: 'A qubit is a unit vector in ℂ²', blurb: 'States, the Born rule, the Bloch sphere, single-qubit gates.', art: 'bloch' },
  { num: 2, slug: '02-entanglement', part: 'Foundations', title: 'Multiple qubits and entanglement', blurb: 'Tensor products, Bell states, no-cloning, teleportation.', art: 'entangle' },
  { num: 3, slug: '03-grover', part: 'Algorithms', title: 'Query algorithms and Grover search', blurb: 'Oracles, phase kickback, search as a rotation in a plane.', art: 'grover' },
  { num: 4, slug: '04-shor', part: 'Algorithms', title: 'The quantum Fourier transform and Shor', blurb: 'Fourier analysis on ℤ<sub>N</sub>, phase estimation, order finding.', art: 'qft' },
  { num: 5, slug: '05-hamiltonians', part: 'Variational methods', title: 'Hamiltonians and optimisation', blurb: 'Observables, the variational principle, MaxCut as an Ising model.', art: 'maxcut' },
  { num: 6, slug: '06-qaoa', part: 'Variational methods', title: 'QAOA', blurb: 'Cost and mixer layers, adiabatic evolution, what limits it.', art: 'qaoa' },
  { num: 7, slug: '07-noise', part: 'Error correction', title: 'Noise and the first codes', blurb: "Pauli errors, the repetition code, syndromes, Shor's nine-qubit code.", art: 'repetition' },
  { num: 8, slug: '08-stabilizer', part: 'Error correction', title: 'Stabilizer codes and the surface code', blurb: 'Abelian subgroups of the Pauli group, CSS codes, thresholds.', art: 'surface' },
];
