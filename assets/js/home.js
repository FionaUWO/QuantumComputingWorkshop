/* Home page behaviour: the live qubit in the hero, reveal-on-scroll,
   counting numbers and the tabs for the four parts of the workshop. */
(function () {
  'use strict';
  const still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---- 1. A qubit wandering over the Bloch sphere ---- */
  const canvas = document.getElementById('hero-qubit');
  if (canvas) {
    const ctx = canvas.getContext('2d');
    const PURPLE = '#4f2683', LILAC = '#b9a3dc', INK = '#24123f';
    let yaw = -0.5, pitch = 0.3, pointer = 0, visible = true;
    const trail = [];

    const project = (p, c, R) => {
      const cy = Math.cos(yaw + pointer), sy = Math.sin(yaw + pointer), cp = Math.cos(pitch), sp = Math.sin(pitch);
      const x1 = p[0] * cy - p[1] * sy, y1 = p[0] * sy + p[1] * cy;
      return [c + R * y1, c - R * (p[2] * cp - x1 * sp), x1 * cp + p[2] * sp];
    };

    const state = (t) => {
      const th = Math.PI / 2 + 0.95 * Math.sin(t * 0.55), ph = t * 1.15;
      return [Math.sin(th) * Math.cos(ph), Math.sin(th) * Math.sin(ph), Math.cos(th)];
    };

    function draw(t) {
      const css = canvas.clientWidth;
      if (!css) return;
      const dpr = window.devicePixelRatio || 1;
      if (canvas.width !== Math.round(css * dpr)) canvas.width = canvas.height = Math.round(css * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, css, css);
      const c = css / 2, R = css * 0.39;
      const P = (p) => project(p, c, R);
      ctx.lineCap = 'round';
      ctx.lineJoin = 'round';

      ctx.fillStyle = '#fff';
      ctx.beginPath(); ctx.arc(c, c, R, 0, 2 * Math.PI); ctx.fill();
      ctx.strokeStyle = PURPLE; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.arc(c, c, R, 0, 2 * Math.PI); ctx.stroke();

      // latitude and longitude lines, dimmer on the far side
      const ring = (f, w) => {
        for (const front of [false, true]) {
          ctx.beginPath();
          ctx.strokeStyle = front ? LILAC : '#e3daf2';
          ctx.lineWidth = w;
          let pen = false;
          for (let i = 0; i <= 96; i++) {
            const q = P(f((i / 96) * 2 * Math.PI));
            if ((q[2] >= 0) === front) { pen ? ctx.lineTo(q[0], q[1]) : ctx.moveTo(q[0], q[1]); pen = true; } else pen = false;
          }
          ctx.stroke();
        }
      };
      for (const z of [-0.6, 0, 0.6]) { const r = Math.sqrt(1 - z * z); ring((a) => [r * Math.cos(a), r * Math.sin(a), z], z ? 1 : 1.8); }
      for (let k = 0; k < 4; k++) { const a0 = (k * Math.PI) / 4; ring((a) => [Math.cos(a0) * Math.cos(a), Math.sin(a0) * Math.cos(a), Math.sin(a)], 1); }

      // poles
      ctx.font = 'italic 600 ' + Math.max(15, css * 0.045) + 'px Fraunces, Georgia, serif';
      ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillStyle = INK;
      const n = P([0, 0, 1.17]), s = P([0, 0, -1.17]);
      ctx.fillText('|0⟩', n[0], n[1]); ctx.fillText('|1⟩', s[0], s[1]);

      // the state and the path it has traced
      const v = state(t);
      trail.push(v);
      if (trail.length > 150) trail.shift();
      for (let i = 1; i < trail.length; i++) {
        const a = P(trail[i - 1]), b = P(trail[i]);
        ctx.globalAlpha = (i / trail.length) * (b[2] >= 0 ? 0.9 : 0.3);
        ctx.strokeStyle = PURPLE; ctx.lineWidth = 3;
        ctx.beginPath(); ctx.moveTo(a[0], a[1]); ctx.lineTo(b[0], b[1]); ctx.stroke();
      }
      ctx.globalAlpha = 1;
      const o = P([0, 0, 0]), tip = P(v);
      ctx.strokeStyle = INK; ctx.lineWidth = 3.5;
      ctx.beginPath(); ctx.moveTo(o[0], o[1]); ctx.lineTo(tip[0], tip[1]); ctx.stroke();
      ctx.fillStyle = PURPLE;
      ctx.beginPath(); ctx.arc(tip[0], tip[1], 9, 0, 2 * Math.PI); ctx.fill();
      ctx.fillStyle = '#fff';
      ctx.beginPath(); ctx.arc(tip[0], tip[1], 3.5, 0, 2 * Math.PI); ctx.fill();
    }

    if (still) {
      for (let i = 0; i < 150; i++) trail.push(state(i * 0.03));
      draw(4.5);
      new ResizeObserver(() => draw(4.5)).observe(canvas);
    } else {
      canvas.addEventListener('pointermove', (e) => {
        const r = canvas.getBoundingClientRect();
        pointer = ((e.clientX - r.left) / r.width - 0.5) * 1.2;
      });
      canvas.addEventListener('pointerleave', () => { pointer = 0; });
      new IntersectionObserver((es) => { visible = es[0].isIntersecting; }).observe(canvas);
      const t0 = performance.now();
      const loop = (now) => {
        if (visible) { const t = (now - t0) / 1000; yaw = -0.5 + t * 0.12; draw(t); }
        requestAnimationFrame(loop);
      };
      requestAnimationFrame(loop);
    }
  }

  /* ---- 2. Reveal sections as they enter ---- */
  const groups = document.querySelectorAll('[data-reveal]');
  groups.forEach((g) => [...g.children].forEach((el, i) => el.style.setProperty('--n', i)));
  // Checked from plain scroll events (not IntersectionObserver), so content can
  // never stay hidden in a throttled or background tab.
  let waiting = [...groups];
  const revealVisible = () => {
    const limit = window.innerHeight * 0.92;
    waiting = waiting.filter((g) => {
      if (still || g.getBoundingClientRect().top < limit) { g.classList.add('in'); return false; }
      return true;
    });
    if (!waiting.length) { removeEventListener('scroll', revealVisible); removeEventListener('resize', revealVisible); }
  };
  addEventListener('scroll', revealVisible, { passive: true });
  addEventListener('resize', revealVisible);
  addEventListener('load', revealVisible);
  revealVisible();

  /* ---- 3. Count the numbers up once ---- */
  document.querySelectorAll('[data-count]').forEach((el) => {
    const target = +el.dataset.count;
    if (still || !target) { el.textContent = target; return; }
    el.textContent = '0';
    new IntersectionObserver((es, io) => {
      if (!es[0].isIntersecting) return;
      io.disconnect();
      const t0 = performance.now(), dur = 1100;
      const tick = (now) => {
        const u = Math.min(1, (now - t0) / dur);
        el.textContent = Math.round(target * (1 - Math.pow(1 - u, 3)));
        if (u < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    }).observe(el);
  });

  /* ---- 4. Tabs for the four parts ---- */
  const tabs = [...document.querySelectorAll('.stepper [role="tab"]')];
  const pick = (tab) => {
    tabs.forEach((t) => {
      const on = t === tab;
      const panel = document.getElementById(t.getAttribute('aria-controls'));
      t.setAttribute('aria-selected', on);
      t.tabIndex = on ? 0 : -1;
      panel.hidden = !on;
      panel.classList.toggle('swap-in', on);
    });
  };
  tabs.forEach((t, i) => {
    t.addEventListener('click', () => pick(t));
    t.addEventListener('keydown', (e) => {
      const d = { ArrowRight: 1, ArrowLeft: -1 }[e.key];
      if (!d) return;
      const next = tabs[(i + d + tabs.length) % tabs.length];
      pick(next);
      next.focus();
    });
  });
})();
