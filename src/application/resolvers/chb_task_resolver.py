import os
from selenium.webdriver.common.by import By

from src.application.utils import is_images_equal
from src.application.resolvers.resolver import ResolverInterface
from src.application.browser import Browser
from src.domen.constants import (
    text_chb_xp1,
    text_chb_xp2,
    answer_chb_xp1,
    answer_chb_xp2,
    second_xpath,
)
from src.domen.models.task import Task


class ChbTaskResolver(ResolverInterface):
    def __init__(self, browser: Browser):
        self.browser = browser

        # TODO: getter/setter
        self.task: Task

    def resolve(self, task: Task):
        self.task = task
        self.text_chb_xp1: str = text_chb_xp1
        self.text_chb_xp2: str = text_chb_xp2
        self.answer_chb_xp1: str = answer_chb_xp1
        self.answer_chb_xp2: str = answer_chb_xp2

        if task.checkbox_type_answer.text_chb_xp1 != "default":
            print("menyaem xpath v chb")
            self.text_chb_xp1 = task.checkbox_type_answer.text_chb_xp1
            self.text_chb_xp2 = task.checkbox_type_answer.text_chb_xp2
            self.answer_chb_xp1 = task.checkbox_type_answer.answer_chb_xp1
            self.answer_chb_xp2 = task.checkbox_type_answer.answer_chb_xp2

        i = 0

        second_xpath_type1 = f"{second_xpath}3]"

        if task.checkbox_type_answer.is_equations:
            html_elem = self.browser.webdriver.find_element(
                By.XPATH, second_xpath_type1
            ).text
            print(html_elem)
            values_Variables = html_elem.split()
            indices_of_vars = task.checkbox_type_answer.indices_of_vars
            totals = []
            equations = task.checkbox_type_answer.equations

            print(values_Variables)
            print(equations)
            equation_values = []
            list_of_vars = list(indices_of_vars)
            print(indices_of_vars)

            for j in range(len(list_of_vars)):
                print(indices_of_vars[f"{list_of_vars[j]}"])
                equation_values.append(
                    values_Variables[indices_of_vars[f"{list_of_vars[j]}"]]
                )
            print(equation_values)

            for j in range(len(list_of_vars)):
                indices_of_vars[f"{list_of_vars[j]}"] = equation_values[j]
                print(indices_of_vars[f"{list_of_vars[j]}"])

            for j in range(len(equations)):
                totals.append("".join(equations[j].split("=")[0]))
                equations[j] = "".join(equations[j].split("=")[1])
                print(equations[j])
                for k in range(len(list_of_vars)):
                    equations[j] = equations[j].replace(
                        list_of_vars[k], indices_of_vars[f"{list_of_vars[k]}"]
                    )
                    # print(formuls[j])
            print(equations)

            for j in range(len(equations)):
                print(equations[j])
                if task.checkbox_type_answer.answer_type_var == "int":
                    equations[j] = int(eval(equations[j]))
                    print(equations[j])
                if task.checkbox_type_answer.answer_type_var == "float":
                    equations[j] = float(eval(equations[j]))
                    print(equations[j])

            while self.browser.xpath_exist(
                self.text_chb_xp1 + str(i + 1) + self.text_chb_xp2
            ):
                text_xpath = self.text_chb_xp1 + str(i + 1) + self.text_chb_xp2
                text_ans = self.browser.webdriver.find_element(
                    By.XPATH, text_xpath
                ).text

                ans_xpath = self.answer_chb_xp1 + str(i + 1) + self.answer_chb_xp2
                answer = self.browser.webdriver.find_element(By.XPATH, ans_xpath)
                self.browser.webdriver.execute_script(
                    "arguments[0].removeAttribute('checked')", answer
                )
                for j in range(len(equations)):
                    # print(str(totals[j]))
                    if (
                        text_ans.find(" " + str(equations[j])) != -1
                        and text_ans.find(totals[j]) != -1
                    ):
                        # ans_xpath = self.answer_chb_xp1 + str(i+1) + self.answer_chb_xp2
                        # answer = browser.find_element(By.XPATH, ans_xpath)
                        # browser.execute_script("arguments[0].setAttribute('type','text')", answer)
                        # time.sleep(0.2)
                        # answer.clear()
                        # answer.send_keys('1')
                        answer.click()
                        totals[j] = "00000"
                        break
                i += 1

        while self.browser.xpath_exist(
            self.text_chb_xp1 + str(i + 1) + self.text_chb_xp2
        ):
            if self.text_chb_xp2.endswith("/img") or self.browser.xpath_exist(
                self.text_chb_xp1 + str(i + 1) + self.text_chb_xp2 + "/img"
            ):
                img_xpath = self.text_chb_xp1 + str(i + 1) + self.text_chb_xp2
                if not img_xpath.endswith("/img"):
                    img_xpath = img_xpath + "/img"
                img_el = self.browser.webdriver.find_element(By.XPATH, img_xpath)
                img_url = img_el.get_attribute("src")
                print(img_url)
                file = self.browser.download_pict(None, img_url)
                if not file:
                    return False
                ans_xpath = self.answer_chb_xp1 + str(i + 1) + self.answer_chb_xp2
                answer = self.browser.webdriver.find_element(By.XPATH, ans_xpath)
                self.browser.webdriver.execute_script(
                    "arguments[0].removeAttribute('checked')", answer
                )
                for j in range(len(task.checkbox_type_answer.values)):
                    if (task.checkbox_type_answer.values[j].endswith(".png")) or (
                        task.checkbox_type_answer.values[j].endswith(".gif")
                    ):
                        if is_images_equal(file, task.checkbox_type_answer.values[j]):
                            answer.click()
                            break
                        # else:
                        # 	browser.execute_script("arguments[0].removeAttribute('checked')", answer)

                os.remove(file)

            else:
                text_xpath = self.text_chb_xp1 + str(i + 1) + self.text_chb_xp2
                print(self.browser.webdriver.find_element(By.XPATH, text_xpath).text)
                ans_xpath = self.answer_chb_xp1 + str(i + 1) + self.answer_chb_xp2
                input_el = self.browser.webdriver.find_element(By.XPATH, ans_xpath)
                self.browser.webdriver.execute_script(
                    "arguments[0].removeAttribute('checked')", input_el
                )
                for j in range(len(task.checkbox_type_answer.values)):
                    if not (
                        (task.checkbox_type_answer.values[j].endswith(".png"))
                        or (task.checkbox_type_answer.values[j].endswith(".gif"))
                    ):
                        if (
                            self.browser.webdriver.find_element(
                                By.XPATH, text_xpath
                            ).text
                            == task.checkbox_type_answer.values[j]
                        ):
                            input_el.click()
                            break

            i += 1

        return True
