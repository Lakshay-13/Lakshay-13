/* Export SVG animation as looping, GitHub-compatible GIFs. */
const { chromium } = require('playwright');
const fs = require('node:fs/promises');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const { execFileSync } = require('node:child_process');

const root = path.resolve(__dirname, '..');
const duration = 8;

async function main() {
  const browser = await chromium.launch({ headless: true, channel: process.env.BROWSER_CHANNEL || 'chrome' });
  try {
    const flags = new Set(process.argv.slice(2));
    const jobs = [];
    if (!flags.has('--projects') || flags.has('--all')) jobs.push(['banner', 15], ['banner-mobile', 15]);
    if (flags.has('--projects') || flags.has('--all')) {
      const projects = JSON.parse(await fs.readFile(path.join(root, 'assets', 'projects.json'), 'utf8'));
      for (const project of projects) jobs.push([`projects/${project.id}`, 8], [`projects/${project.id}-mobile`, 8]);
    }
    async function exportLoop(name, fps) {
      const source = await fs.readFile(path.join(root, 'assets', `${name}.svg`), 'utf8');
      const [, widthText, heightText] = source.match(/<svg[^>]*width="(\d+)" height="(\d+)"/);
      const width = Number(widthText), height = Number(heightText);
      const frames = path.join(root, '.preview', `${name}-frames`);
      await fs.mkdir(frames, { recursive: true });
      const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: 1 });
      await page.goto(pathToFileURL(path.join(root, 'assets', `${name}.svg`)).href);
      await page.evaluate(async () => {
        await document.fonts.ready;
        await Promise.all([...document.querySelectorAll('image')].map(image => new Promise((resolve, reject) => {
          const probe = new Image();
          probe.onload = resolve;
          probe.onerror = () => reject(new Error('Embedded artwork failed to load.'));
          probe.src = image.getAttribute('href');
        })));
      });
      const clippedPills = await page.evaluate(() => [...document.querySelectorAll('[data-pill]')].filter(pill => {
        const bounds = pill.querySelector('text').getBBox();
        const rect = pill.querySelector('rect');
        return bounds.x < Number(rect.getAttribute('x')) + 8 || bounds.x + bounds.width > Number(rect.getAttribute('x')) + Number(rect.getAttribute('width')) - 8;
      }).length);
      if (clippedPills) throw new Error(`${name}: ${clippedPills} labels do not fit inside their pills.`);
      const clippedText = await page.evaluate(() => {
        const svg = document.documentElement;
        const width = svg.viewBox.baseVal.width, height = svg.viewBox.baseVal.height;
        return [...svg.querySelectorAll('text')].filter(text => {
          if (text.closest('g[transform]')) return false;
          const b = text.getBBox();
          return b.x < 0 || b.x+b.width > width || b.y < 0 || b.y+b.height > height;
        }).map(text => text.textContent);
      });
      if (clippedText.length) throw new Error(`${name}: clipped text: ${clippedText.join(', ')}`);
      await page.emulateMedia({ reducedMotion: 'reduce' });
      if (name.startsWith('banner')) await page.screenshot({ path: path.join(root, 'assets', `${name}-still.png`), omitBackground: true });
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
      const rawGif = path.join(root, '.preview', `${name}-raw.gif`);
      execFileSync('ffmpeg', [
        '-hide_banner', '-loglevel', 'error', '-y', '-framerate', String(fps),
        '-i', path.join(frames, '%04d.png'),
        '-filter_complex', 'split[a][b];[a]palettegen=stats_mode=diff:reserve_transparent=1[p];[b][p]paletteuse=dither=bayer:bayer_scale=3:diff_mode=rectangle',
        '-loop', '0', rawGif
      ], { stdio: 'inherit' });
      execFileSync(process.env.GIFSICLE_PATH || 'gifsicle', [
        '-O3', rawGif, '-o', path.join(root, 'assets', `${name}.gif`)
      ], { stdio: 'inherit' });
      await page.close();
      console.log(`Exported ${name}: ${duration}s loop at ${fps}fps; reduced-motion ${name.startsWith('banner') ? 'PNG' : 'SVG'} available.`);
    }
    let next = 0;
    await Promise.all(Array.from({ length: 2 }, async () => {
      while (next < jobs.length) {
        const [name, fps] = jobs[next++];
        await exportLoop(name, fps);
      }
    }));
  } finally {
    await browser.close();
  }
}

main().catch(error => { console.error(error.message); process.exitCode = 1; });
