Profile artwork uses the original illustrated portrait from `top-banner.jpg`, with the existing black, mint, and lavender palette.

- `python3 scripts/build_assets.py` rebuilds the self-contained animated SVGs. Pillow measures pill labels and text wrapping. Edit `assets/projects.json` for all 21 project cards and `assets/profile.json` for the profile panels. `assets/logos/sources.json` and `assets/brands/sources.json` record verified artwork sources. Brand imagery remains separate from the vector workflow illustrations.
- `scripts/project_scenes.py` defines a distinct animation for every project, grounded in the linked product pages and repository READMEs. These are illustrative scenes, not screenshots or measured results. Morph Images shows graph interpolation; Grid shows triangular tessellation; Transcribe shows the current macOS local/API app.
- `node scripts/render_banner.cjs --all` exports eight-second desktop and mobile GIF loops, with transparent corners. It requires Node.js, Playwright, Chrome, FFmpeg, and Gifsicle; `GIFSICLE_PATH` selects an executable. Use `--select=fren,artgridx` to rebuild specific cards and `--with-banner` to include the banner. Generated frames stay in the ignored `.preview` directory.
- `python3 scripts/build_readme.py` assembles the visual README from the same profile and project data.
- `GITHUB_TOKEN=… python3 scripts/update_activity.py` retrieves verified contribution data without modifying the README or adding public-event lists. The scheduled workflow runs daily at 08:53 India time and uses the repository's `NOTIFYME_API_KEY` secret for completion and failure notifications.

The banner keeps the original wording and illustrated avatar from `top-banner.jpg`. Its starfield contains 250 stars on desktop and 190 on mobile, plus a rotating wreath of 72 stars. The motion begins immediately, with faster twinkles and no initial hold.

The README selects explicit still SVGs and PNGs for reduced motion, plus mobile layouts. Connect uses three columns and two rows. About and contact panels have no animated divider lines. Toolkit imagery shows Python, Codex, GCP/AWS, database/API systems, and PINNs/neural nets. All SVGs embed their artwork. Ecosystem statistics remain backed by the original live API.

FREN, ArtGridX, and Watermark Studio use their authentic logos with motion. The Watermark logo comes from the application's source because its current public website returns 404. Zinging's cat logo and Chat/Translate/Memory scene take inspiration from the reference profile. Host describes image/document file sharing rather than application deployment.

Every authored link includes `target="_blank"` and `rel="noopener noreferrer"`. GitHub's Markdown sanitizer removes those attributes, so README authors cannot force a new tab on GitHub. This behavior was verified with GitHub's Markdown API.
