/* Multi-qubit simulator and the two widgets for lecture 2.
     new TwoQubit(element)   two qubits A and B: gates, CNOT, partial measurement
     new Teleport(element)   three qubits, stepped through the teleportation protocol
   Qubit 0 is the leftmost symbol in a ket, so on two qubits |ab> has index 2a + b. */
(function () {
  'use strict';

  const R2 = Math.SQRT1_2;
  const GATE = {
    H: [[[R2, 0], [R2, 0]], [[R2, 0], [-R2, 0]]],
    X: [[[0, 0], [1, 0]], [[1, 0], [0, 0]]],
    Z: [[[1, 0], [0, 0]], [[0, 0], [-1, 0]]],
  };

  /* ---------- state-vector register ---------- */
  class Register {
    constructor(n) {
      this.n = n;
      this.size = 1 << n;
      this.re = new Float64Array(this.size);
      this.im = new Float64Array(this.size);
      this.re[0] = 1;
    }
    mask(q) { return 1 << (this.n - 1 - q); }
    set(amps) { amps.forEach((a, i) => { this.re[i] = a[0]; this.im[i] = a[1]; }); }
    prob(i) { return this.re[i] * this.re[i] + this.im[i] * this.im[i]; }

    gate(q, m) {
      const k = this.mask(q), { re, im } = this;
      for (let i = 0; i < this.size; i++) {
        if (i & k) continue;
        const j = i | k, ar = re[i], ai = im[i], br = re[j], bi = im[j];
        re[i] = m[0][0][0] * ar - m[0][0][1] * ai + m[0][1][0] * br - m[0][1][1] * bi;
        im[i] = m[0][0][0] * ai + m[0][0][1] * ar + m[0][1][0] * bi + m[0][1][1] * br;
        re[j] = m[1][0][0] * ar - m[1][0][1] * ai + m[1][1][0] * br - m[1][1][1] * bi;
        im[j] = m[1][0][0] * ai + m[1][0][1] * ar + m[1][1][0] * bi + m[1][1][1] * br;
      }
    }

    cnot(control, target) {
      const c = this.mask(control), t = this.mask(target), { re, im } = this;
      for (let i = 0; i < this.size; i++) {
        if (!(i & c) || (i & t)) continue;
        const j = i | t;
        [re[i], re[j]] = [re[j], re[i]];
        [im[i], im[j]] = [im[j], im[i]];
      }
    }

    /* Measure one qubit: returns 0 or 1 and collapses the state. */
    measure(q) {
      const k = this.mask(q);
      let p1 = 0;
      for (let i = 0; i < this.size; i++) if (i & k) p1 += this.prob(i);
      const out = Math.random() < p1 ? 1 : 0;
      const norm = Math.sqrt(out ? p1 : 1 - p1);
      for (let i = 0; i < this.size; i++) {
        if (!!(i & k) === !!out) { this.re[i] /= norm; this.im[i] /= norm; }
        else { this.re[i] = 0; this.im[i] = 0; }
      }
      return out;
    }

    /* Outcome of measuring every qubit, without disturbing this register. */
    sample() {
      let r = Math.random();
      for (let i = 0; i < this.size; i++) { r -= this.prob(i); if (r < 0) return i; }
      return this.size - 1;
    }
  }

  /* ---------- formatting ---------- */
  const num = (x) => String(+x.toFixed(3)).replace('-', '−');
  function fmt(re, im) {
    if (Math.abs(re) < 5e-4) re = 0;
    if (Math.abs(im) < 5e-4) im = 0;
    if (!im) return num(re);
    if (!re) return num(im) + 'i';
    return num(re) + (im < 0 ? ' − ' : ' + ') + num(Math.abs(im)) + 'i';
  }
  const ket = (i, n) => '|' + i.toString(2).padStart(n, '0') + '⟩';

  function ampRows(reg, labels) {
    let html = '';
    for (let i = 0; i < reg.size; i++) {
      const p = reg.prob(i);
      html += '<span class="k">' + (labels ? labels(i) : ket(i, reg.n)) + '</span>' +
        '<div class="bar"><i style="width:' + (p * 100).toFixed(1) + '%"></i></div>' +
        '<span class="num">' + fmt(reg.re[i], reg.im[i]) + '</span>';
    }
    return html;
  }

  /* ---------- widget 1: two qubits ---------- */
  class TwoQubit {
    constructor(root) {
      this.root = root;
      root.classList.add('multi');
      root.innerHTML =
        '<p class="title">Two qubits, A and B</p>' +
        '<div class="amps" aria-live="polite"></div>' +
        '<p class="verdict" aria-live="polite"></p>' +
        '<div class="row"><span class="lab">A</span>' + this.btns('A') + '</div>' +
        '<div class="row"><span class="lab">B</span>' + this.btns('B') + '</div>' +
        '<div class="row">' +
        '<button type="button" data-do="CAB">CNOT, A controls B</button>' +
        '<button type="button" data-do="CBA">CNOT, B controls A</button></div>' +
        '<div class="row">' +
        '<button type="button" class="measure" data-do="MA">Measure A</button>' +
        '<button type="button" class="measure" data-do="MB">Measure B</button>' +
        '<button type="button" class="measure" data-do="sample">Measure both, 100 copies</button>' +
        '<button type="button" data-do="reset">Reset to |00⟩</button></div>' +
        '<p class="circuit"></p>' +
        '<p class="result" aria-live="polite"></p>';
      this.el = {
        amps: root.querySelector('.amps'),
        verdict: root.querySelector('.verdict'),
        circuit: root.querySelector('.circuit'),
        result: root.querySelector('.result'),
      };
      root.addEventListener('click', (e) => {
        const b = e.target.closest('button[data-do]');
        if (b) this.run([b.dataset.do]);
      });
      this.reset();
    }

    btns(q) {
      return ['H', 'X', 'Z'].map((g) => '<button type="button" data-do="' + g + q + '" aria-label="Apply ' + g + ' to qubit ' + q + '">' + g + '</button>').join('');
    }

    reset() {
      this.reg = new Register(2);
      this.history = ['|00⟩'];
      this.el.result.textContent = '';
      this.render();
    }

    /* Steps: HA XA ZA HB XB ZB, CAB, CBA, MA, MB, sample, reset. */
    run(steps) {
      steps.forEach((s) => {
        if (s === 'reset') return this.reset();
        if (s === 'sample') return this.sample();
        this.el.result.textContent = '';
        if (s === 'CAB') { this.reg.cnot(0, 1); this.history.push('CNOT(A→B)'); }
        else if (s === 'CBA') { this.reg.cnot(1, 0); this.history.push('CNOT(B→A)'); }
        else if (s[0] === 'M') {
          const q = s[1] === 'A' ? 0 : 1, out = this.reg.measure(q);
          this.history.push('measure ' + s[1] + ' = ' + out);
          this.el.result.textContent = 'Qubit ' + s[1] + ' gave ' + out + '. The amplitudes that disagree with it are gone and the rest are rescaled.';
        } else if (GATE[s[0]]) {
          this.reg.gate(s[1] === 'A' ? 0 : 1, GATE[s[0]]);
          this.history.push(s[0] + '(' + s[1] + ')');
        }
        this.render();
      });
    }

    sample() {
      const c = [0, 0, 0, 0];
      for (let i = 0; i < 100; i++) c[this.reg.sample()]++;
      this.el.result.textContent = '100 fresh copies, both qubits measured. 00: ' + c[0] + ', 01: ' + c[1] + ', 10: ' + c[2] + ', 11: ' + c[3] +
        '. The two bits agreed ' + (c[0] + c[3]) + ' times.';
    }

    render() {
      const { re, im } = this.reg;
      this.el.amps.innerHTML = ampRows(this.reg);
      // |psi> is a product state exactly when a00*a11 - a01*a10 = 0
      const dr = re[0] * re[3] - im[0] * im[3] - (re[1] * re[2] - im[1] * im[2]);
      const di = re[0] * im[3] + im[0] * re[3] - (re[1] * im[2] + im[1] * re[2]);
      const det = Math.hypot(dr, di);
      const entangled = det > 1e-9;
      this.el.verdict.innerHTML = '<b>' + (entangled ? 'Entangled' : 'Product state') + '</b> |a₀₀a₁₁ − a₀₁a₁₀| = ' + num(det);
      this.el.verdict.classList.toggle('on', entangled);
      this.el.circuit.textContent = 'Circuit: ' + this.history.join(' – ');
    }
  }

  /* ---------- widget 2: teleportation, step by step ---------- */
  const STEPS = [
    { label: 'Share a Bell pair', text: 'Alice holds the message qubit M in the state shown. She and Bob have not shared anything yet.' },
    { label: 'Alice entangles M with her half', text: 'H on A, then CNOT from A to B. Alice and Bob now share the Bell state. Bob can walk away with B.' },
    { label: 'Alice measures M and A', text: 'CNOT from M to A, then H on M. No information has moved, but the eight amplitudes are now four copies of the message, each scrambled a different way.' },
    { label: 'Bob corrects', text: '' },
    { label: 'Start again with a new message', text: '' },
  ];

  class Teleport {
    constructor(root) {
      this.root = root;
      root.classList.add('multi');
      root.innerHTML =
        '<p class="title">Teleportation: qubits M (message), A (Alice), B (Bob)</p>' +
        '<p class="msg"></p>' +
        '<div class="amps" aria-live="polite"></div>' +
        '<p class="result" aria-live="polite"></p>' +
        '<div class="row"><button type="button" class="measure" data-next></button></div>';
      this.el = {
        msg: root.querySelector('.msg'),
        amps: root.querySelector('.amps'),
        result: root.querySelector('.result'),
        next: root.querySelector('[data-next]'),
      };
      this.el.next.addEventListener('click', () => this.advance());
      this.start();
    }

    start() {
      const th = 0.4 + Math.random() * 2.3, ph = Math.random() * 2 * Math.PI;
      this.a = [Math.cos(th / 2), 0];
      this.b = [Math.sin(th / 2) * Math.cos(ph), Math.sin(th / 2) * Math.sin(ph)];
      this.reg = new Register(3);
      this.reg.set([this.a, [0, 0], [0, 0], [0, 0], this.b, [0, 0], [0, 0], [0, 0]]);
      this.step = 0;
      this.render();
    }

    advance() {
      const r = this.reg;
      if (this.step === 0) { r.gate(1, GATE.H); r.cnot(1, 2); }
      else if (this.step === 1) { r.cnot(0, 1); r.gate(0, GATE.H); }
      else if (this.step === 2) { this.m = r.measure(0); this.a1 = r.measure(1); }
      else if (this.step === 3) { if (this.a1) r.gate(2, GATE.X); if (this.m) r.gate(2, GATE.Z); }
      else return this.start();
      this.step++;
      this.render();
    }

    bob() {
      const base = (this.m << 2) | (this.a1 << 1);
      return fmt(this.reg.re[base], this.reg.im[base]) + ' |0⟩ + (' + fmt(this.reg.re[base + 1], this.reg.im[base + 1]) + ') |1⟩';
    }

    render() {
      const message = fmt(this.a[0], this.a[1]) + ' |0⟩ + (' + fmt(this.b[0], this.b[1]) + ') |1⟩';
      this.el.msg.textContent = 'Message |ψ⟩ = ' + message;
      this.el.amps.innerHTML = ampRows(this.reg);
      let text = STEPS[this.step].text;
      if (this.step === 3) {
        const fix = (this.a1 ? 'X' : '') + (this.m ? (this.a1 ? ', then Z' : 'Z') : '') || 'nothing';
        text = 'Alice got M = ' + this.m + ' and A = ' + this.a1 + ' and phones Bob with those two bits. His qubit is now ' + this.bob() +
          '. To repair it he must apply ' + fix + '.';
      }
      if (this.step === 4) text = 'Bob’s qubit is ' + this.bob() + ', exactly the message. Alice’s copy was destroyed by her measurement, so nothing was cloned.';
      this.el.result.textContent = text;
      this.el.next.textContent = STEPS[this.step].label;
    }
  }

  window.Register = Register;
  window.TwoQubit = TwoQubit;
  window.Teleport = Teleport;
})();
