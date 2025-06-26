import json
import config
from src.domen.models.account import Account
from src.domen.models.task import Task


# да это должно быть в 3 слое infrastructure
# и должно инжектиться в другие зависимости через DI, но пока так
class Reader:
    def get_data_for_test(self) -> list[Task]:
        # TODO: parse to list[Model]
        with open(config.test_data_file, "r", encoding="utf-8") as file:
            data = json.load(file)
        tasks = [Task.model_validate(task) for task in data["questions"]]
        return tasks

    def get_accounts(self) -> list[Account]:
        with open(config.accounts_file, "r", encoding="utf-8") as file:
            return self.parse_accounts(file)

    def parse_accounts(self, file):
        accounts: list[Account] = []
        for line in file:
            cred_list = line.replace("\n", "").split(None, 1)
            account = Account(cred_list[0], cred_list[1])
            accounts.append(account)
        return accounts
