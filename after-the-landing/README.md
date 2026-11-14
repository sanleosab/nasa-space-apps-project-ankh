# AFTER THE LANDING — Premium Space Heritage Explorer

A responsive, cinematic educational archive exploring mission hardware, science instruments and historic traces left on the Moon and Mars.

## Run on macOS

1. Extract `after-the-landing-premium.zip`.
2. Open the `after-the-landing` folder in VS Code or Finder.
3. Open `index.html` in a browser, or use VS Code Live Server for local development.
4. No npm install, build step, backend or external JavaScript library is required.

Internet is used only for Google Fonts. All 18 project photographs are stored locally and remain available offline.

## What is included

- Home page with expanded editorial content and a classification guide to deployed, discarded and deliberately impacted hardware.
- Dedicated Moon and Mars pages with distinct animated planetary scenes, orbital elements, world-specific facts and editorial chapters.
- 18 mission-object records with individual dossier pages, facts, mission context, status, purpose, legacy and related records.
- Expanded, alternating mission timeline with lunar/Martian colour coding and scroll progress.
- Archive filters, responsive navigation, source references and heritage section.
- Initial loading screen, page transitions, top reading-progress indicator and an ambient-motion switch.
- Keyboard focus states, responsive layouts and reduced-motion support.
- All 18 local JPG images in `images/moon` and `images/mars`.

## Important content distinctions

- Apollo 11 used EASEP; the full ALSEP package was deployed on Apollo 12, 14, 15, 16 and 17.
- Apollo descent stages were left at the six crewed landing sites.
- Ranger spacecraft and selected Saturn V S-IVB stages deliberately impacted the Moon; they were not soft-landed equipment.
- Perseverance's parachute, backshell and other landing components are discarded hardware. Perseverance itself is an active rover and is not abandoned.
- Curiosity is included as an active-mission comparison, clearly labelled as not abandoned.
- The timeline distinguishes mission events from the continuing work of orbital documentation.

## Images and credits

The image files were retrieved through NASA's public Images API search. The search can return representative imagery rather than a guaranteed exact archival photograph for every historical object. Review the original NASA asset record for photographer/creator credits and any third-party restrictions before public or commercial reuse. NASA should be credited appropriately, and imagery must not imply NASA endorsement.

## Updating images

The included `download_images.py` can be run from this folder:

```bash
python3 download_images.py
```

It may require the `requests` and `certifi` Python packages. It uses normal HTTPS certificate verification.

## ANKH identity and planetary visuals
The project identity is **After the Landing**, created by **ANKH**. The home hero now presents both the Moon and Mars, and the destination pages use animated equirectangular planetary surface maps instead of CSS-drawn pseudo-planets.

Planet texture source: Solar System Scope texture library — https://www.solarsystemscope.com/textures/ (check the current attribution/licence terms before redistribution). The texture maps are loaded from the source host, so an internet connection is required for the photographic surface detail; the site retains its dark-space fallback styling if they are unavailable.
