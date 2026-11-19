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
    lede: 'Flip a coin twice and the result is still random. Apply the Hadamard gate to a qubit twice and the result is certain. This lecture explains why, and on the way sets up the three components of the theory: states as unit vectors in ℂ², measurement governed by the Born rule, and gates as unitary operators.',
    board: 'bloch', boardLabel: 'Interactive Bloch sphere' },
  { num: 2, slug: '02-entanglement', part: 'Foundations', title: 'Multiple qubits and entanglement', blurb: 'Tensor products, Bell states, no-cloning, teleportation.', art: 'entangle',
    heading: 'Two qubits live in ℂ² ⊗ ℂ²',
    lede: 'This lecture extends the formalism to composite systems through the tensor product. It distinguishes product states from entangled states and examines the consequences of entanglement, including the no-cloning theorem, quantum teleportation and superdense coding.',
    board: 'pair', boardLabel: 'Interactive two-qubit simulator' },
  { num: 3, slug: '03-grover', part: 'Algorithms', title: 'Query algorithms and Grover search', blurb: 'Oracles, phase kickback, search as a rotation in a plane.', art: 'grover', draft: true,
    heading: 'Search is a rotation in a plane',
    lede: 'This lecture introduces the query model of computation, in which cost is measured by the number of calls to a black-box function. It presents the Deutsch–Jozsa algorithm, where a single quantum query replaces exponentially many classical ones, and Grover\'s algorithm, which finds a marked item among N in on the order of √N queries.',
    board: 'pair', boardLabel: 'Interactive two-qubit simulator' },
  { num: 4, slug: '04-shor', part: 'Algorithms', title: 'The quantum Fourier transform and Shor', blurb: 'Fourier analysis on ℤ<sub>N</sub>, phase estimation, order finding.', art: 'qft', draft: true,
    heading: 'Fourier analysis finds periods, and periods factor integers',
    lede: 'This lecture studies the quantum Fourier transform on a cyclic group, which maps a hidden period to a sharply peaked distribution. It develops phase estimation as a general subroutine and applies it to order finding, the core of Shor\'s polynomial-time algorithm for integer factorisation.' },
  { num: 5, slug: '05-hamiltonians', part: 'Variational methods', title: 'Hamiltonians and optimisation', blurb: 'Observables, the variational principle, MaxCut as an Ising model.', art: 'maxcut', draft: true,
    heading: 'Optimisation problems are eigenvalue problems',
    lede: 'This lecture introduces Hamiltonians as Hermitian operators that generate time evolution and assign energies to states. It formulates MaxCut as the problem of finding an extreme eigenvalue of a diagonal Hamiltonian and presents the variational principle as a method for approximating it.' },
  { num: 6, slug: '06-qaoa', part: 'Variational methods', title: 'QAOA', blurb: 'Cost and mixer layers, adiabatic evolution, what limits it.', art: 'qaoa', draft: true,
    heading: 'QAOA alternates a cost layer with a mixing layer',
    lede: 'This lecture presents the Quantum Approximate Optimization Algorithm, which prepares a state with a shallow, problem-dependent circuit whose parameters are optimised classically. It constructs the circuit, analyses the depth-one case analytically, and discusses the limitations of the method.' },
  { num: 7, slug: '07-noise', part: 'Error correction', title: 'Noise and the first codes', blurb: "Pauli errors, the repetition code, syndromes, Shor's nine-qubit code.", art: 'repetition', draft: true,
    heading: 'Quantum information can be protected without being read',
    lede: 'This lecture addresses three apparent obstacles to quantum error correction: quantum states cannot be copied, measurement destroys superpositions, and errors form a continuum. It shows how the three-qubit repetition code overcomes them and how Shor\'s nine-qubit code corrects an arbitrary single-qubit error.' },
  { num: 8, slug: '08-stabilizer', part: 'Error correction', title: 'Stabilizer codes and the surface code', blurb: 'Abelian subgroups of the Pauli group, CSS codes, thresholds.', art: 'surface', draft: true,
    heading: 'A code is an abelian subgroup of the Pauli group',
    lede: 'This lecture develops the stabilizer formalism, in which a code is specified by the operators that fix it. The formalism unifies the codes of Lecture 7, relates quantum codes to classical ones, and leads to the surface code and the threshold theorem.' },
];
