# KEMET CODEX

An immersive, information-rich digital codex for exploring ancient Egypt — cinematic real-time 3D of the Giza plateau, an era-scrubbing timeline across five millennia, and layered knowledge that presents the **mainstream archaeological consensus**, the most compelling **alternative hypotheses** (Hancock, Schoch, Bauval, Biondi, Houdin…), and the **latest scientific findings** side by side, always labeled and attributed.

Built from the spec in [`Kemet_Codex_Spec_Handoff.md`](Kemet_Codex_Spec_Handoff.md).

## Run it

No build step. Serve the folder over HTTP and open `index.html`:

```sh
python -m http.server 8741
# → http://localhost:8741
```

(Opening `index.html` directly from disk also works, minus the service worker / install prompt.)

## Features

- **Two monuments** — the Great Pyramid (exterior, cutaway interior, fly-through) and a sculpted Great Sphinx (smooth-shaded bedrock body with nemes headdress, repair-masonry forelegs, enclosure, sand-burial through the ages, **Erosion Lab** that paints Schoch's rain-runoff reading vs the wind-and-salt consensus onto the enclosure walls).
- **The whole necropolis** — Khafre, Menkaure, all six queens' pyramids, Khufu's satellite pyramid, the three causeways, mortuary/valley/Sphinx temples, both cemetery mastaba fields and the boat pits, placed from survey-derived offsets (Petrie / Glen Dash). Procedural limestone-block, polished-casing and rippled-sand textures with bump relief; dune terrain surrounds the flat archaeological zone.
- **Era timeline** — 8 snap-point eras from Predynastic to Modern; casing, capstone, lighting, sky, and the Sphinx's sand level all transform.
- **Theory Lab** — 4 seeded debates with three attributed columns each and a "where it stands" verdict.
- **Knowledge Vault** — 11 searchable, filterable entries with key-facts tables, sources, Wikimedia Commons galleries (with lightbox), and localStorage bookmarks.
- **Family Mode** (✦ in the nav) — kid-friendly explanations appear first, with "go deeper" for the full text.
- **Night & Stars** — a real J2000 bright-star catalog (~130 stars, 33 constellation figures) precessed to each era's epoch: watch the pole star pass from Edasich to Thuban to Kochab to Polaris, the zodiacal Age drift from Gemini through Taurus and Aries into Pisces, and Alnitak slide off the King's Chamber shaft's fixed 45° as fifty centuries of precession accumulate. Two sky moments: **equinox dawn** (the Age constellation rising) and **Orion culmination** (the shaft-alignment test). Deep-linkable via `&sky=dawn|orion`.
- **Minimizable UI** — the control stack, info panel and timeline each collapse to restore chips for an unobstructed viewport (state persists per session).
- **PWA** — installable; the shell and CDN assets cache for offline use after first visit.
- **Accessibility** — keyboard timeline (arrows/Home/End), location list as a non-visual alternative to 3D picking, ARIA roles, `prefers-reduced-motion` support, WebGL fallback diagram.

## File layout

```
index.html          app shell: 3D engine + UI (pack-agnostic)
packs/giza.js       Giza civilization pack: all content + 3D config
manifest.json       PWA manifest
sw.js               service worker (precache shell, runtime-cache CDNs)
icons/              generated PWA icons
tools/gen_icons.py  regenerates the icons (pure stdlib, no Pillow)
```

## Adding a civilization pack (Deep Time Atlas)

Packs are plain JS files that register data on `window.KEMET.packs` — see the shape in [`packs/giza.js`](packs/giza.js). A pack supplies:

- `eras[]` — labels, context text, and a `visual{}` block the engine lerps (casing/ghost/sand levels, sun, sky gradients…)
- `monuments[]` — overview/measurements/theories text, `kid` text for Family Mode, hotspots (position + content), camera `presets`, an optional fly-through `tour`, and `threeConfig` (`model` selects a procedural builder; set `gltfUrl` to swap in a scanned model later)
- `scenery[]` — context geometry (`pyramid`, `ruin`, `causeway`, `mastabas` grids, `pit`)
- `site{ lat }` — drives the engine's precessed night-sky computation; `eras[].year` sets each era's astronomical epoch
- `debates[]`, `vault[]`, `vaultCats[]` — Theory Lab and Knowledge Vault content

Engine changes are only needed for new procedural model types; everything else is data. Göbekli Tepe, the Andes, Oceania → new pack files.

## Content notes

Seed content was written for an educational prototype: measurements follow published surveys (Petrie 1883; Cole 1925; Glen Dash Foundation 2015–2017; Nature 2017 / Nature Communications 2023; PNAS 2022), and every theory block names its proponents. Expand with expert review before public deployment. Photographs are hotlinked from Wikimedia Commons via `Special:FilePath` and degrade gracefully if unavailable.

*Educational exploration, not endorsement.*
