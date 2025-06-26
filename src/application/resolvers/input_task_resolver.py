import re
from selenium.webdriver.common.by import By

from src.application.resolvers.resolver import ResolverInterface
from src.application.browser import Browser
from src.domen.constants import answer_inp_xpath, string_xpath
from src.domen.models.task import Task


class InputTaskResolver(ResolverInterface):
    def __init__(self, browser: Browser):
        self.browser = browser

        # TODO: getter/setter
        self.task: Task
        self.answer_inp_xp: str = answer_inp_xpath
        self.string_xpath: str = string_xpath

    def resolve(self, task: Task):
        self.task = task
        self.answer_inp_xp = answer_inp_xpath
        self.string_xpath = string_xpath

        if task.input_type_answer.answer_inp_xp != "default":
            print("menyaem xpath v chb")
            self.answer_inp_xp = task.input_type_answer.answer_inp_xp

        # if item["answer"] == "skip":
        #     print("skip")
        #     return True

        elif task.input_type_answer.is_equations:
            if task.input_type_answer.string_xpath is not None:
                print("menyaem xpath v chb")
                self.string_xpath = task.input_type_answer.string_xpath

            html_elem = self.browser.webdriver.find_element(
                By.XPATH, self.string_xpath
            ).text
            print(html_elem)
            values_Variables = html_elem.split()
            indices_of_vars = task.input_type_answer.indices_of_vars
            totals = []
            equations = task.checkbox_type_answer.equations

            print(values_Variables)
            print(equations)
            equation_values: list[str] = []
            list_of_vars = list(indices_of_vars)
            print(indices_of_vars)

            for j in range(len(list_of_vars)):
                print(indices_of_vars[f"{list_of_vars[j]}"])
                # получаем индекс который будем юзать для спаршенной строки
                index = indices_of_vars[f"{list_of_vars[j]}"]
                if task.checkbox_type_answer.answer_type_var == "float":
                    equation_values.append(values_Variables[index].replace(",", "."))
                else:
                    equation_values.append(values_Variables[index])
            print(equation_values)

            new_dict_of_indexes = {}

            ########################
            # TODO: гавно
            for j in range(len(list_of_vars)):
                if (
                    task.input_type_answer.need_exact_value is not None
                    and task.input_type_answer.need_exact_value != []
                ):
                    for k in range(len(task.input_type_answer.need_exact_value)):
                        if (
                            task.input_type_answer.need_exact_value[k].var
                            == indices_of_vars[f"{list_of_vars[j]}"]
                        ) or (
                            task.input_type_answer.need_exact_value[k].var
                            == list_of_vars[j]
                        ):
                            # слайсим число нужной нам строки
                            # if 'start' in item['need_exact_value'][k]:

                            temp = re.findall(
                                "[-+]?(?:\\d+(?:\\.\\d*)?|\\.\\d+)",
                                equation_values[j].replace(",", "."),
                            )

                            equation_values[j] = temp[
                                task.input_type_answer.need_exact_value[k].idx
                            ]

                            # values[j] = values[j][item['need_exact_value'][k]['start']
                            # :item['need_exact_value'][k]['end']]
                            # слайсим до определенного символа
                            # elif 'slice_to' in item['need_exact_value'][k]:
                            # 	values[j] = ''.join(values[j].split(item['need_exact_value'][k]['slice_to'])
                            # [item['need_exact_value'][k]['ind']])
                            # print(values[j])
                if equation_values[j].endswith(",") or equation_values[j].endswith("."):
                    equation_values[j] = equation_values[j][:-1]
                new_dict_of_indexes[f"{list_of_vars[j]}"] = equation_values[j]
                print(new_dict_of_indexes[f"{list_of_vars[j]}"])
            ########################

            if task.input_type_answer.system_of_equations is not None:
                for j in range(
                    len(task.input_type_answer.system_of_equations.conditions)
                ):
                    temp = task.input_type_answer.system_of_equations.conditions[
                        j
                    ].replace(
                        task.input_type_answer.system_of_equations.var,
                        new_dict_of_indexes[
                            f"{task.input_type_answer.system_of_equations.var}"
                        ],
                    )
                    if eval(temp):
                        temp1 = equations[j]
                        equations.append(temp1)
                        break

            for j in range(len(equations)):
                totals.append("".join(equations[j].split("=")[0]))
                equations[j] = "".join(equations[j].split("=")[1])
                print(equations[j])
                for k in range(len(list_of_vars)):
                    equations[j] = equations[j].replace(
                        list_of_vars[k], new_dict_of_indexes[f"{list_of_vars[k]}"]
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

            if task.checkbox_type_answer.answer_type_var == "float":
                precision = 2
                if html_elem.find("десятых") != -1:
                    precision = 1
                if html_elem.find("сотых") != -1:
                    precision = 2
                if html_elem.find("тысячных") != -1:
                    precision = 3
                answer = round(equations[len(equations) - 1], precision)
            else:
                answer = equations[len(equations) - 1]

            if html_elem.find("целых") != -1:
                answer = int(
                    equations[len(equations) - 1]
                    + (0.5 if equations[len(equations) - 1] > 0 else -0.5)
                )

            answer = str(answer)

            string = answer

            answer = string.replace(".", ",")

            if (
                string.endswith(".0")
                or string.endswith(".1")
                or string.endswith(".2")
                or string.endswith(".3")
                or string.endswith(".4")
                or string.endswith(".5")
                or string.endswith(".6")
                or string.endswith(".7")
                or string.endswith(".8")
                or string.endswith(".9")
            ) and (html_elem.find("сотых") != -1):
                answer = answer + "0"

            if html_elem.find("тысячных") != -1:
                if len(string.split(".")[1]) == 1:
                    answer = answer + "00"
                elif len(string.split(".")[1]) == 2:
                    answer = answer + "0"

            print(answer)
            answer_input = self.browser.webdriver.find_element(
                By.XPATH, self.answer_inp_xp
            )
            answer_input.clear()
            answer_input.send_keys(answer)

        else:
            answer_input = self.browser.webdriver.find_element(
                By.XPATH, self.answer_inp_xp
            )
            answer_input.clear()
            answer_input.send_keys(task.input_type_answer.value)

        return True
