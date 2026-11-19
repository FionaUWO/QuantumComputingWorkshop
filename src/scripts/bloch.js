/* Bloch sphere widget — reusable on lecture pages and in the playground.
   Usage:  const sphere = new BlochSphere(element, { sliders: false });
           sphere.run(['reset', 'H', 'sample']);
   A state is [[Re a, Im a], [Re b, Im b]] for a|0> + b|1>. */
(function () {
  'use strict';

  const R2 = Math.SQRT1_2;
  const PI = Math.PI;

  const GATES = {
    X: { m: [[[0, 0], [1, 0]], [[1, 0], [0, 0]]], axis: [1, 0, 0], angle: PI },
    Y: { m: [[[0, 0], [0, -1]], [[0, 1], [0, 0]]], axis: [0, 1, 0], angle: PI },
    Z: { m: [[[1, 0], [0, 0]], [[0, 0], [-1, 0]]], axis: [0, 0, 1], angle: PI },
    H: { m: [[[R2, 0], [R2, 0]], [[R2, 0], [-R2, 0]]], axis: [R2, 0, R2], angle: PI },
    S: { m: [[[1, 0], [0, 0]], [[0, 0], [0, 1]]], axis: [0, 0, 1], angle: PI / 2 },
    T: { m: [[[1, 0], [0, 0]], [[0, 0], [R2, R2]]], axis: [0, 0, 1], angle: PI / 4 },
  };

  const KET0 = () => [[1, 0], [0, 0]];
  const KET1 = () => [[0, 0], [1, 0]];

  // ---- complex 2x2 linear algebra ----
  const cmul = (a, b) => [a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]];
  const cadd = (a, b) => [a[0] + b[0], a[1] + b[1]];
  const abs2 = (a) => a[0] * a[0] + a[1] * a[1];
  const apply = (m, s) => [
    cadd(cmul(m[0][0], s[0]), cmul(m[0][1], s[1])),
    cadd(cmul(m[1][0], s[0]), cmul(m[1][1], s[1])),
  ];

  // exp(-i t/2 n.sigma): rotation of the sphere by angle t about unit axis n
  function rotation(n, t) {
    const c = Math.cos(t / 2), s = Math.sin(t / 2);
    return [
      [[c, -s * n[2]], [-s * n[1], -s * n[0]]],
      [[s * n[1], -s * n[0]], [c, s * n[2]]],
    ];
  }

  function blochVector(s) {
    const [a, b] = s;
    return [
      2 * (a[0] * b[0] + a[1] * b[1]),
      2 * (a[0] * b[1] - a[1] * b[0]),
      abs2(a) - abs2(b),
    ];
  }

  // Fix the global phase so the first non-zero amplitude is real and positive.
  function canonical(s) {
    const ref = abs2(s[0]) > 1e-12 ? s[0] : s[1];
    const r = Math.sqrt(abs2(ref));
    const ph = [ref[0] / r, -ref[1] / r];
    return [cmul(s[0], ph), cmul(s[1], ph)];
  }

  const num = (x) => String(+x.toFixed(3)).replace('-', '−');
  function fmt(c) {
    const re = Math.abs(c[0]) < 5e-4 ? 0 : c[0];
    const im = Math.abs(c[1]) < 5e-4 ? 0 : c[1];
    if (!im) return num(re);
    if (!re) return (Math.abs(Math.abs(im) - 1) < 5e-4 ? (im < 0 ? '−' : '') : num(im)) + 'i';
    return '(' + num(re) + (im < 0 ? ' − ' : ' + ') + num(Math.abs(im)) + 'i)';
  }

  function stateText(s) {
    const [a, b] = canonical(s);
    const parts = [];
    if (abs2(a) > 1e-6) parts.push((Math.abs(a[0] - 1) < 5e-4 ? '' : fmt(a) + ' ') + '|0⟩');
    if (abs2(b) > 1e-6) parts.push((Math.abs(b[0] - 1) < 5e-4 && Math.abs(b[1]) < 5e-4 ? '' : fmt(b) + ' ') + '|1⟩');
    return '|ψ⟩ = ' + parts.join(' + ');
  }

  const reducedMotion = () => window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  class BlochSphere {
    constructor(root, opts) {
      this.opts = Object.assign({ sliders: false }, opts);
      this.state = KET0();
      this.vec = [0, 0, 1];      // what is drawn (differs from state mid-animation)
      this.trail = [];
      this.history = ['|0⟩'];
      this.yaw = -0.55;
      this.pitch = 0.32;
      this.queue = Promise.resolve();
      this.build(root);
      this.bind();
      this.refresh();
    }

    build(root) {
      root.classList.add('bloch');
      root.innerHTML =
        '<canvas tabindex="0" role="img" aria-label="Bloch sphere showing the current qubit state. Drag or use arrow keys to turn the view."></canvas>' +
        '<p class="hint">Drag the sphere to turn it</p>' +
        '<p class="state" aria-live="polite"></p>' +
        '<div class="probs">' +
        '<span>P(0)</span><div class="bar"><i data-bar="0"></i></div><span class="num" data-num="0"></span>' +
        '<span>P(1)</span><div class="bar"><i data-bar="1"></i></div><span class="num" data-num="1"></span>' +
        '</div>' +
        '<div class="row" role="group" aria-label="Apply a gate">' +
        Object.keys(GATES).map((g) => '<button type="button" data-do="' + g + '" aria-label="Apply ' + g + ' gate">' + g + '</button>').join('') +
        '</div>' +
        '<div class="row">' +
        '<button type="button" class="measure" data-do="measure">Measure once</button>' +
        '<button type="button" class="measure" data-do="sample">Measure 100 copies</button>' +
        '<button type="button" data-do="reset">Reset to |0⟩</button>' +
        '</div>' +
        (this.opts.sliders
          ? '<div class="sliders">' +
            '<label for="bl-theta">θ</label><input id="bl-theta" type="range" min="0" max="180" step="1" value="0"><span class="num" data-out="theta"></span>' +
            '<label for="bl-phi">φ</label><input id="bl-phi" type="range" min="0" max="360" step="1" value="0"><span class="num" data-out="phi"></span>' +
            '</div>'
          : '') +
        '<p class="circuit"></p>' +
        '<p class="result" aria-live="polite"></p>';
      this.canvas = root.querySelector('canvas');
      this.ctx = this.canvas.getContext('2d');
      this.el = {
        state: root.querySelector('.state'),
        circuit: root.querySelector('.circuit'),
        result: root.querySelector('.result'),
        bars: [root.querySelector('[data-bar="0"]'), root.querySelector('[data-bar="1"]')],
        nums: [root.querySelector('[data-num="0"]'), root.querySelector('[data-num="1"]')],
        theta: root.querySelector('#bl-theta'),
        phi: root.querySelector('#bl-phi'),
        thetaOut: root.querySelector('[data-out="theta"]'),
        phiOut: root.querySelector('[data-out="phi"]'),
      };
      this.root = root;
    }

    bind() {
      this.root.addEventListener('click', (e) => {
        const b = e.target.closest('button[data-do]');
        if (b) this.run([b.dataset.do]);
      });

      let last = null;
      this.canvas.addEventListener('pointerdown', (e) => { last = [e.clientX, e.clientY]; this.canvas.setPointerCapture(e.pointerId); });
      this.canvas.addEventListener('pointermove', (e) => {
        if (!last) return;
        this.turn((e.clientX - last[0]) * 0.01, (e.clientY - last[1]) * 0.01);
        last = [e.clientX, e.clientY];
      });
      const end = () => { last = null; };
      this.canvas.addEventListener('pointerup', end);
      this.canvas.addEventListener('pointercancel', end);
      this.canvas.addEventListener('keydown', (e) => {
        const k = { ArrowLeft: [-0.1, 0], ArrowRight: [0.1, 0], ArrowUp: [0, -0.1], ArrowDown: [0, 0.1] }[e.key];
        if (k) { e.preventDefault(); this.turn(k[0], k[1]); }
      });

      if (this.el.theta) {
        const onSlide = () => {
          const th = (this.el.theta.value * PI) / 180, ph = (this.el.phi.value * PI) / 180;
          this.state = [[Math.cos(th / 2), 0], [Math.sin(th / 2) * Math.cos(ph), Math.sin(th / 2) * Math.sin(ph)]];
          this.history = ['|ψ(θ, φ)⟩'];
          this.trail = [];
          this.el.result.textContent = '';
          this.refresh(true);
        };
        this.el.theta.addEventListener('input', onSlide);
        this.el.phi.addEventListener('input', onSlide);
      }

      new ResizeObserver(() => this.draw()).observe(this.canvas);
    }

    turn(dyaw, dpitch) {
      this.yaw += dyaw;
      this.pitch = Math.max(-1.45, Math.min(1.45, this.pitch + dpitch));
      this.draw();
    }

    /* Run a list of steps one after another: gate names, 'measure', 'sample', 'reset'. */
    run(steps) {
      steps.forEach((step) => {
        this.queue = this.queue.then(() => {
          if (GATES[step]) return this.gate(step);
          if (step === 'measure') return this.measure();
          if (step === 'sample') return this.sample();
          if (step === 'reset') return this.reset();
        });
      });
      return this.queue;
    }

    gate(name) {
      const g = GATES[name];
      const start = this.state;
      this.el.result.textContent = '';
      this.history.push(name);
      this.trail = [blochVector(start)];
      const finish = () => { this.state = apply(g.m, start); this.refresh(); };
      // Animation frames do not fire in a hidden tab, so skip straight to the result there.
      if (reducedMotion() || document.hidden) { finish(); return Promise.resolve(); }
      const dur = Math.max(320, 650 * (g.angle / PI));
      return new Promise((resolve) => {
        const t0 = performance.now();
        const frame = (now) => {
          const u = Math.min(1, (now - t0) / dur);
          const eased = u * u * (3 - 2 * u);
          this.vec = blochVector(apply(rotation(g.axis, g.angle * eased), start));
          this.trail.push(this.vec);
          this.draw();
          if (u < 1) requestAnimationFrame(frame);
          else { finish(); resolve(); }
        };
        requestAnimationFrame(frame);
      });
    }

    measure() {
      const p0 = abs2(this.state[0]);
      const outcome = Math.random() < p0 ? 0 : 1;
      this.state = outcome ? KET1() : KET0();
      this.history = ['|' + outcome + '⟩'];
      this.trail = [];
      this.refresh();
      this.el.result.textContent = 'Outcome ' + outcome + '. The state collapsed to |' + outcome + '⟩.';
    }

    sample() {
      const p0 = abs2(this.state[0]);
      let zeros = 0;
      for (let i = 0; i < 100; i++) if (Math.random() < p0) zeros++;
      this.el.result.textContent =
        '100 fresh copies of this state, each measured once: outcome 0 came up ' + zeros + ' times, outcome 1 ' + (100 - zeros) + ' times.';
    }

    reset() {
      this.state = KET0();
      this.history = ['|0⟩'];
      this.trail = [];
      this.el.result.textContent = '';
      this.refresh();
    }

    refresh(fromSlider) {
      this.vec = blochVector(this.state);
      const p0 = abs2(this.state[0]), p = [p0, 1 - p0];
      this.el.state.textContent = stateText(this.state);
      p.forEach((v, i) => {
        this.el.bars[i].style.width = (v * 100).toFixed(1) + '%';
        this.el.nums[i].textContent = v.toFixed(3);
      });
      this.el.circuit.textContent = 'Circuit: ' + this.history.join(' – ');
      if (this.el.theta) {
        const th = Math.acos(Math.max(-1, Math.min(1, this.vec[2])));
        let ph = Math.atan2(this.vec[1], this.vec[0]);
        if (ph < -1e-9) ph += 2 * PI;
        if (!fromSlider) {
          this.el.theta.value = Math.round((th * 180) / PI);
          if (Math.sin(th) > 1e-6) this.el.phi.value = Math.round((ph * 180) / PI);
        }
        this.el.thetaOut.textContent = this.el.theta.value + '°';
        this.el.phiOut.textContent = this.el.phi.value + '°';
      }
      this.draw();
    }

    project(p, cx, cy, R) {
      const cyaw = Math.cos(this.yaw), syaw = Math.sin(this.yaw);
      const cp = Math.cos(this.pitch), sp = Math.sin(this.pitch);
      const x1 = p[0] * cyaw - p[1] * syaw;
      const y1 = p[0] * syaw + p[1] * cyaw;
      return [cx + R * y1, cy - R * (p[2] * cp - x1 * sp), x1 * cp + p[2] * sp];
    }

    draw() {
      const css = this.canvas.clientWidth;
      if (!css) return;
      const dpr = window.devicePixelRatio || 1;
      if (this.canvas.width !== Math.round(css * dpr)) {
        this.canvas.width = this.canvas.height = Math.round(css * dpr);
      }
      const ctx = this.ctx;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, css, css);
      const cx = css / 2, cy = css / 2, R = css * 0.36;
      const P = (p) => this.project(p, cx, cy, R);
      const chalk = (a) => 'rgba(255,255,255,' + a + ')';
      ctx.lineCap = 'round';
      ctx.lineJoin = 'round';

      // outline
      ctx.strokeStyle = chalk(0.75);
      ctx.lineWidth = 1.5;
      ctx.beginPath(); ctx.arc(cx, cy, R, 0, 2 * PI); ctx.stroke();

      // great circles: front half solid, back half dashed
      const circle = (f) => {
        for (const front of [false, true]) {
          ctx.beginPath();
          ctx.setLineDash(front ? [] : [3, 5]);
          ctx.strokeStyle = chalk(front ? 0.45 : 0.22);
          ctx.lineWidth = 1;
          let pen = false;
          for (let i = 0; i <= 120; i++) {
            const q = P(f((i / 120) * 2 * PI));
            if ((q[2] >= 0) === front) { pen ? ctx.lineTo(q[0], q[1]) : ctx.moveTo(q[0], q[1]); pen = true; }
            else pen = false;
          }
          ctx.stroke();
        }
        ctx.setLineDash([]);
      };
      circle((t) => [Math.cos(t), Math.sin(t), 0]);
      circle((t) => [Math.cos(t), 0, Math.sin(t)]);
      circle((t) => [0, Math.cos(t), Math.sin(t)]);

      // axes and basis-state labels
      const axes = [
        [[0, 0, 1], '|0⟩'], [[0, 0, -1], '|1⟩'],
        [[1, 0, 0], '|+⟩'], [[-1, 0, 0], '|−⟩'],
        [[0, 1, 0], '|+i⟩'], [[0, -1, 0], '|−i⟩'],
      ];
      ctx.font = 'italic ' + Math.max(13, css * 0.042) + 'px "Cambria Math", Georgia, serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      const o = P([0, 0, 0]);
      for (const [v, label] of axes) {
        const q = P(v), l = P(v.map((c) => c * 1.2));
        ctx.strokeStyle = chalk(q[2] >= 0 ? 0.4 : 0.18);
        ctx.lineWidth = 1;
        ctx.beginPath(); ctx.moveTo(o[0], o[1]); ctx.lineTo(q[0], q[1]); ctx.stroke();
        ctx.fillStyle = chalk(q[2] >= 0 ? 0.95 : 0.5);
        ctx.fillText(label, l[0], l[1]);
      }

      // path traced by the last gate
      if (this.trail.length > 1) {
        ctx.strokeStyle = '#b9a3dc';
        ctx.lineWidth = 2;
        ctx.setLineDash([2, 5]);
        ctx.beginPath();
        this.trail.forEach((v, i) => { const q = P(v); i ? ctx.lineTo(q[0], q[1]) : ctx.moveTo(q[0], q[1]); });
        ctx.stroke();
        ctx.setLineDash([]);
      }

      // state vector
      const tip = P(this.vec);
      const behind = tip[2] < -0.05;
      ctx.globalAlpha = behind ? 0.55 : 1;
      ctx.strokeStyle = '#ffffff';
      ctx.fillStyle = '#ffffff';
      ctx.lineWidth = 3;
      ctx.beginPath(); ctx.moveTo(o[0], o[1]); ctx.lineTo(tip[0], tip[1]); ctx.stroke();
      ctx.beginPath(); ctx.arc(tip[0], tip[1], 6, 0, 2 * PI); ctx.fill();
      ctx.globalAlpha = 1;
    }
  }

  window.BlochSphere = BlochSphere;
})();
