import time

from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pynput.keyboard import Key, Controller

keyboard = Controller()
topic_links = []


def create_driver():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--disable-web-security")

    DRIVER = webdriver.Chrome(options=chrome_options)
    return DRIVER


def login(LOGIN_PAGE: webdriver.Chrome):
    username = LOGIN_PAGE.find_element(By.ID, "loginUsername")
    username.clear()
    username.send_keys("jonleR333")
    password = LOGIN_PAGE.find_element(By.ID, "loginPassword")
    password.clear()
    password.send_keys("jonReddit333*")

    time.sleep(1)

    LOGIN_PAGE.find_element(
        By.XPATH, '//html/body/div/main/div[1]/div/div[2]/form/fieldset[5]/button').click()

    WebDriverWait(LOGIN_PAGE, 60).until(
        EC.title_is("Reddit - Explora lo que quieras"))


def searchTopic(topic, SEARCH_PAGE: webdriver.Chrome):
    search_bar = SEARCH_PAGE.find_element(
        By.XPATH, '//*[@id="header-search-bar"]')
    search_bar.clear()
    search_bar.send_keys(topic)
    search_bar.click()
    keyboard.press(Key.enter)
    WebDriverWait(SEARCH_PAGE, 60).until(
        EC.title_is("reddit.com: resultados de búsqueda - "+topic))


def getTopicLinks(RESULTS_PAGE: webdriver.Chrome):

    results_div = RESULTS_PAGE.find_elements(
        By.XPATH, '//*[@id="SHORTCUT_FOCUSABLE_DIV"]/div[2]/div/div/div/div[2]/div/div/div[2]/div[1]/div[2]/div[1]/div')

    for element in results_div:
        link = element.find_element(
            By.XPATH, '//div/div/div[2]/a').get_attribute("href")
        topic_links.append(link)


def dowlonadContent(link, CONTENT_PAGE: webdriver.Chrome):
    print("todo")


if __name__ == '__main__':

    START_URL = "https://www.reddit.com/login"

    try:

        DRIVER = create_driver()
        DRIVER.get(START_URL)
        login(DRIVER)
        searchTopic('crypto', DRIVER)
        getTopicLinks(DRIVER)

    finally:
        DRIVER.delete_all_cookies()
        DRIVER.quit()
        print("Chrome cerrado")
