Profile artwork uses the original illustrated portrait from `top-banner.jpg`, with the existing black, mint, and lavender palette.

- `python3 scripts/build_assets.py` rebuilds the self-contained animated SVGs. Edit `assets/projects.json` to change the featured cards.
- `node scripts/render_banner.cjs` exports the eight-second desktop and mobile GIF loops and their still PNGs. It requires Node.js, Playwright, Chrome, and FFmpeg. Generated frames stay in the ignored `.preview` directory.
- `GITHUB_TOKEN=… python3 scripts/update_activity.py` retrieves contribution data and public events from GitHub. The scheduled workflow runs daily at 08:53 India time and uses the repository's `NOTIFYME_API_KEY` secret for completion and failure notifications.

The README selects explicit still SVGs and banner PNGs for `prefers-reduced-motion`, plus separate banner/card layouts on small screens. Animated SVGs also include a reduced-motion CSS rule. All SVGs embed their own artwork and need no third-party rendering service. The existing ecosystem statistics image remains backed by its original live API.
