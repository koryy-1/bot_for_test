import time
import urllib3
import config

from src.application.reader import Reader

from src.application.utils import sleep_random_by_task_format
from src.application.bot import Bot


def run_test():
    # goto default page https://eios.sibsutis.ru/

    # for acc in accs:
    #    login()
    #    start_test()
    #    for i in range(40):
    #       bot.resolve(data)
    #       goto_next_task()
    #    logout()

    bot = Bot()

    accounts = Reader.get_accounts()

    bot.browser.webdriver.get("https://eios.sibsutis.ru/")
    # TODO: вместо sleep использовать WebDriverWait
    time.sleep(1)

    for account in accounts:
        bot.authenticate(account)
        time.sleep(1)
        bot.is_authenticated()

        # TODO: то есть при каждом переходе на страницу (не важно по кнопке или через browser.get())
        # вызывать check_logout()
        # получается это надо выносить в отдельную функцию
        if bot.check_logout():
            continue

        bot.browser.update_headers()

        bot.browser.webdriver.get(config.url_test)
        time.sleep(1)

        if bot.check_logout():
            continue

        bot.start_test()

        bot.browser.switch_to_window(1)

        bot.goto_first_page()
        time.sleep(1)

        if bot.check_logout():
            continue

        tasks = Reader.get_data_for_test()

        for _ in range(40):
            task_format = bot.resolve(tasks)
            if config.is_set_delay_between_tasks:
                sleep_random_by_task_format(task_format)
            bot.goto_next_task()

        # TODO: use logger
        print("test finished for account ()")

        bot.browser.ensure_other_windows_closed()

        bot.logout()

        # TODO: вместо таймингов просто условия + ожидания когда появятся ключевые элементы,
        # по которым можно сориентироваться что селениум щас на правильной странице
        # (мб юзать WebDriverWait)
        time.sleep(4)

    print("bot resolving finished")


# TODO: эта функция пойдет в 4 слой CLI
def run_command_execution():
    bot = Bot()
    while True:
        command = input("cmd >")
        if command == "exit":
            break

        try:
            bot.execute_command(command)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    urllib3.disable_warnings()

    if config.mode == "test run":
        run_test()

    if config.mode == "commands execution":
        run_command_execution()
