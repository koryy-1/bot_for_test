import os
import time
from selenium.webdriver.common.by import By

from src.application.resolvers.resolver import ResolverInterface
from src.application.utils import is_images_equal, log_errors
from src.application.browser import Browser
from src.domen.constants import array_xpath, answer_xpath
from src.domen.models.task import Task


class DragDropTaskResolver(ResolverInterface):
    def __init__(self, browser: Browser):
        self.browser = browser

        # TODO: getter/setter
        self.task: Task
        self.array_xp: str = array_xpath
        self.answer_xp: str = answer_xpath

    def resolve(self, task: Task):
        self.task = task
        self.array_xp = array_xpath
        self.answer_xp = answer_xpath

        if task.drag_drop_type_answer.array_xp1 is not None:
            # TODO: прочекать правильность
            array_xp1 = task.drag_drop_type_answer.array_xp1
            array_xp2 = task.drag_drop_type_answer.array_xp2

        # TODO: кейс покрывает только 9 тест
        if task.drag_drop_type_answer.answer_xp != "default":
            self.array_xp = task.drag_drop_type_answer.array_xp
            self.answer_xp = task.drag_drop_type_answer.answer_xp

        # очищение дефолтных ответов
        ################
        # for k in range(len(item['answer'])):
        # ans_xpath = f'{self.answer_xp + str(k+2)}]'

        # if (item['answer'][0].endswith('.png')) or (item['answer'][0].endswith('.gif')):
        # ans_xpath = f'{self.answer_xp + str(k+1)}]'

        # input_el = browser.find_element(By.XPATH, ans_xpath)
        # browser.execute_script("arguments[0].setAttribute('type','text')", input_el)
        # print('opened', k+1, 'input for clearing')
        # time.sleep(0.2)
        # input_el.clear()
        # input_el.send_keys(0)

        # time.sleep(0.5)
        # refresh_browser()
        # time.sleep(1)
        ################

        # TODO: проверить правильность
        if task.drag_drop_type_answer.array2_xp != "":
            ans_row1 = []
            j = 2
            while self.browser.xpath_exist(f"{self.array_xp + str(j)}]"):
                el = self.browser.webdriver.find_element(
                    By.XPATH, f"{self.array_xp + str(j)}]"
                ).text
                if el[0] == "‑":  # тире это не минус
                    el = "-" + el[1:]
                ans_row1.append(el)
                # time.sleep(0.1)
                j += 2
            print(ans_row1)

        elif task.drag_drop_type_answer.multiple_arrays != 0:
            main_ans_row = {}
            for i in range(task.drag_drop_type_answer.multiple_arrays):
                ans_row = []
                j = 2
                while self.browser.xpath_exist(
                    f"{array_xp1 + str(i+1) + array_xp2 + str(j)}]"
                ):
                    el = self.browser.webdriver.find_element(
                        By.XPATH, f"{array_xp1 + str(i+1) + array_xp2 + str(j)}]"
                    ).text
                    if el[0] == "‑":  # тире это не минус
                        el = "-" + el[1:]
                    ans_row.append(el)
                    # time.sleep(0.1)
                    j += 2
                print(ans_row)
                array_el = self.browser.webdriver.find_element(
                    By.XPATH, f"{array_xp1 + str(i+1)}]"
                )
                num_ar = array_el.get_attribute("class")[-1]
                main_ans_row[f"{num_ar}"] = ans_row
            print(main_ans_row)

        elif (task.drag_drop_type_answer.values[0].endswith(".png")) or (
            task.drag_drop_type_answer.values[0].endswith(".gif")
        ):
            time.sleep(1)

            img_urls = []
            j = 2
            while self.browser.xpath_exist(f"{self.array_xp + str(j)}]"):
                el = self.browser.webdriver.find_element(
                    By.XPATH, f"{self.array_xp + str(j)}]"
                ).get_attribute("src")
                print(el)
                img_urls.append(el)
                # time.sleep(0.1)
                j += 2
            print(img_urls)

        else:
            ans_row = []
            j = 2
            while self.browser.xpath_exist(f"{self.array_xp + str(j)}]"):
                el = self.browser.webdriver.find_element(
                    By.XPATH, f"{self.array_xp + str(j)}]"
                ).text
                print(el)
                if el[0] == "‑":  # тире это не минус
                    el = "-" + el[1:]
                ans_row.append(el)
                # time.sleep(0.1)
                j += 2
            print(ans_row)

        if (task.drag_drop_type_answer.values[0].endswith(".png")) or (
            task.drag_drop_type_answer.values[0].endswith(".gif")
        ):
            i = 0
            for j in range(len(img_urls)):
                file = self.browser.download_pict(None, img_urls[j])
                if not file:
                    return False
                for k in range(len(task.drag_drop_type_answer.values)):
                    if is_images_equal(file, task.drag_drop_type_answer.values[k]):
                        ans_xpath = f"{self.answer_xp + str(i+1)}]"
                        input_el = self.browser.webdriver.find_element(
                            By.XPATH, ans_xpath
                        )
                        self.browser.webdriver.execute_script(
                            "arguments[0].setAttribute('type','text')", input_el
                        )
                        # print('opened', k+1, 'input for clearing')
                        time.sleep(0.2)
                        input_el.clear()
                        input_el.send_keys(j + 1)
                        print(img_urls[j])
                        i += 1
                        break

                os.remove(file)

        for k in range(len(task.drag_drop_type_answer.values)):
            ans_xpath = f"{self.answer_xp + str(k+2)}]"

            if (task.drag_drop_type_answer.values[0].endswith(".png")) or (
                task.drag_drop_type_answer.values[0].endswith(".gif")
            ):
                # ans_xpath = f'{self.answer_xp + str(k+1)}]'
                break

            input_el = self.browser.webdriver.find_element(By.XPATH, ans_xpath)
            self.browser.webdriver.execute_script(
                "arguments[0].setAttribute('type','text')", input_el
            )
            # print('opened', k+1, 'input for clearing')
            time.sleep(0.2)
            input_el.clear()

            # TODO: проверить правильность
            if task.drag_drop_type_answer.array2_xp != "":
                if task.drag_drop_type_answer.values[k] in ans_row:
                    input_el.send_keys(
                        ans_row.index(task.drag_drop_type_answer.values[k]) + 1
                    )

                elif task.drag_drop_type_answer.values[k] in ans_row1:
                    input_el.send_keys(
                        ans_row1.index(task.drag_drop_type_answer.values[k]) + 1
                    )

                else:
                    log_errors("elem in arrays not found")

            elif task.drag_drop_type_answer.multiple_arrays != 0:
                num_ar = input_el.get_attribute("class")[-1]
                # for j in range(len(main_ans_row)):

                if task.drag_drop_type_answer.values[k] in main_ans_row[f"{num_ar}"]:
                    input_el.send_keys(
                        main_ans_row[f"{num_ar}"].index(
                            task.drag_drop_type_answer.values[k]
                        )
                        + 1
                    )
                else:
                    log_errors(
                        f"elementa {task.drag_drop_type_answer.values[k]} net v nujnom massive"
                    )

            else:
                input_el.send_keys(
                    ans_row.index(task.drag_drop_type_answer.values[k]) + 1
                )

        return True
