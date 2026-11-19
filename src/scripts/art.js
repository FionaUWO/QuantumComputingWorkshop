/* Small topic illustrations, one per lecture. Any element with data-art="name"
   gets the matching SVG injected, so the drawings live in one place. */
(function () {
  'use strict';
  const T = '#b9a3dc', TL = '#ddd3ee', D = '#24123f', W = '#4f2683', M = '#4f2683', P = '#807f83', G = '#c9c6d1';
  const svg = (body) => '<svg viewBox="0 0 240 140" xmlns="http://www.w3.org/2000/svg" fill="none" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + body + '</svg>';

  const ART = {
    // Bloch sphere with a state vector
    bloch: svg(
      '<circle cx="120" cy="72" r="54" stroke="' + D + '" stroke-width="2"/>' +
      '<ellipse cx="120" cy="72" rx="54" ry="16" stroke="' + T + '" stroke-width="2" stroke-dasharray="4 5"/>' +
      '<path d="M120 18v108" stroke="' + G + '" stroke-width="1.5"/>' +
      '<path d="M120 72l34-38" stroke="' + W + '" stroke-width="4"/><circle cx="154" cy="34" r="6" fill="' + W + '"/>'),
    // Bell-state circuit: H then CNOT
    entangle: svg(
      '<path d="M24 48h192M24 98h192" stroke="' + D + '" stroke-width="2"/>' +
      '<rect x="62" y="30" width="36" height="36" rx="5" fill="' + T + '"/>' +
      '<path d="M72 39v18M88 39v18M72 48h16" stroke="#fff" stroke-width="3"/>' +
      '<path d="M150 48v62" stroke="' + D + '" stroke-width="2"/><circle cx="150" cy="48" r="6" fill="' + D + '"/>' +
      '<circle cx="150" cy="98" r="12" stroke="' + D + '" stroke-width="2"/><path d="M138 98h24" stroke="' + D + '" stroke-width="2"/>' +
      '<path d="M190 48q14 25 0 50" stroke="' + W + '" stroke-width="3" stroke-dasharray="2 6"/>'),
    // Grover: one amplitude grows
    grover: svg(
      '<path d="M22 112h196" stroke="' + D + '" stroke-width="2"/>' +
      [40, 66, 92, 144, 170, 196].map((x) => '<rect x="' + x + '" y="92" width="16" height="20" rx="2" fill="' + TL + '"/>').join('') +
      '<rect x="118" y="24" width="16" height="88" rx="2" fill="' + W + '"/>' +
      '<path d="M30 78h180" stroke="' + G + '" stroke-width="1.5" stroke-dasharray="4 5"/>'),
    // Roots of unity for the Fourier transform
    qft: svg(
      '<circle cx="120" cy="70" r="50" stroke="' + D + '" stroke-width="2"/>' +
      '<path d="M58 70h124M120 8v124" stroke="' + G + '" stroke-width="1.5"/>' +
      [0, 1, 2, 3, 4, 5, 6, 7].map((k) => {
        const a = (k * Math.PI) / 4, x = 120 + 50 * Math.cos(a), y = 70 - 50 * Math.sin(a);
        return '<circle cx="' + x.toFixed(1) + '" cy="' + y.toFixed(1) + '" r="6" fill="' + (k === 1 ? W : T) + '"/>';
      }).join('') +
      '<path d="M120 70l35.4-35.4" stroke="' + W + '" stroke-width="3"/>'),
    // MaxCut: a graph split into two colours
    maxcut: svg(
      '<path d="M60 40l60-16M60 40l10 62M120 24l58 30M70 102l80 12M178 54l-28 60M60 40l90 74" stroke="' + W + '" stroke-width="2.5"/>' +
      '<path d="M120 24l-50 78M178 54l-108 48" stroke="' + G + '" stroke-width="2"/>' +
      '<circle cx="60" cy="40" r="11" fill="' + T + '"/><circle cx="150" cy="114" r="11" fill="' + T + '"/>' +
      '<circle cx="120" cy="24" r="11" fill="' + P + '"/><circle cx="70" cy="102" r="11" fill="' + P + '"/><circle cx="178" cy="54" r="11" fill="' + P + '"/>'),
    // QAOA: an optimiser walking down a landscape
    qaoa: svg(
      '<ellipse cx="132" cy="72" rx="92" ry="54" stroke="' + G + '" stroke-width="1.5"/>' +
      '<ellipse cx="138" cy="74" rx="66" ry="38" stroke="' + TL + '" stroke-width="2"/>' +
      '<ellipse cx="144" cy="76" rx="40" ry="23" stroke="' + T + '" stroke-width="2"/>' +
      '<ellipse cx="150" cy="78" rx="16" ry="9" fill="' + T + '"/>' +
      '<path d="M40 34l34 14 22 22 30-4 24 12" stroke="' + W + '" stroke-width="3"/>' +
      '<circle cx="40" cy="34" r="5" fill="' + W + '"/><circle cx="150" cy="78" r="5" fill="#fff" stroke="' + W + '" stroke-width="3"/>'),
    // Repetition code: three qubits, one flipped, two parity checks
    repetition: svg(
      '<path d="M50 60h140" stroke="' + D + '" stroke-width="2"/>' +
      '<circle cx="50" cy="60" r="16" fill="' + T + '"/><circle cx="120" cy="60" r="16" fill="' + W + '"/><circle cx="190" cy="60" r="16" fill="' + T + '"/>' +
      '<path d="M50 76l35 30M120 76l-35 30M120 76l35 30M190 76l-35 30" stroke="' + G + '" stroke-width="1.5"/>' +
      '<rect x="72" y="100" width="26" height="26" rx="4" fill="' + P + '"/><rect x="142" y="100" width="26" height="26" rx="4" fill="' + P + '"/>' +
      '<path d="M112 52l16 16M128 52l-16 16" stroke="#fff" stroke-width="3"/>'),
    // Surface code: checkerboard of stabilizers with data qubits on the corners
    surface: svg(
      (function () {
        let s = '';
        for (let r = 0; r < 3; r++) for (let c = 0; c < 5; c++) {
          s += '<rect x="' + (45 + c * 30) + '" y="' + (25 + r * 30) + '" width="30" height="30" fill="' + ((r + c) % 2 ? TL : '#fff') + '" stroke="' + D + '" stroke-width="1.5"/>';
        }
        for (let r = 0; r < 4; r++) for (let c = 0; c < 6; c++) {
          const hit = r === 1 && c === 3;
          s += '<circle cx="' + (45 + c * 30) + '" cy="' + (25 + r * 30) + '" r="5" fill="' + (hit ? W : D) + '"/>';
        }
        return s;
      })()),
  };

  document.querySelectorAll('[data-art]').forEach((el) => {
    if (ART[el.dataset.art]) el.innerHTML = ART[el.dataset.art];
  });
  window.WorkshopArt = ART;
})();
