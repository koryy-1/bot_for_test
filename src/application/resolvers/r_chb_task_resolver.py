import os
import time
from selenium.webdriver.common.by import By

from src.application.utils import is_images_equal, log_errors
from src.application.resolvers.resolver import ResolverInterface
from src.application.browser import Browser
from src.domen.constants import text_xp1, text_xp2, answer_xp1, answer_xp2
from src.domen.models.task import Task


class RadioChbTaskResolver(ResolverInterface):
    def __init__(self, browser: Browser):
        self.browser = browser

        # TODO: getter/setter
        self.task: Task

    def resolve(self, task: Task):
        self.task = task
        self.text_xp1: str = text_xp1
        self.text_xp2: str = text_xp2
        self.answer_xp1: str = answer_xp1
        self.answer_xp2: str = answer_xp2

        if task.radio_checkbox_type_answer.text_xp1 != "default":
            # print("menyaem xpath v radio chb")
            self.text_xp1 = task.radio_checkbox_type_answer.text_xp1
            self.text_xp2 = task.radio_checkbox_type_answer.text_xp2
            self.answer_xp1 = task.radio_checkbox_type_answer.answer_xp1
            self.answer_xp2 = task.radio_checkbox_type_answer.answer_xp2

        i = 0
        if (task.radio_checkbox_type_answer.value.endswith(".png")) or (
            task.radio_checkbox_type_answer.value.endswith(".gif")
        ):
            while self.browser.xpath_exist(self.text_xp1 + str(i + 1) + self.text_xp2):
                img_xpath = self.text_xp1 + str(i + 1) + self.text_xp2
                img_el = self.browser.webdriver.find_element(By.XPATH, img_xpath)
                img_url = img_el.get_attribute("src")
                print(img_url)
                file = self.browser.download_pict(None, img_url)
                if not file:
                    return False
                ans_xpath = self.answer_xp1 + str(i + 1) + self.answer_xp2
                answer = self.browser.webdriver.find_element(By.XPATH, ans_xpath)
                self.browser.webdriver.execute_script(
                    "arguments[0].removeAttribute('checked')", answer
                )

                if is_images_equal(file, task.radio_checkbox_type_answer.value):
                    answer.click()
                    time.sleep(1)
                    os.remove(file)
                    return True
                else:
                    time.sleep(1)
                    os.remove(file)
                # 	browser.execute_script("arguments[0].removeAttribute('checked')", answer)

                i += 1
        else:
            while self.browser.xpath_exist(self.text_xp1 + str(i + 1) + self.text_xp2):
                print(
                    self.browser.webdriver.find_element(
                        By.XPATH, self.text_xp1 + str(i + 1) + self.text_xp2
                    ).text
                )
                if (
                    self.browser.webdriver.find_element(
                        By.XPATH, self.text_xp1 + str(i + 1) + self.text_xp2
                    ).text
                    == task.radio_checkbox_type_answer.value
                ):
                    ans_xpath = self.answer_xp1 + str(i + 1) + self.answer_xp2
                    input_el = self.browser.webdriver.find_element(By.XPATH, ans_xpath)
                    input_el.click()
                    return True
                    # browser.execute_script("arguments[0].setAttribute('checked','checked')", answer)
                i += 1

        log_errors("otvet ne pro4elsya")
        return False
