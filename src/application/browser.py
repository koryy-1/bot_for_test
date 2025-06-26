import os
import time
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

from src.application.utils import log_errors
from src.domen.constants import link_xp


class Browser:
    def __init__(self):
        # хидер используется для отдельного скачивания файлов, если браузером скачать нельзя
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
            "Connection": "keep-alive",
            "Cookie": None,
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        }

        self.webdriver = self.get_webdriver()
        self.update_headers()

    def __del__(self):
        self.webdriver.quit()

    def get_webdriver(self) -> webdriver.Firefox:
        options = webdriver.FirefoxOptions()
        options.set_preference("dom.webdriver.enabled", False)
        options.set_preference("dom.webnotifications.enabled", False)
        options.set_preference(
            "general.useragent.override",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        )
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.manager.showWhenStarting", False)
        options.set_preference("browser.download.dir", os.getcwd())
        options.set_preference(
            "browser.helperApps.neverAsk.saveToDisk", "image/png, image/gif"
        )

        # options.headless = True

        return webdriver.Firefox(options=options)

    def update_headers(self):
        cookie = self.webdriver.get_cookies()
        moodle_cookie = cookie[0]["name"] + "=" + cookie[0]["value"]
        print(moodle_cookie)
        self.headers["Cookie"] = moodle_cookie

    # функция проверяет существование xpath в странице
    def xpath_exist(self, xpath):
        try:
            self.webdriver.find_element(By.XPATH, xpath)
            return True
        except Exception:
            return False

    def refresh_browser(self):
        # xpath = '/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[2]/input'
        # xpath1 = '/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[2]/input[2]'

        id1 = "mod_quiz-prev-nav"
        id2 = "mod_quiz-next-nav"
        el_class = "btn-secondary"
        try:
            if (self.webdriver.current_url.replace("#", "")[-2:] == "39") or (
                self.webdriver.current_url.replace("#", "")[-2:] == "49"
            ):
                self.webdriver.find_element(By.ID, id1).click()
                time.sleep(0.5)
                self.webdriver.find_element(By.ID, id2).click()
                time.sleep(0.5)
            else:
                self.webdriver.find_element(By.ID, id2).click()
                time.sleep(0.5)
                self.webdriver.find_element(By.ID, id1).click()
                time.sleep(0.5)
        except Exception:
            print(self.webdriver.find_element(By.CLASS_NAME, el_class).text)
            if (
                self.webdriver.find_element(By.CLASS_NAME, el_class).text
                == "Вернуться к попытке"
            ):
                self.webdriver.find_element(By.CLASS_NAME, el_class).click()

    # TODO: refactor
    def download_pict(self, pict_xpath, img_url):
        # print(img_url)
        if pict_xpath:
            img_el = self.webdriver.find_element(By.XPATH, pict_xpath)
            img_url = img_el.get_attribute("src")
        if img_url is None:
            cur_url = self.webdriver.current_url
            r = requests.get(cur_url, headers=self.headers, verify=False)
            # print(r.text)

            soup = BeautifulSoup(r.text, "html.parser")

            div = soup.find("div", {"class": "qtext"})
            img_url = div.find("img")["src"]
            # print(img_url)

        list_of_files = os.listdir(os.getcwd())
        for file in list_of_files:
            if (file.endswith(".png")) or (file.endswith(".gif")):
                print("est neudalennaya kartinka")
                print(file)
                os.remove(file)

        # img-responsive atto_image_button_text-bottom
        # img-responsive atto_image_button_text-bottom

        if not self.xpath_exist(link_xp + "/a"):
            el = self.webdriver.find_element(By.XPATH, link_xp)
            # browser.execute_script(
            # "arguments[0].appendChild(arguments[1]);", el, "<a href='URL'>открыть</a>")
            self.webdriver.execute_script(
                "arguments[0].appendChild(document.createElement('a'));", el
            )
        element = self.webdriver.find_element(By.XPATH, link_xp + "/a")

        self.webdriver.execute_script(
            f"arguments[0].setAttribute('href','{img_url}')", element
        )
        self.webdriver.execute_script(
            "arguments[0].setAttribute('download','current_pict.png')", element
        )
        time.sleep(0.2)
        self.webdriver.execute_script("arguments[0].click();", element)
        # element.click()
        time.sleep(1)

        for file in os.listdir(os.getcwd()):
            if (file.endswith(".png")) or (file.endswith(".gif")):
                print(file)
                return file

        # TODO: передавать логгер (видимо с помощью DI)
        log_errors("file ne ska4alsya")
        # TODO: raise Exception()
        return False

    def switch_to_window(self, window_num):
        window_handles = self.webdriver.window_handles
        print(window_handles)
        if len(window_handles) == 2:
            self.webdriver.switch_to.window(window_handles[window_num])

    def ensure_other_windows_closed(self):
        if len(self.webdriver.window_handles) == 2:
            self.webdriver.close()
            self.webdriver.switch_to.window(self.webdriver.window_handles[0])
