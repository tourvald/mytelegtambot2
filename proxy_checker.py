import asyncio
from pyppeteer import launch
import time

async def fetch_headings(url):
    browser = await launch(headless=False, args=['--no-sandbox'], devtools=True)
    page = await browser.newPage()

    # Настройки для минимизации детектирования автоматизации
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    await page.setJavaScriptEnabled(True)
    await page.evaluateOnNewDocument('''() => {
        Object.defineProperty(navigator, 'webdriver', {
            get: () => false,
        });
    }''')
    await page.evaluateOnNewDocument('''() => {
        window.chrome = {
            runtime: {},
        };
    }''')
    await page.evaluateOnNewDocument('''() => {
        Object.defineProperty(navigator, 'languages', {
            get: () => ['en-US', 'en'],
        });
    }''')
    await page.evaluateOnNewDocument('''() => {
        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3],
        });
    }''')

    retries = 5
    delay = 15  # Initial delay

    for attempt in range(retries):
        try:
            await page.goto(url, {'waitUntil': 'networkidle2'})
            h1 = await page.evaluate('''() => Array.from(document.querySelectorAll('h1')).map(element => element.textContent)''')
            h2 = await page.evaluate('''() => Array.from(document.querySelectorAll('h2')).map(element => element.textContent)''')
            h3 = await page.evaluate('''() => Array.from(document.querySelectorAll('h3')).map(element => element.textContent)''')
            await browser.close()
            return {'url': url, 'h1': h1, 'h2': h2, 'h3': h3}
        except Exception as e:
            print(f"Attempt {attempt+1} for URL {url} failed: {e}")
            if attempt < retries - 1:
                print(f"Retrying in {delay} seconds...")
                await asyncio.sleep(delay)
                delay *= 2  # Increase the delay
            else:
                print(f"All attempts failed for URL {url}")
                await browser.close()
                return {'url': url, 'error': str(e)}

async def main(urls):
    results = []
    for url in urls:
        result = await fetch_headings(url)
        results.append(result)
    return results

urls = [
    "https://www.avito.ru/moskva/telefony/mobile-ASgBAgICAUSwwQ2I_Dc?bt=1&cd=1&f=ASgBAQICAUSwwQ2I_DcBQOjrDjT~_dsC_P3bAvr92wI&q=iphone+12+128+-pro+-max+-mini&s=104&user=1",
    "https://www.avito.ru/moskva_i_mo/telefony/mobilnye_telefony/apple-ASgBAgICAkS0wA3OqzmwwQ2I_Dc?bt=1&f=ASgBAQICA0SywA2MgTy0wA3OqzmwwQ2I_DcDQPa8DRSU0jTm4A0U~MFc6OsONP792wL8_dsC~v3bAg&q=iphone+12+pro+max+256&s=104&user=1",
    "https://www.avito.ru/moskva_i_mo/telefony/mobile-ASgBAgICAUSwwQ2I_Dc?f=ASgBAQICA0SywA2Cr5QRtMAN3q45sMENiPw3AkDm4A0U~MFc6OsONP792wL8_dsC~v3bAg&q=Xiaomi+Redmi+Note+12+Pro+256&s=104",
    "https://www.avito.ru/moskva_i_mo/telefony?bt=1&f=ASgCAQICAUD2vA0UlNI0&q=Oneplus+7+pro+256&user=1",
    "https://www.avito.ru/moskva/telefony/mobilnye_telefony/xiaomi-ASgBAgICAkS0wA3erjmwwQ2I_Dc?cd=1&f=ASgBAQICA0SywA2egTy0wA3erjmwwQ2I_DcDQOTgDRSMwlzm4A0U9sFc6OsONP792wL8_dsC~v3bAg&q=xiaomi+mi+10t+128+-lite+-pro&s=104"
]

results = asyncio.get_event_loop().run_until_complete(main(urls))
for result in results:
    print(result)