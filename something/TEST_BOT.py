import time
import os
import shutil
# from selenium import webdriver
# import requests
from PIL import Image, ImageChops
import json
import math
import random


# with open('questions_for_4_test.json', 'r', encoding='utf-8') as file:
# 	data = json.load(file)
# main_xpath = data['type1']['main_xpath']
# print(main_xpath)
# i = 1
# if (data['type1']['questions'][i]['quest_text']['main_xpath'] == 'default'):
# 	print(data['type1']['questions'][i]['quest_text']['main_xpath'])
# 	print('vse norm')
# else:
# 	print('menyaem xpath')
# 	main_xpath = data['type1']['questions'][i]['quest_text']['main_xpath']
# 	print(main_xpath)

# i = 0
# for item in data['type1']['questions']:
# 	print(item)
# 	quest_text = item['quest_text']
# 	break

# if isinstance(item['answer'], str):
# 	print('Да, это строка')
# if isinstance(item['answer'], list):
# 	print('это spisok')
# if isinstance(item['answer'], dict):
# 	print('это object')

# answer = [8, 4, 0, 4, 0, 4,
# 		0, 0, 6, 6, 0, 0,
# 		3, 3, 0, 6, 0, 6,
# 		0, 0, 0, 3, 3, 0,
# 		5, 7, 6, 1, 3, -2]
# for i in range(len(answer)):
# 	print(answer[i])

print(random.randrange(20, 40))