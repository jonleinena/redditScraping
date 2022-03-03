import time

from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def create_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-web-security")

    DRIVER = webdriver.Chrome(options=chrome_options)
    return DRIVER

captchas_intercepted = []

def captcha_interceptor(request, response):
    if request.path == "/prueba/create_image.php":
        headers = request.response.headers.get_all('set-cookie')
        captcha = headers[0].split(";")[0].split("=")[1]
        captchas_intercepted.append(captcha)

def iniciar_sesion(LOGIN_PAGE: webdriver.Chrome):
    if LOGIN_PAGE.title == "ExVagos - Controles de Usuario":
        print("Sesión ya iniciada")

    elif LOGIN_PAGE.title == "ExVagos":
        print("Inicia Sesión")
        username = LOGIN_PAGE.find_element(By.ID, "navbar_username")
        username.clear()
        username.send_keys("alvaro3639")

        password = LOGIN_PAGE.find_element(By.ID, "navbar_password")
        password.clear()
        password.send_keys("A94271500a")

        time.sleep(1)

        DRIVER.find_element(By.XPATH, "/html/body/div/div/div/table[1]/tbody/tr/td[2]/form/table/tbody/tr[2]/td[2]/input").click()

        LOGIN_PAGE.save_screenshot("sa.png")

        WebDriverWait(LOGIN_PAGE, 60).until(EC.title_is("ExVagos - Controles de Usuario"))

        print("Sesión Iniciada")

    else:
        print("A")

def get_updatedtopics(CONTROLPANEL_PAGE: webdriver.Chrome):
    updated_topics = CONTROLPANEL_PAGE.find_elements(By.XPATH, "//a[starts-with(@id, 'thread_title_')]")
    links = [topic.get_attribute('href') for topic in updated_topics]

    return links

def get_dowloadlinks(TOPIC_PAGE: webdriver.Chrome, link: str):
    TOPIC_PAGE.get(link)
    print(TOPIC_PAGE.title)

    time.sleep(1)

    show_links_buttons = TOPIC_PAGE.find_elements(By.XPATH, "//input[starts-with(@id,'ver_links')]")

    for button in show_links_buttons:
        if button.is_displayed():
            button.click()

            captcha_id = button.get_attribute("id").split("_")[2]

            WebDriverWait(TOPIC_PAGE, 30).until(EC.visibility_of_element_located((By.ID, "imgCaptcha_" + captcha_id)))

            TOPIC_PAGE.find_element(By.ID, "txtCaptcha_" + captcha_id).send_keys(captchas_intercepted.pop())

            TOPIC_PAGE.find_element(By.ID, "btnCaptcha_" + captcha_id).click()

            WebDriverWait(TOPIC_PAGE, 30).until(EC.visibility_of_element_located((By.XPATH, f"//div[@id='result_{captcha_id}']/pre")))

            post_text = TOPIC_PAGE.find_element(By.XPATH, f"//div[@id='result_{captcha_id}']/pre").text

            array_text = post_text.split("\n")
            array_text = list(filter(('').__ne__, array_text))

            for line in array_text:
                print(line)

        else:
            continue


if __name__ == '__main__':

    START_URL = "https://www.exvagos2.com/usercp.php"

    try:

        DRIVER = create_driver()
        DRIVER.get(START_URL)
        DRIVER.response_interceptor = captcha_interceptor

        iniciar_sesion(DRIVER)

        updated_topic_links = get_updatedtopics(DRIVER)

        for link in updated_topic_links:
            get_dowloadlinks(DRIVER, link)

    finally:
        DRIVER.delete_all_cookies()
        DRIVER.quit()
        print("Chrome cerrado")
