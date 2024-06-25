import puppeteer from 'puppeteer';

async function captureMapElement(url, outputPath) {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.goto(url, { waitUntil: 'networkidle2' });

    // Introduce a delay if needed for map to load
    await page.waitForSelector('#map2'); // Așteaptă până când harta (#map2) este încărcată
    await new Promise(resolve => setTimeout(resolve, 4000)); // Adaugă o mică întârziere suplimentară (2 secunde)

    // Setează dimensiunea viewport-ului
    await page.setViewport({ width: 1920, height: 1080 });

    // Capturează doar elementul hărții
    const mapElement = await page.$('#map2');
    if (!mapElement) {
        throw new Error('Map element not found!');
    }
    await mapElement.screenshot({ path: outputPath });

    // Închide browser-ul
    await browser.close();
    console.log(`Map element captured successfully and saved to ${outputPath}`);

    return outputPath; // Returnează calea către imaginea generată
}

// Exemplu de utilizare:
captureMapElement('http://127.0.0.1:5500/index.html', 'captura.png')
    .then((outputPath) => console.log(`Captură reușită! Imagine salvată la: ${outputPath}`))
    .catch(err => console.error('Eroare la capturare:', err));
