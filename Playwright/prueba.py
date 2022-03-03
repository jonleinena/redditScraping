import asyncio
from multiprocessing.connection import wait
from playwright.async_api import async_playwright
import traceback
import time


async def main():
    try:
        async with async_playwright() as p:
            url = "www.reddit.com/r/CryptoCurrency/comments/s9yfhs/its_actually_impressive_how_fast_people_lose/"

            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()
            await page.goto("https://www.reddit.com/r/CryptoCurrency/comments/s9yfhs/its_actually_impressive_how_fast_people_lose/")
            time.sleep(10)
            # //html/body/div[1]/div/div[2]/div[3]/div/div/div/div[2]/div[1]/div[2]/div[1]/div
            # //*[@id="t3_s9yfhs"]/div
            # //html/body/div[1]/div/div[2]/div[3]/div/div/div/div[2]/div[1]/div[2]/div[1]
            # //*[@id="overlayScrollContainer"]/div[2]/div[1]/div[2]
            # //*[@id="overlayScrollContainer"]/div[2]/div[1]/div[2]
            # /html/body/div[1]/div/div[2]/div[3]/div/div/div/div[2]/div[1]/div[2]/div[1]/div
            print(await page.title())
            res = await page.query_selector(
                '//*[@id="overlayScrollContainer"]/div[2]/div[1]/div[2]/div')
            # r = await page.query_selector('//*[@id="overlayScrollContainer"]/div[2]/div[1]/div[2]/div[1]')
            print(await res.inner_html())

    except Exception:
        # await browser.close()
        print(traceback.format_exc())
        print("error")
        await browser.close()


asyncio.run(main())
