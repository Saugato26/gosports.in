# Homepage concept QA

Source: /Users/sreeb/.codex/generated_images/01a094e8-d7e2-79f3-9d52-98a87508dcb6/exec-a5c54cd4-d115-41c7-a73d-ec7ab537db9a.png

Initial screenshot: /Users/sreeb/.codex/visualizations/2026/09/12/01a094e8-d7e2-79f3-9d52-98a87508dcb6/gosports-home-qa/desktop-before.png

Viewport: 1487 × 1058; source and screenshot both 1487 × 1058 pixels, CSS viewport 1487 × 1058, density 1.
State: homepage initial scroll, desktop.

Initial comparison: images emitted together in one browser comparison input.
- P1: athlete too central compared with target; reposition original photograph right to preserve identity while matching composition.
- P2: headline and support heading too light/narrow; increase Satoshi weight and headline size.
- P2: eyebrow divider too long; use short divider matching reference.

## Final comparison

Implementation screenshot: /Users/sreeb/.codex/visualizations/2026/09/12/01a094e8-d7e2-79f3-9d52-98a87508dcb6/gosports-home-qa/desktop-final.png
Full-view comparison: selected source and final browser screenshot displayed together in the same comparison input, same 1487 × 1058 viewport. The headline, navigation, CTA, photo and support strip were all legible at this size; no additional focused crop was needed.

### Fidelity surfaces
- Typography: Satoshi, strengthened to 900 for headline and support heading; three-line desktop headline retained. Browser rasterisation and the generated reference's letter shapes differ slightly (P3).
- Spacing: white 84px header, large dark hero, 164px support strip and consistent left alignment. Eyebrow divider shortened after initial comparison.
- Colors: original brand red #C71B23 retained rather than the mockup's brighter red. White/ink contrast and understated decorative rings retained.
- Images: original athlete photograph and supplied logo reused, preserving the real subject rather than reproducing AI changes to their pose. Photograph shifted right to match the selected composition. Generated transparent arcs are decorative only; their exact curvature is a P3 difference.
- Copy: selected headline, supporting copy, actions and role labels retained. Supporting section describes programmes generally rather than inventing personal support relationships or an athlete biography.

### Comparison history
1. Initial screenshot desktop-before.png: athlete too central (P1), lighter type and long divider (P2). Fixed position, type weight/size and divider. Recompared in desktop-after.png and desktop-final.png; no remaining actionable P0/P1/P2 desktop differences.
2. 320px check: existing testimonial grid overflowed by 11px (P2). Stacked it at narrow widths; browser measurement now reports no overflow. Evidence narrow-after.png.
3. 768px check: headline approached athlete's face (P2). Extended stacked image/text layout to tablet sizes; tablet-after.png shows legible separated copy and original photo.

### Interaction and responsive checks
- Browser inspected at 1487 × 1058, 768 × 1024, 390 × 844 and 320 × 740.
- No horizontal overflow measured at final desktop, tablet and 320px states.
- Scroll cue reaches support-team; mentorship link opens its programme page.
- Explore our work opens Programmes; Get involved and Partner with us reach their intended page/anchor.
- Mobile menu opens, aria-expanded updates, Escape closes it and restores focus.
- All newly referenced hero images loaded; no browser error logs reported.
- Local homepage href/src paths and anchors resolve; JS syntax and git diff whitespace checks pass.
- Motion is progressive and explicitly disabled for reduced-motion users. No-JS and reduced-motion runtime modes were not separately emulated; source fallback reviewed.

### Scope and residual limitations
This is a local implementation of the selected homepage concept. It does not implement the CMS, approval gates or other architecture-checklist items. Website-use consent, final editorial approval, physical-device and screen-reader testing remain launch tasks. Header simplified on the homepage to match the selected design; other routes retain existing navigation.

### Asset provenance
- Athlete: existing assets/img/home-ecosystem.jpg; unmodified source.
- Logo: existing assets/img/gallery/brand-logo-black.webp.
- Arcs: assets/img/hero-support-rings.png, generated with built-in ImageGen. Prompt brief: transparent square overlay, three thin incomplete concentric arcs, muted red inner ring and subtle gray outer arcs, no fill, text or people, grounded in selected reference. Output is 1254px square and scaled in layout.
- Arrows: Bootstrap Icons 1.11.3; local SVGs and licence included under assets/img/icons/.

### Implementation checklist
- [x] Match selected desktop composition using real source photography.
- [x] Connect primary and supporting actions.
- [x] Verify responsive layout and menu behaviour.
- [x] Preserve readable content without animation.
- [x] Recompare after P1/P2 fixes.

final result: passed
