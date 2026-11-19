// The eight lectures, in order. A lecture goes live when the folder
// src/content/lectures/<slug>/ holds at least one section file; until then it shows as "In preparation".
export interface LectureInfo {
  num: number;
  slug: string;
  part: string;
  title: string; // may contain inline HTML such as <sub>
  blurb: string;
  art: string;
  // Needed once the lecture has pages:
  heading?: string; // headline of the lecture's opening page
  lede?: string;
  board?: 'bloch' | 'pair'; // simulator shown beside the notes
  boardLabel?: string;
  draft?: boolean; // true shows a "first draft" notice on the lecture's pages
}

export const lectures: LectureInfo[] = [
  { num: 1, slug: '01-qubit', part: 'Foundations', title: 'A qubit is a unit vector in ℂ²', blurb: 'States, the Born rule, the Bloch sphere, single-qubit gates.', art: 'bloch',
    heading: 'A qubit is a unit vector in ℂ²',
    lede: 'Everything in this workshop is linear algebra over the complex numbers. Today we set up the three ingredients for a single qubit: states, measurements and gates.',
    board: 'bloch', boardLabel: 'Interactive Bloch sphere' },
  { num: 2, slug: '02-entanglement', part: 'Foundations', title: 'Multiple qubits and entanglement', blurb: 'Tensor products, Bell states, no-cloning, teleportation.', art: 'entangle',
    heading: 'Two qubits live in ℂ² ⊗ ℂ²',
    lede: 'Most vectors in a tensor product are not products. Those that are not are called entangled, and they are what makes a quantum computer more than a collection of independent qubits.',
    board: 'pair', boardLabel: 'Interactive two-qubit simulator' },
  { num: 3, slug: '03-grover', part: 'Algorithms', title: 'Query algorithms and Grover search', blurb: 'Oracles, phase kickback, search as a rotation in a plane.', art: 'grover', draft: true,
    heading: 'Search is a rotation in a plane',
    lede: 'With superposition, entanglement and interference in hand we can compute. We count calls to a black-box function, see one query do the work of exponentially many, and then find a marked item among N in about √N steps.',
    board: 'pair', boardLabel: 'Interactive two-qubit simulator' },
  { num: 4, slug: '04-shor', part: 'Algorithms', title: 'The quantum Fourier transform and Shor', blurb: 'Fourier analysis on ℤ<sub>N</sub>, phase estimation, order finding.', art: 'qft', draft: true,
    heading: 'Fourier analysis finds periods, and periods factor integers',
    lede: 'The quantum Fourier transform on a cyclic group turns a hidden period into a sharp peak. Phase estimation packages that as a tool, and Shor used it to factor integers in polynomial time.' },
  { num: 5, slug: '05-hamiltonians', part: 'Variational methods', title: 'Hamiltonians and optimisation', blurb: 'Observables, the variational principle, MaxCut as an Ising model.', art: 'maxcut', draft: true,
    heading: 'Optimisation problems are eigenvalue problems',
    lede: 'A Hamiltonian is a Hermitian matrix that generates time evolution and assigns energies to states. Written the right way, the largest cut of a graph is an extreme eigenvalue of a diagonal Hamiltonian, and the variational principle gives a way to look for it.' },
  { num: 6, slug: '06-qaoa', part: 'Variational methods', title: 'QAOA', blurb: 'Cost and mixer layers, adiabatic evolution, what limits it.', art: 'qaoa', draft: true,
    heading: 'QAOA alternates a cost layer with a mixing layer',
    lede: 'The Quantum Approximate Optimization Algorithm prepares a state with a short circuit shaped by the problem, and tunes a handful of angles classically. We build the circuit, solve depth one by hand, and look honestly at what limits it.' },
  { num: 7, slug: '07-noise', part: 'Error correction', title: 'Noise and the first codes', blurb: "Pauli errors, the repetition code, syndromes, Shor's nine-qubit code.", art: 'repetition', draft: true,
    heading: 'Quantum information can be protected without being read',
    lede: 'Qubits cannot be copied, measuring them destroys superpositions, and their errors form a continuum. Three qubits are enough to see why none of this prevents error correction, and nine are enough to correct any single-qubit error.' },
  { num: 8, slug: '08-stabilizer', part: 'Error correction', title: 'Stabilizer codes and the surface code', blurb: 'Abelian subgroups of the Pauli group, CSS codes, thresholds.', art: 'surface', draft: true,
    heading: 'A code is an abelian subgroup of the Pauli group',
    lede: 'The stabilizer formalism describes a code by the operators that fix it. It organises every code from lecture 7, connects quantum codes to classical ones, and leads to the surface code and the threshold theorem.' },
];
