// GoSports Foundation — beta site interactions (vanilla JS, no dependencies)

document.addEventListener('DOMContentLoaded', () => {

  // Mobile nav toggle
  const toggle = document.querySelector('.nav-toggle');
  const links = document.querySelector('.nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', () => {
      const isOpen = links.classList.toggle('open');
      toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });
    links.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
      links.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
    }));
  }

  // Accordion (FAQ / selection process)
  document.querySelectorAll('.accordion-item').forEach(item => {
    const trigger = item.querySelector('.accordion-trigger');
    const panel = item.querySelector('.accordion-panel');
    if (!trigger || !panel) return;
    trigger.addEventListener('click', () => {
      const isOpen = panel.style.maxHeight && panel.style.maxHeight !== '0px';
      // close siblings within same accordion group
      const group = item.closest('[data-accordion-group]');
      if (group) {
        group.querySelectorAll('.accordion-panel').forEach(p => { p.style.maxHeight = '0px'; });
        group.querySelectorAll('.accordion-trigger .plus').forEach(p => { p.textContent = '+'; });
      }
      panel.style.maxHeight = isOpen ? '0px' : panel.scrollHeight + 'px';
      const plus = trigger.querySelector('.plus');
      if (plus) plus.textContent = isOpen ? '+' : '\u2212';
    });
  });

  // Testimonial tabs
  document.querySelectorAll('[data-tabs]').forEach(wrap => {
    const tabs = wrap.querySelectorAll('.t-tab');
    const panes = wrap.querySelectorAll('.t-pane');
    tabs.forEach((tab, i) => {
      tab.addEventListener('click', () => {
        tabs.forEach(t => t.setAttribute('aria-selected', 'false'));
        panes.forEach(p => p.classList.remove('active'));
        tab.setAttribute('aria-selected', 'true');
        panes[i].classList.add('active');
      });
    });
  });

  // Set current year in footer
  document.querySelectorAll('[data-year]').forEach(el => {
    el.textContent = new Date().getFullYear();
  });
});
