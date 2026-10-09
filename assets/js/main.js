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

  // Nav dropdowns (About us, Get involved): the chevron button opens the menu
  // for touch and keyboard users; Escape or a click elsewhere closes it.
  const groups = document.querySelectorAll('.nav-group');
  const closeGroups = except => groups.forEach(g => {
    if (g === except) return;
    g.classList.remove('open');
    g.querySelector('.nav-sub-toggle')?.setAttribute('aria-expanded', 'false');
  });
  groups.forEach(g => {
    const btn = g.querySelector('.nav-sub-toggle');
    btn?.addEventListener('click', e => {
      e.stopPropagation();
      const open = g.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      closeGroups(g);
    });
    // tabbing out of an open menu closes it
    g.addEventListener('focusout', e => { if (!g.contains(e.relatedTarget)) closeGroups(); });
  });
  document.addEventListener('click', e => { if (!e.target.closest('.nav-group')) closeGroups(); });
  document.addEventListener('keydown', e => {
    if (e.key !== 'Escape') return;
    const open = document.querySelector('.nav-group.open');
    closeGroups();
    open?.querySelector('.nav-sub-toggle')?.focus();
  });

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

// Click-to-play YouTube embeds: swap the poster for the player only on demand,
// so the page never loads YouTube's scripts for visitors who don't press play.
document.querySelectorAll('.video-embed[data-video-id]').forEach(fig => {
  const btn = fig.querySelector('.video-poster');
  if (!btn) return;
  btn.addEventListener('click', () => {
    const iframe = document.createElement('iframe');
    iframe.className = 'video-frame';
    iframe.src = 'https://www.youtube-nocookie.com/embed/' + fig.dataset.videoId + '?autoplay=1&rel=0';
    iframe.title = btn.getAttribute('aria-label') || 'Video';
    iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
    iframe.allowFullscreen = true;
    btn.replaceWith(iframe);
    iframe.focus();
  });
});
