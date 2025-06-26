import time

from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import src.application.utils as utils
from src.application.task_searcher import TaskSearcher
from src.application.resolvers.r_chb_task_resolver import RadioChbTaskResolver
from src.application.resolvers.chb_task_resolver import ChbTaskResolver
from src.application.resolvers.select_task_resolver import SelectTaskResolver
from src.application.resolvers.drag_drop_task_resolver import DragDropTaskResolver
from src.application.resolvers.input_task_resolver import InputTaskResolver
from src.application.reader import Reader
from src.application.browser import Browser

from src.domen.constants import (
    acc_name_xp,
    login_xpath,
    password_xpath,
    login_btn_xpath,
    login_page,
)
from src.domen.models.account import Account
from src.domen.models.task import Task


class Bot:
    def __init__(self):
        self.browser = Browser()

        # creating searcher
        self.task_searcher = TaskSearcher(self.browser)

        # creating resolvers
        self.radio_chb_task_resolver = RadioChbTaskResolver(self.browser)
        self.chb_task_resolver = ChbTaskResolver(self.browser)
        self.select_task_resolver = SelectTaskResolver(self.browser)
        self.drag_drop_task_resolver = DragDropTaskResolver(self.browser)
        self.input_task_resolver = InputTaskResolver(self.browser)

    def resolve_concrete_task(self, task: Task):
        if task.format == "radio checkbox":
            return self.radio_chb_task_resolver.resolve(task)
        elif task.format == "checkbox":
            return self.chb_task_resolver.resolve(task)
        elif task.format == "select":
            return self.select_task_resolver.resolve(task)
        elif task.format == "drag&drop":
            return self.drag_drop_task_resolver.resolve(task)
        elif task.format == "input":
            return self.input_task_resolver.resolve(task)

    def resolve(
        self,
        tasks,
    ):
        task = self.task_searcher.search(tasks)
        if task is None:
            return None

        self.resolve_concrete_task(task)
        return task["format"]

    # TODO: то что про вход в аккаунт пойдет в auth_service который будет принимать в себя браузер
    def authenticate(self, account: Account):
        # TODO: создать обертки для find_element(By.XPATH
        self.browser.webdriver.find_element(By.XPATH, login_xpath).send_keys(
            account.login
        )

        self.browser.webdriver.find_element(By.XPATH, password_xpath).send_keys(
            account.password
        )

        self.browser.webdriver.find_element(By.XPATH, login_btn_xpath).click()

    def is_authenticated(self):
        if self.browser.xpath_exist(acc_name_xp):
            acc_name = self.browser.webdriver.find_element(By.XPATH, acc_name_xp).text
            print("bot logined by name: " + acc_name)
            return True
        return False

    # refactor
    def logout(self):
        # browser.find_element(By.XPATH, context_menu_logout_xp).click()
        # time.sleep(1)
        # browser.find_element(By.XPATH, logout_xpath).click()
        # time.sleep(3)
        if self.check_logout():
            return

        text_html = self.browser.webdriver.page_source
        soup = BeautifulSoup(text_html, "html.parser")

        logout_el = soup.find("a", {"data-title": "logout,moodle"})
        if logout_el is None:
            raise Exception()

        self.browser.webdriver.get(logout_el.get("href"))

    def check_logout(self):
        if self.browser.webdriver.current_url == login_page:
            utils.log_errors("kto-to vowel v acc")
            return True
        return False

    def start_test(self):
        if self.browser.xpath_exist("//button[text()='Начать тестирование']"):
            WebDriverWait(self.browser.webdriver, 5).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[text()='Начать тестирование']")
                )
            ).click()
        elif self.browser.xpath_exist(
            '//button[text()="Продолжить последнюю попытку"]'
        ):
            WebDriverWait(self.browser.webdriver, 5).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[text()='Продолжить последнюю попытку']")
                )
            ).click()
        elif self.browser.xpath_exist('//button[text()="Пройти тест заново"]'):
            WebDriverWait(self.browser.webdriver, 5).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[text()='Пройти тест заново']")
                )
            ).click()
        else:
            print("ne nawel knopku testa")
        time.sleep(1)

    def goto_page(self, page_num):
        url = self.browser.webdriver.current_url
        new_url = utils.set_page_param(url, page_num)
        self.browser.webdriver.get(new_url)

    def goto_first_page(self):
        url = self.browser.webdriver.current_url
        new_url = utils.remove_query_param(url, "page")
        self.browser.webdriver.get(new_url)

    def goto_next_task(self):
        id = "mod_quiz-next-nav"
        self.browser.webdriver.find_element(By.ID, id).click()
        time.sleep(1)

    def execute_command(self, raw_command: str):
        if raw_command.split() == []:
            return
        command = raw_command.split()[0]
        args = raw_command.split()[1:]

        if command == "urlparse":
            # просто проверяет корректное удаление page из урл
            # нужно для перехода на 1 вопрос теста
            url = self.browser.webdriver.current_url
            new_url = utils.remove_query_param(url, "page")
            print("new url: ", new_url)
        elif command == "gotopage":
            # проверяет корректный переход на определенную страницу
            self.goto_page(int(args[1]))
        elif command == "swto":
            self.browser.webdriver.switch_to.window(
                self.browser.webdriver.window_handles[int(args[1])]
            )
        elif command == "help":
            print(
                "xpexist - 4ekaet suwestvyet li xpath na stranice",
                "resolveq - probuet rewit tekuwiy vopros",
            )
        elif command == "xpex":
            print(self.browser.xpath_exist(args[1]))
        elif command == "resq":
            tasks = Reader.get_data_for_test()
            self.resolve(tasks)
        else:
            print('unknown command, type "help" for more info')
