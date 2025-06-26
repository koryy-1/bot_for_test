import os
from selenium.webdriver.common.by import By

from src.application.browser import Browser
from src.application.utils import is_images_equal, log_errors
from src.domen.constants import check_xpath_img, main_xpath, second_xpath
from src.domen.models.task import Task


class TaskSearcher:
    def __init__(self, browser: Browser):
        self.browser = browser

    def is_dl_images_equal(self, xpath_to_image, img_url, path_to_image):
        file = self.browser.download_pict(xpath_to_image, img_url)
        if not file:
            return False
        result = is_images_equal(file, path_to_image)
        os.remove(file)

        if result:
            return True
        else:
            return False

    def get_valid_xpath_to_quest(
        self, xpath_to_question, const_xpath_to_quest, index_for_quest_text
    ):
        if xpath_to_question == "default":
            # print('xpath ne nujno menyat')
            xpath = f"{const_xpath_to_quest + str(index_for_quest_text)}]"
        else:
            # print('menyaem xpath')
            xpath = xpath_to_question
            # print(xpath)

        if not self.browser.xpath_exist(xpath):
            return None

        return xpath

    def search(self, tasks: list[Task]):
        index_for_quest_text = 1
        img_url = None

        if self.browser.xpath_exist(check_xpath_img):
            img_el = self.browser.webdriver.find_element(By.XPATH, check_xpath_img)
            img_url = img_el.get_attribute("src")
            index_for_quest_text += 1

        for task in tasks:
            # идет сравнение в несколько этапов
            # сначала сверяется 1 элемент с текстом вопроса, потом 2 элемент
            # если сверяется картинка то item определяется однозначно

            quest_text = task.question

            xpath = self.get_valid_xpath_to_quest(
                quest_text.main_xpath, main_xpath, index_for_quest_text
            )
            if xpath is None:
                continue

            ###
            # кейс, если путь до картинки прописан в поле,
            # который предназначен для текста вопроса
            if (quest_text.first_line.endswith(".png")) or (
                quest_text.first_line.endswith(".gif")
            ):
                is_equal = self.is_dl_images_equal(
                    xpath, img_url, quest_text.first_line
                )
                if is_equal:
                    return task
                else:
                    continue
            ###

            question = self.browser.webdriver.find_element(By.XPATH, xpath).text
            print(quest_text.first_line)
            # print(question)

            # is_exact_quest если проставлен, то идет сравнение всей строки с вопросом,
            # если не проставлен то идет сравнение только подстроки в строке с вопросом
            if not (
                (
                    (question.find(quest_text.first_line) != -1)
                    and not task.question.is_exact_quest
                )
                or (
                    (question == quest_text.first_line) and task.question.is_exact_quest
                )
            ):
                continue

            if quest_text.second_line == "nothing":
                return task

            xpath = self.get_valid_xpath_to_quest(
                quest_text.second_xpath, second_xpath, index_for_quest_text
            )
            if xpath is None:
                continue

            # TODO: крч если нашелся missing_xp на странице, то скипает вопрос (гавно)
            if quest_text.missing is not None:
                if self.browser.xpath_exist(quest_text.missing_xp):
                    missing_part_q = self.browser.webdriver.find_element(
                        By.XPATH, quest_text.missing_xp
                    ).text
                    if missing_part_q.find(quest_text.missing) != -1:
                        continue

            # такой же кейс с картинкой
            if (quest_text.second_line.endswith(".png")) or (
                quest_text.second_line.endswith(".gif")
            ):
                is_equal = self.is_dl_images_equal(
                    xpath, img_url, quest_text.second_line
                )
                if is_equal:
                    return task
                else:
                    continue

            question = self.browser.webdriver.find_element(By.XPATH, xpath).text
            if question.find(quest_text.second_line) != -1:
                return task

        log_errors("vopros ne nawelsya")
        return None
