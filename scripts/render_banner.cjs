/* Export SVG animation as looping, GitHub-compatible GIFs. */
const { chromium } = require('playwright');
const fs = require('node:fs/promises');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const { execFileSync } = require('node:child_process');

const root = path.resolve(__dirname, '..');
const defaultDuration = 8;

async function main() {
  const browser = await chromium.launch({ headless: true, channel: process.env.BROWSER_CHANNEL || 'chrome' });
  try {
    const flags = new Set(process.argv.slice(2));
    const selected = process.argv.find(arg => arg.startsWith('--select='))?.slice(9).split(',');
    const includeProjects = flags.has('--projects') || flags.has('--all') || Boolean(selected);
    const jobs = [];
    if (!includeProjects || flags.has('--all') || flags.has('--with-banner')) jobs.push(['banner', 15], ['banner-mobile', 15]);
    if (includeProjects) {
      const projects = JSON.parse(await fs.readFile(path.join(root, 'assets', 'projects.json'), 'utf8'));
      if (selected?.some(id => !projects.some(project => project.id === id))) throw new Error('An unknown project was selected.');
      for (const project of projects.filter(project => selected ? selected.includes(project.id) : project.loop_seconds)) {
        const duration = project.loop_seconds || defaultDuration;
        jobs.push([`projects/${project.id}`, 8, duration], [`projects/${project.id}-mobile`, 8, duration]);
      }
    }
    async function exportLoop(name, fps, duration = defaultDuration) {
      const source = await fs.readFile(path.join(root, 'assets', `${name}.svg`), 'utf8');
      const [, widthText, heightText] = source.match(/<svg[^>]*width="(\d+)" height="(\d+)"/);
      const width = Number(widthText), height = Number(heightText);
      const frames = path.join(root, '.preview', `${name}-frames`);
      await fs.rm(frames, { recursive: true, force: true });
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
      // An SVG embedded as an image has its own clock. Inline the scene in the
      // export page so every animation can be paused and sampled at exact times.
      if (name.startsWith('projects/')) {
        await page.evaluate(() => {
          const source = [...document.querySelectorAll('image')].at(-1);
          const href = source?.getAttribute('href');
          if (!href?.startsWith('data:image/svg+xml;base64,')) return;
          const bytes = Uint8Array.from(atob(href.split(',')[1]), char => char.charCodeAt(0));
          const parsed = new DOMParser().parseFromString(new TextDecoder().decode(bytes), 'image/svg+xml');
          if (parsed.querySelector('parsererror')) throw new Error('The embedded SVG scene could not be parsed.');
          const scene = document.importNode(parsed.documentElement, true);
          const ids = new Map([...scene.querySelectorAll('[id]')].map(node => [node.id, 'embedded-' + node.id]));
          for (const node of [scene, ...scene.querySelectorAll('*')]) {
            for (const attr of [...node.attributes]) {
              let value = attr.value.replace(/url\(#([^)]+)\)/g, (match, id) => ids.has(id) ? 'url(#' + ids.get(id) + ')' : match);
              if (attr.name === 'id') value = ids.get(value) || value;
              if (attr.name === 'href' && value.startsWith('#') && ids.has(value.slice(1))) value = '#' + ids.get(value.slice(1));
              if (value !== attr.value) node.setAttribute(attr.name, value);
            }
          }
          for (const attr of ['x', 'y', 'width', 'height', 'preserveAspectRatio']) {
            scene.setAttribute(attr, source.getAttribute(attr));
          }
          source.replaceWith(scene);
        });
      }
      const clippedPills = await page.evaluate(() => [...document.querySelectorAll('[data-pill]')].filter(pill => {
        const bounds = pill.querySelector('text').getBBox();
        const rect = pill.querySelector('rect');
        return bounds.x < Number(rect.getAttribute('x')) + 8 || bounds.x + bounds.width > Number(rect.getAttribute('x')) + Number(rect.getAttribute('width')) - 8;
      }).length);
      if (clippedPills) throw new Error(`${name}: ${clippedPills} labels do not fit inside their pills.`);
      const clippedText = await page.evaluate(() => {
        return [...document.querySelectorAll('text')].filter(text => {
          if (text.closest('g[transform]')) return false;
          const { x, y, width, height } = text.ownerSVGElement.viewBox.baseVal;
          const b = text.getBBox();
          return b.x < x || b.x + b.width > x + width || b.y < y || b.y + b.height > y + height;
        }).map(text => text.textContent);
      });
      if (clippedText.length) throw new Error(`${name}: clipped text: ${clippedText.join(', ')}`);
      await page.emulateMedia({ reducedMotion: 'reduce' });
      if (name.startsWith('banner')) await page.screenshot({ path: path.join(root, 'assets', `${name}-still.png`), omitBackground: true });
      await page.emulateMedia({ reducedMotion: 'no-preference' });
      for (let frame = 0; frame < Math.round(fps * duration); frame++) {
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
      const output = path.join(root, 'assets', `${name}.gif`);
      try {
        execFileSync(process.env.GIFSICLE_PATH || 'gifsicle', ['-O3', rawGif, '-o', output], { stdio: 'inherit' });
      } catch (error) {
        if (error.code !== 'ENOENT' || process.env.GIFSICLE_PATH) throw error;
        if (name.startsWith('projects/')) {
          const displayWidth = name.endsWith('-mobile') ? 480 : 900;
          execFileSync('magick', [rawGif, '-coalesce', '-resize', `${displayWidth}x`, '-fuzz', '3%', '-layers', 'Optimize', '-layers', 'OptimizeTransparency', output], { stdio: 'inherit' });
        } else {
          await fs.copyFile(rawGif, output);
        }
      }
      await page.close();
      console.log(`Exported ${name}: ${duration}s loop at ${fps}fps; reduced-motion ${name.startsWith('banner') ? 'PNG' : 'SVG'} available.`);
    }
    let next = 0;
    await Promise.all(Array.from({ length: 2 }, async () => {
      while (next < jobs.length) {
        const [name, fps, duration] = jobs[next++];
        await exportLoop(name, fps, duration);
      }
    }));
  } finally {
    await browser.close();
  }
}

main().catch(error => { console.error(error.message); process.exitCode = 1; });
