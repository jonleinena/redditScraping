import asyncio
from multiprocessing.connection import wait
from playwright.async_api import async_playwright
import time
import traceback
from colorama import Fore


async def open(url):
    async with async_playwright() as p:

        browser = await p.webkit.launch(headless=False)

        page = await browser.new_page()
        await page.goto("https://"+url)

        await page.screenshot(path="example1.png")
        return browser, page


async def close(browser):
    await browser.close()


async def login(username, password):
    await username.fill('jonleR333')
    await password.fill('jonReddit333*')


async def downloadContent(linksToVisit):
    if(len(linksToVisit) < 1):
        print("ya")
        return
    else:
        await linksToVisit[0].click()
        # hago cosas
        print("E")
        sublist = linksToVisit[1:(len(linksToVisit)-1)]
        await downloadContent(sublist)


async def clickLinks(links):
    async with async_playwright() as p:
        for pos in range(0, len(links)):
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto("https://reddit.com"+links[pos])


async def main():
    try:
        async with async_playwright() as p:
            url = "reddit.com/login"

            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()
            await page.goto("https://"+url)

            usernameElement = await page.query_selector('#loginUsername')

            passwordElement = await page.query_selector('#loginPassword')

            await login(usernameElement, passwordElement)

            element = await page.query_selector('button:has-text("Iniciar")')

            await element.click()

            time.sleep(10)
            search = await page.query_selector('input')
            await search.fill('crypto')
            time.sleep(2)
            await page.press('input', 'Enter')

            time.sleep(5)

            results = await page.query_selector('//*[@id="SHORTCUT_FOCUSABLE_DIV"]/div[2]/div/div/div/div[2]/div/div/div[2]/div[1]/div[2]/div[1]/div[1]')

            resultsChildren = await results.query_selector_all('div')
            print(len(resultsChildren))
            linksToVisit = []
            for child in range(1, len(resultsChildren)):
                r = await page.query_selector('//html/body/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div/div/div[2]/div[1]/div[2]/div[1]/div['+str(child)+']/div/div/div/div/div[2]/div/div/div[1]/a')
                # print(await r.get_attribute('href'))
                linksToVisit.append(await r.get_attribute('href'))

            time.sleep(5)
            await clickLinks(linksToVisit)
            await browser.close()

    except Exception:
        print(traceback.format_exc())
        print("error")

asyncio.run(main())
