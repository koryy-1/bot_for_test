import random
import time
from PIL import Image, ImageChops
from urllib import parse
import config

LOGIN = ""
PASSWORD = ""
PAGE = 0


def build_url(base_url, query_params):
    # Returns a list in the structure of urlparse.ParseResult
    url_parts = list(parse.urlparse(base_url))
    url_parts[4] = parse.urlencode(query_params)
    return parse.urlunparse(url_parts)


def remove_query_param(url: str, param: str) -> str:
    queries = dict(parse.parse_qsl(parse.urlsplit(url).query))
    queries.pop(param, None)
    return build_url(url, queries)


def set_page_param(url: str, page_num: int) -> str:
    queries = dict(parse.parse_qsl(parse.urlsplit(url).query))
    queries["page"] = str(page_num)
    return build_url(url, queries)


def is_images_equal(file, pict_path):
    img1 = Image.open(file)
    img2 = Image.open(config.pictures_path + pict_path)
    try:
        differences = ImageChops.difference(img1, img2)
        if differences.getbbox() is None:
            return True

    except Exception as e:
        print(e)

    return False


# TODO: remake
def log_errors(msg):
    print(msg)
    with open("logs.log", "a", encoding="utf-8") as file:
        file.write(
            LOGIN
            + " "
            + PASSWORD
            + "\t"
            + "ошибка в "
            + str(PAGE)
            + " номере: "
            + msg
            + "\n"
        )


def sleep_random_by_task_format(task_format):
    if task_format == "radio checkbox":
        time.sleep(60 * random.randrange(5, 15))
    elif task_format == "checkbox":
        time.sleep(60 * random.randrange(10, 25))
    elif task_format == "select":
        time.sleep(60 * random.randrange(20, 35))
    elif task_format == "drag&drop":
        time.sleep(60 * random.randrange(15, 35))
    elif task_format == "input":
        time.sleep(60 * random.randrange(10, 40))
