// The story is readable without JavaScript. Motion is a progressive enhancement.
(() => {
  const stories = document.querySelector('.support-stories');
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  if (stories && 'IntersectionObserver' in window && !reduceMotion.matches) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15 });
    stories.classList.add('motion-ready');
    stories.querySelectorAll('article').forEach(article => observer.observe(article));
    reduceMotion.addEventListener('change', () => {
      if (reduceMotion.matches) {
        stories.classList.remove('motion-ready');
        observer.disconnect();
      }
    });
  }
  const toggle = document.querySelector('.nav-toggle');
  const menu = document.querySelector('#home-navigation');
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menu?.classList.contains('open')) {
      menu.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.focus();
    }
  });
})();
