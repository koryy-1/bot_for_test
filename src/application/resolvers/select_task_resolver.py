import os
from selenium.webdriver.common.by import By
from src.application.resolvers.resolver import ResolverInterface
from src.application.utils import is_images_equal
from src.application.browser import Browser
from src.domen.constants import (
    text_sel_xp1,
    text_sel_xp2,
    answer_sel_xp1,
    answer_sel_xp2,
)
from src.domen.models.task import Task


class SelectTaskResolver(ResolverInterface):
    def __init__(self, browser: Browser):
        self.browser = browser

        # TODO: getter/setter
        self.task: Task

    def resolve(self, task: Task):
        self.task = task
        self.text_sel_xp1: str = text_sel_xp1
        self.text_sel_xp2: str = text_sel_xp2
        self.answer_sel_xp1: str = answer_sel_xp1
        self.answer_sel_xp2: str = answer_sel_xp2

        answer = task.select_type_answer.values
        quantity_ans = task.select_type_answer.quantity_ans
        if task.select_type_answer.text_sel_xp1 is not None:
            # print("menyaem xpath v sel")
            self.text_sel_xp1 = task.select_type_answer.text_sel_xp1
            self.text_sel_xp2 = task.select_type_answer.text_sel_xp2
            self.answer_sel_xp1 = task.select_type_answer.answer_sel_xp1
            self.answer_sel_xp2 = task.select_type_answer.answer_sel_xp2

        for i in range(len(answer)):
            for j in range(len(answer)):
                if not self.browser.xpath_exist(
                    self.text_sel_xp1 + str(i + 1) + self.text_sel_xp2
                ):
                    return True

                quest = self.browser.webdriver.find_element(
                    By.XPATH, self.text_sel_xp1 + str(i + 1) + self.text_sel_xp2
                ).text

                if (answer[j].line.endswith(".png")) or (
                    answer[j].line.endswith(".gif")
                ):
                    img_xpath = self.text_sel_xp1 + str(i + 1) + self.text_sel_xp2
                    img_el = self.browser.webdriver.find_element(By.XPATH, img_xpath)
                    img_url = img_el.get_attribute("src")
                    print(img_url)
                    file = self.browser.download_pict(None, img_url)
                    if not file:
                        return False

                    if is_images_equal(file, answer[j].line):
                        print("sravnil pole otveta")

                        for k in range(quantity_ans):
                            ans_xpath = f"{self.answer_sel_xp1 + str(i+1) + self.answer_sel_xp2 + str(k+1)}]"

                            if (
                                self.browser.webdriver.find_element(
                                    By.XPATH, ans_xpath
                                ).text
                                == answer[j].ans
                            ):
                                select_el = self.browser.webdriver.find_element(
                                    By.XPATH, ans_xpath
                                )
                                self.browser.webdriver.execute_script(
                                    "arguments[0].setAttribute('selected','selected')",
                                    select_el,
                                )
                                break
                    os.remove(file)

                elif (
                    (quest.find(answer[j].line) != -1)
                    and not task.question.is_exact_answer
                ) or ((quest == answer[j].line) and task.question.is_exact_answer):
                    for k in range(quantity_ans):
                        ans_xpath = f"{self.answer_sel_xp1 + str(i+1) + self.answer_sel_xp2 + str(k+1)}]"

                        if (
                            self.browser.webdriver.find_element(
                                By.XPATH, ans_xpath
                            ).text
                            == answer[j].ans
                        ):
                            select_el = self.browser.webdriver.find_element(
                                By.XPATH, ans_xpath
                            )
                            self.browser.webdriver.execute_script(
                                "arguments[0].setAttribute('selected','selected')",
                                select_el,
                            )
                            break

        return True
