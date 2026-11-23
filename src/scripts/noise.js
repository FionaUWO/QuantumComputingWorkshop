/* Pauli errors on the Bloch sphere: shows the state arrow being flipped.
   Usage:  new NoiseSphere(element)
   A bit flip (X) turns the arrow half way round the x-axis, from |0> to |1>.
   A phase flip (Z) turns it half way round the z-axis, from |+> to |->. */
(function () {
  'use strict';

  const PI = Math.PI;
  const ERRORS = {
    bit: {
      label: 'Bit flip (X)',
      start: [0, 0, 1],
      axis: [1, 0, 0],
      text: 'X turns the arrow half way round the x-axis: |0⟩ becomes |1⟩.',
    },
    phase: {
      label: 'Phase flip (Z)',
      start: [1, 0, 0],
      axis: [0, 0, 1],
      text: 'Z turns the arrow half way round the z-axis: |+⟩ becomes |−⟩.',
    },
  };

  // v turned by angle t about the unit axis a (Rodrigues' formula)
  function turned(v, a, t) {
    const c = Math.cos(t), sn = Math.sin(t), d = (a[0] * v[0] + a[1] * v[1] + a[2] * v[2]) * (1 - c);
    return [
      v[0] * c + (a[1] * v[2] - a[2] * v[1]) * sn + a[0] * d,
      v[1] * c + (a[2] * v[0] - a[0] * v[2]) * sn + a[1] * d,
      v[2] * c + (a[0] * v[1] - a[1] * v[0]) * sn + a[2] * d,
    ];
  }

  const reducedMotion = () => window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  class NoiseSphere {
    constructor(root) {
      this.kind = 'bit';
      this.rot = reducedMotion() ? 1 : 0;   // how far the arrow has turned: 0 = start, 1 = flipped
      this.yaw = -0.55;
      this.pitch = 0.32;
      this.anim = 0;
      this.build(root);
      this.bind();
      this.refresh();
    }

    build(root) {
      root.classList.add('bloch', 'noise');
      root.innerHTML =
        '<canvas tabindex="0" role="img" aria-label="Bloch sphere with the state arrow being flipped by an error. Drag or use arrow keys to turn the view."></canvas>' +
        '<p class="hint">Drag the sphere to turn it</p>' +
        '<div class="row channels" role="group" aria-label="Kind of error">' +
        Object.keys(ERRORS).map((k) => '<button type="button" data-kind="' + k + '">' + ERRORS[k].label + '</button>').join('') +
        '</div>' +
        '<div class="trace"><p class="circuit" aria-live="polite"></p><button type="button" class="reset" data-play>Play again</button></div>';
      this.root = root;
      this.canvas = root.querySelector('canvas');
      this.ctx = this.canvas.getContext('2d');
      this.el = {
        kinds: Array.from(root.querySelectorAll('[data-kind]')),
        text: root.querySelector('.circuit'),
        play: root.querySelector('[data-play]'),
      };
    }

    bind() {
      this.el.kinds.forEach((b) => b.addEventListener('click', () => { this.kind = b.dataset.kind; this.play(); }));
      this.el.play.addEventListener('click', () => this.play());

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
      new ResizeObserver(() => this.draw()).observe(this.canvas);

      // Play once, the first time the sphere scrolls into view.
      const seen = new IntersectionObserver((entries) => {
        if (entries.some((en) => en.isIntersecting)) { seen.disconnect(); this.play(); }
      }, { threshold: 0.6 });
      seen.observe(this.canvas);
    }

    turn(dyaw, dpitch) {
      this.yaw += dyaw;
      this.pitch = Math.max(-1.45, Math.min(1.45, this.pitch + dpitch));
      this.draw();
    }

    /* Show the arrow at its starting state for a moment, then flip it. */
    play() {
      cancelAnimationFrame(this.anim);
      // Animation frames do not fire in a hidden tab, so skip straight to the result there.
      if (reducedMotion() || document.hidden) { this.rot = 1; this.refresh(); return; }
      const t0 = performance.now(), wait = 600, dur = 1500;
      const frame = (now) => {
        const u = Math.max(0, Math.min(1, (now - t0 - wait) / dur));
        this.rot = u * u * (3 - 2 * u);
        this.draw();
        this.anim = u < 1 ? requestAnimationFrame(frame) : 0;
      };
      this.rot = 0;
      this.refresh();
      this.anim = requestAnimationFrame(frame);
    }

    refresh() {
      this.el.kinds.forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.kind === this.kind)));
      this.el.text.textContent = ERRORS[this.kind].text;
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
      const err = ERRORS[this.kind];
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

      // the axis the arrow turns about
      const a0 = P(err.axis.map((c) => -c)), a1 = P(err.axis);
      ctx.strokeStyle = '#b9a3dc';
      ctx.lineWidth = 2.5;
      ctx.beginPath(); ctx.moveTo(a0[0], a0[1]); ctx.lineTo(a1[0], a1[1]); ctx.stroke();

      const arrow = (v, color, width) => {
        const q = P(v), dx = q[0] - o[0], dy = q[1] - o[1], len = Math.hypot(dx, dy);
        ctx.strokeStyle = color;
        ctx.fillStyle = color;
        ctx.lineWidth = width;
        if (len < 14) { ctx.beginPath(); ctx.arc(q[0], q[1], width + 2, 0, 2 * PI); ctx.fill(); return; }
        const ux = dx / len, uy = dy / len, h = 14, w = 6;
        ctx.beginPath(); ctx.moveTo(o[0], o[1]); ctx.lineTo(q[0] - ux * h * 0.8, q[1] - uy * h * 0.8); ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(q[0], q[1]);
        ctx.lineTo(q[0] - ux * h - uy * w, q[1] - uy * h + ux * w);
        ctx.lineTo(q[0] - ux * h + uy * w, q[1] - uy * h - ux * w);
        ctx.closePath(); ctx.fill();
      };

      if (this.rot > 0) {
        // where the arrow started, and the path it has swept
        arrow(err.start, chalk(0.3), 2);
        ctx.setLineDash([2, 5]);
        ctx.strokeStyle = '#b9a3dc';
        ctx.lineWidth = 2;
        ctx.beginPath();
        for (let i = 0; i <= 48; i++) {
          const q = P(turned(err.start, err.axis, (i / 48) * this.rot * PI));
          i ? ctx.lineTo(q[0], q[1]) : ctx.moveTo(q[0], q[1]);
        }
        ctx.stroke();
        ctx.setLineDash([]);
      }
      arrow(turned(err.start, err.axis, this.rot * PI), '#ffffff', 3);
    }
  }

  window.NoiseSphere = NoiseSphere;
})();
