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
    async with async_playwright() as p:
        if(len(linksToVisit) < 1):
            print("ya")
            return
        else:
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()
            await page.goto("https://reddit.com"+linksToVisit[0])
            sublist = linksToVisit[1:(len(linksToVisit)-1)]
            print(linksToVisit[0])
            time.sleep(5)
            main = await page.query_selector('//html/body/div[1]/div/div[2]/div[3]/div/div/div/div[2]/div[1]/div[2]/div[1]/div')
            text = await main.inner_text()
            #writeToFile(text, (len(linksToVisit)-1))
            await browser.close()
            await downloadContent(sublist)


""" async def clickLinks(links):
    async with async_playwright() as p:
        for pos in range(0, len(links)):
            browser = await p.chromium.launch()
            page = await browser.new_page()
            
            
            await page.goto("https://reddit.com"+links[pos]) """


def writeToFile(text, index):
    f = open("files/content"+str(index)+".txt", "w")
    f.write(text)
    f.close()


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
            linksToVisit.append(await (await page.query_selector('//html/body/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div/div/div[2]/div[1]/div[2]/div[1]/div[0]/div/div/div/div/div[2]/div/div[1]/a')).get_attribute('href'))

            print("ieup")
            for child in range(1, len(resultsChildren)):
                r = await page.query_selector('//html/body/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div/div/div[2]/div[1]/div[2]/div[1]/div['+str(child)+']/div/div/div/div/div[2]/div/div/div[1]/a')
                #                               /html/body/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div/div/div[2]/div[1]/div[2]/div[1]/div[0]/div/div/div/div/div[2]/div/div[1]/a
                #                               /html/body/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div/div/div[2]/div[1]/div[2]/div[2]/div[2]/div/div/div/div/div[2]/div[1]/div/div[1]/a
                #                               /html/body/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div/div/div[2]/div[1]/div[2]/div[2]/div[1]/div/div/div/div/div[2]/div/div/div[1]/a
                print(await r.get_attribute('href'))
                linksToVisit.append(await r.get_attribute('href'))

            time.sleep(5)
            await downloadContent(linksToVisit)
            await browser.close()

    except Exception:
        await browser.close()
        print(traceback.format_exc())
        print("error")

asyncio.run(main())
