#!/usr/bin/env node
/**
 * html2pptx.js — Convert HTML report/slides → PPTX
 *
 * Strategy: Puppeteer captures each slide section as a high-res PNG image,
 * then pptxgenjs assembles them into a PPTX file with correct aspect ratio.
 *
 * Usage:
 *   node html2pptx.js <input.html> [output.pptx] [options]
 *
 * Options:
 *   --width  <px>     Slide width in pixels for capture (default: 1280)
 *   --height <px>     Slide height in pixels for capture (default: 720)
 *   --selector <css>  CSS selector for slide sections (default: .slide, section, article)
 *   --full-page       Treat entire page as one slide
 *   --quality <1-100> PNG quality (default: 95)
 *   --delay <ms>      Wait after page load for animations (default: 500)
 *   --layout <ratio>  Slide aspect: WIDE (16:9) | LAYOUT_4x3 | LAYOUT_WIDE (default: WIDE)
 *
 * Auto-installs: puppeteer, pptxgenjs
 *
 * Requirements: Node.js 16+
 */

const { execSync, spawnSync } = require("child_process");
const path = require("path");
const fs = require("fs");
const os = require("os");

// ── Dependency installation ───────────────────────────────────────────────────

function npmInstall(pkg) {
  console.error(`Installing ${pkg}...`);
  const result = spawnSync("npm", ["install", pkg, "--save-dev"], {
    stdio: "inherit",
    cwd: __dirname,
  });
  if (result.status !== 0) {
    // Try global install as fallback
    spawnSync("npm", ["install", "-g", pkg], { stdio: "inherit" });
  }
}

function tryRequire(pkg, importName = null) {
  const name = importName || pkg;
  try {
    return require(name);
  } catch {
    npmInstall(pkg);
    return require(name);
  }
}

// ── Argument parsing ──────────────────────────────────────────────────────────

function parseArgs() {
  const args = process.argv.slice(2);
  const opts = {
    input: null,
    output: null,
    width: 1280,
    height: 720,
    selector: null,
    fullPage: false,
    quality: 95,
    delay: 500,
    layout: "LAYOUT_WIDE",
  };

  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case "--width":    opts.width = parseInt(args[++i]); break;
      case "--height":   opts.height = parseInt(args[++i]); break;
      case "--selector": opts.selector = args[++i]; break;
      case "--full-page":opts.fullPage = true; break;
      case "--quality":  opts.quality = parseInt(args[++i]); break;
      case "--delay":    opts.delay = parseInt(args[++i]); break;
      case "--layout":   opts.layout = args[++i]; break;
      default:
        if (!opts.input)       opts.input = args[i];
        else if (!opts.output) opts.output = args[i];
    }
  }

  if (!opts.input) {
    console.error("Usage: node html2pptx.js <input.html> [output.pptx] [options]");
    process.exit(1);
  }

  // Default output filename
  if (!opts.output) {
    opts.output = opts.input.replace(/\.html?$/, "") + ".pptx";
  }

  return opts;
}

// ── Main ──────────────────────────────────────────────────────────────────────

async function main() {
  const opts = parseArgs();

  // Resolve absolute input path
  const inputPath = path.resolve(opts.input);
  if (!fs.existsSync(inputPath)) {
    console.error(`Error: Input file not found: ${inputPath}`);
    process.exit(1);
  }

  console.log(`\n📄 Input:  ${inputPath}`);
  console.log(`📊 Output: ${path.resolve(opts.output)}`);
  console.log(`📐 Slide:  ${opts.width}×${opts.height}px (${opts.layout})\n`);

  // Load dependencies
  const puppeteer = tryRequire("puppeteer");
  const PptxGenJS = tryRequire("pptxgenjs");

  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), "html2pptx-"));

  try {
    // ── Step 1: Launch browser ───────────────────────────────────────────────
    console.log("🚀 Launching browser...");
    const browser = await puppeteer.launch({
      headless: "new",
      args: ["--no-sandbox", "--disable-setuid-sandbox"],
    });
    const page = await browser.newPage();

    // Set viewport to slide dimensions
    await page.setViewport({ width: opts.width, height: opts.height });

    // Load HTML file
    const fileUrl = `file://${inputPath}`;
    await page.goto(fileUrl, { waitUntil: "networkidle0", timeout: 30000 });

    // Wait for animations/charts to render
    if (opts.delay > 0) {
      await new Promise((r) => setTimeout(r, opts.delay));
    }

    // ── Step 2: Find slides ──────────────────────────────────────────────────
    let slideScreenshots = [];

    if (opts.fullPage) {
      // Capture entire page as one slide
      const screenshotPath = path.join(tmpDir, "slide-001.png");
      await page.screenshot({
        path: screenshotPath,
        fullPage: true,
        type: "png",
      });
      slideScreenshots.push(screenshotPath);
      console.log("  📸 Captured full page as single slide");
    } else {
      // Try to find slide sections
      const selectors = opts.selector
        ? [opts.selector]
        : [".slide", "[data-slide]", "section.slide", "article.slide",
           "section", "article"];

      let elements = [];
      for (const sel of selectors) {
        elements = await page.$$(sel);
        if (elements.length > 0) {
          console.log(`  🔍 Found ${elements.length} slides via selector: "${sel}"`);
          break;
        }
      }

      if (elements.length === 0) {
        // Fallback: full page as single slide
        console.log("  ⚠️  No slide sections found — capturing full page as one slide");
        console.log("     Tip: Add class=\"slide\" to each <section> for multi-slide output");
        const screenshotPath = path.join(tmpDir, "slide-001.png");
        await page.screenshot({
          path: screenshotPath,
          fullPage: false,
          type: "png",
        });
        slideScreenshots.push(screenshotPath);
      } else {
        // Capture each slide element
        for (let i = 0; i < elements.length; i++) {
          const screenshotPath = path.join(tmpDir, `slide-${String(i + 1).padStart(3, "0")}.png`);

          // Scroll element into view and capture
          await elements[i].evaluate((el) => {
            el.scrollIntoView({ behavior: "instant", block: "start" });
          });
          await new Promise((r) => setTimeout(r, 100)); // brief render pause

          await elements[i].screenshot({
            path: screenshotPath,
            type: "png",
          });

          slideScreenshots.push(screenshotPath);
          process.stdout.write(`  📸 Slide ${i + 1}/${elements.length}\r`);
        }
        console.log(`\n  ✅ ${elements.length} slides captured`);
      }
    }

    await browser.close();

    // ── Step 3: Assemble PPTX ────────────────────────────────────────────────
    console.log("\n🔧 Assembling PPTX...");

    const pptx = new PptxGenJS();
    pptx.layout = opts.layout; // "LAYOUT_WIDE" = 16:9

    for (let i = 0; i < slideScreenshots.length; i++) {
      const imgPath = slideScreenshots[i];
      const slide = pptx.addSlide();

      // Full-bleed image — fills entire slide
      slide.addImage({
        path: imgPath,
        x: 0,
        y: 0,
        w: "100%",
        h: "100%",
      });
    }

    await pptx.writeFile({ fileName: opts.output });

    console.log(`\n✅ Done! ${slideScreenshots.length} slide(s) → ${opts.output}`);
    console.log(`   File size: ${(fs.statSync(opts.output).size / 1024).toFixed(0)} KB\n`);

  } finally {
    // Cleanup temp files
    fs.rmSync(tmpDir, { recursive: true, force: true });
  }
}

// ── Run ───────────────────────────────────────────────────────────────────────

main().catch((err) => {
  console.error("\n❌ Error:", err.message);
  if (err.stack) console.error(err.stack);
  process.exit(1);
});
