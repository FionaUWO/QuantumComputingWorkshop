/* Starts every simulator on the page and connects the "try it" buttons to the main one.
   Markup:  <div class="board" data-widget="bloch|pair|teleport" [data-sliders] [data-main]>
            <button data-run="reset,H,sample">  */
import './bloch.js';
import './multi.js';

const make = {
  bloch: (el) => new window.BlochSphere(el, { sliders: el.hasAttribute('data-sliders') }),
  pair: (el) => new window.TwoQubit(el),
  teleport: (el) => new window.Teleport(el),
};

document.querySelectorAll('[data-widget]').forEach((el) => {
  if (!el.widget) el.widget = make[el.dataset.widget](el);
});

const main = document.querySelector('[data-widget][data-main]');
if (main) {
  document.querySelectorAll('[data-run]').forEach((b) => {
    b.addEventListener('click', () => {
      // On narrow screens the simulator is not beside the notes, so bring it into view first.
      const r = main.getBoundingClientRect();
      if (r.bottom < 80 || r.top > window.innerHeight - 80) main.scrollIntoView({ block: 'start' });
      main.widget.run(b.dataset.run.split(','));
    });
  });
}
