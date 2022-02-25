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


async def main():
    try:
        async with async_playwright() as p:
            url = "reddit.com/login"

            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()
            await page.goto("https://"+url)
            # await page.locator('text = Iniciar').click()
            # element = await page.query_selector('text = Iniciar Sesión')
            # print(await element.inner_html())
            # await element.click()

            # time.sleep(3)
            usernameElement = await page.query_selector('#loginUsername')

            passwordElement = await page.query_selector('#loginPassword')

            await login(usernameElement, passwordElement)

            element = await page.query_selector('button:has-text("Iniciar")')

            await element.click()

            time.sleep(10)
            search = await page.query_selector('input')
            print(await search.inner_html())
            await search.fill('crypto')
            time.sleep(2)
            await page.press('input', 'Enter')

            # results = await page.query_selector('/html/body/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div/div/div[2]/div[1]/div[2]/div[1]')
            # /html/body/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div/div/div[2]/div[1]/div[2]/div[1]/div[1]/div/div/div/div/div[2]/div/div/div[1]/a
            # /html/body/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div/div/div[2]/div[1]/div[2]/div[1]/div[2]/div/div/div/div/div[2]/div/div/div[1]/a
            # results.query_selector_all()

            for contador in range(1, 8):
                r = await page.query_selector('//html/body/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div/div/div[2]/div[1]/div[2]/div[1]/div[1]/div/div/div/div/div[2]/div/div/div[1]')
                print(Fore.RED + await r.inner_html())

            # results = await page.query_selector('//*[@id="SHORTCUT_FOCUSABLE_DIV"]/div[2]/div/div/div/div[2]/div/div/div[2]/div[1]/div[2]/div[1]/div[1]')
            # resultsChildren = await results.query_selector_all('div')
            # print(len(resultsChildren))
            # for result in resultsChildren:
                # print(Fore.GREEN + await result.inner_html()+"\n")
             #   print("a")

            # await close(browser)
    except Exception:
        print(traceback.format_exc())
        print("error")

asyncio.run(main())


# //*[@id="t3_s98fhs"]/div/div/div[2]/div[1]/div/div[1]/a                     //*[@id="SHORTCUT_FOCUSABLE_DIV"]/div[2]/div/div/div/div[2]/div/div/div[2]/div[1]/div[2]/div[1]/div[1]
# link = await result.query_selector_all('div > div > div')
# for l in link:
#    print(Fore.BLUE + await l.inner_html())
# print(Fore.BLUE +  link)      //*[@id="t3_sh0tgg"]/div/div/div[2]/div/div/div[1]/a
##print(Fore.GREEN +result.count())
