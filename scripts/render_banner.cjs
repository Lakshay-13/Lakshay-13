/* Export the SVG banner's CSS animation as a looping, GitHub-compatible GIF. */
const { chromium } = require('playwright');
const fs = require('node:fs/promises');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const { execFileSync } = require('node:child_process');

const root = path.resolve(__dirname, '..');
const fps = 15;
const duration = 8;

async function main() {
  const browser = await chromium.launch({ headless: true, channel: process.env.BROWSER_CHANNEL || 'chrome' });
  try {
    for (const [name, width, height] of [['banner', 1200, 480], ['banner-mobile', 640, 700]]) {
      const frames = path.join(root, '.preview', `${name}-frames`);
      await fs.mkdir(frames, { recursive: true });
      const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: 1 });
      await page.goto(pathToFileURL(path.join(root, 'assets', `${name}.svg`)).href);
      await page.evaluate(async () => {
        await document.fonts.ready;
        await Promise.all([...document.querySelectorAll('image')].map(image => new Promise((resolve, reject) => {
          const probe = new Image();
          probe.onload = resolve;
          probe.onerror = () => reject(new Error('The original avatar failed to load.'));
          probe.src = image.getAttribute('href');
        })));
      });
      await page.emulateMedia({ reducedMotion: 'reduce' });
      await page.screenshot({ path: path.join(root, 'assets', `${name}-still.png`), omitBackground: true });
      await page.emulateMedia({ reducedMotion: 'no-preference' });
      for (let frame = 0; frame < fps * duration; frame++) {
        await page.evaluate(time => {
          for (const animation of document.getAnimations()) {
            animation.pause();
            animation.currentTime = time;
          }
        }, frame * 1000 / fps);
        await page.screenshot({ path: path.join(frames, `${String(frame).padStart(4, '0')}.png`), omitBackground: true });
      }
      execFileSync('ffmpeg', [
        '-hide_banner', '-loglevel', 'error', '-y', '-framerate', String(fps),
        '-i', path.join(frames, '%04d.png'),
        '-filter_complex', 'format=rgb24,split[a][b];[a]palettegen=stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=3:diff_mode=rectangle',
        '-loop', '0', path.join(root, 'assets', `${name}.gif`)
      ], { stdio: 'inherit' });
      await page.close();
      console.log(`Exported ${name}: ${duration}s loop at ${fps}fps, plus reduced-motion PNG.`);
    }
  } finally {
    await browser.close();
  }
}

main().catch(error => { console.error(error.message); process.exitCode = 1; });
