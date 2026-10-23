import {openBrowser} from '@remotion/renderer';
import assert from 'node:assert/strict';

// Executar depois de npm run dev. Usa o Chromium instalado, sem downloads.
const browser = await openBrowser('chrome', {
  browserExecutable: process.env.REMOTION_BROWSER_EXECUTABLE ?? '/usr/bin/chromium',
});
try {
  const page = await browser.newPage({context: () => null, logLevel: 'error',
    indent: false, pageIndex: 0, onBrowserLog: null, onLog: () => {}});
  for (const id of ['TesteHorizontal', 'TesteVertical']) {
    const response = await page.goto({url: `http://127.0.0.1:3000/${id}`, timeout: 30000});
    assert.equal(response.status(), 200);
    let text = '';
    const deadline = Date.now() + 30000;
    while (Date.now() < deadline) {
      text = await page.evaluate(() => document.body.innerText);
      if (text.includes('TESTE TÉCNICO') && text.includes('Material sintético')) break;
      await new Promise(resolve => setTimeout(resolve, 250));
    }
    assert(text.includes('TESTE TÉCNICO') && text.includes('Material sintético'),
      `Composição não carregou no Studio: ${id}\n${text.slice(-2000)}`);
    console.log(`OK: Studio carregou e exibiu a composição ${id}.`);
  }
} finally {
  await browser.close({silent: true});
}
