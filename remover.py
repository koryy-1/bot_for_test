import time
import random
import math
import re
import os
import shutil
from types import ModuleType
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import requests
from urllib import parse
import urllib3
from bs4 import BeautifulSoup
from PIL import Image, ImageChops
import json
import config

# https://eios.sibsutis.ru/mod/quiz/attempt.php?attempt=127854&cmid=55478
# print('ссылка на тест')
# link_na_test = input()

print('mode for running')
print('1 - developing')
print('2 - production')
mode = config.mode
print(mode)

option = webdriver.FirefoxOptions()
option.set_preference('dom.webdriver.enabled', False)
option.set_preference('dom.webnotifications.enabled', False)
option.set_preference('general.useragent.override', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0')
option.set_preference("browser.download.folderList",2)
option.set_preference("browser.download.manager.showWhenStarting",False)
option.set_preference("browser.download.dir", os.getcwd())
option.set_preference("browser.helperApps.neverAsk.saveToDisk", "image/png, image/gif")

# option.headless = True

urllib3.disable_warnings()



# функция проверяет существование xpath в странице
def xpath_exist(url):
	try:
		browser.find_element(By.XPATH, url)
		exist = True
	except Exception:
		exist = False
	return exist

def exit_for_prod(msg):
	if mode == '2':
		with open('logs.txt', 'a', encoding='utf-8') as file:
			file.write(msg + '\n')

def check_logout():
	if browser.current_url == 'https://eios.sibsutis.ru/login/index.php':
		print('kto-to vowel v acc')
		exit_for_prod('kto-to vowel v acc')
		return True
	else:
		return False

def refresh_browser():
	# xpath = '/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[2]/input'
	# xpath1 = '/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[2]/input[2]'


	id1 = 'mod_quiz-prev-nav'
	id2 = 'mod_quiz-next-nav'
	el_class = 'btn-secondary'
	try:
		if ((browser.current_url.replace('#', '')[-2:] == '39')
			or
			(browser.current_url.replace('#', '')[-2:] == '49')):
			browser.find_element(By.ID, id1).click()
			time.sleep(0.5)
			browser.find_element(By.ID, id2).click()
			time.sleep(0.5)
		else:
			browser.find_element(By.ID, id2).click()
			time.sleep(0.5)
			browser.find_element(By.ID, id1).click()
			time.sleep(0.5)
	except Exception:
		print(browser.find_elements_by_class_name(el_class))
		print(browser.find_elements_by_class_name(el_class)[0].text)
		if browser.find_elements_by_class_name(el_class)[0].text == 'Вернуться к попытке':
			browser.find_elements_by_class_name(el_class)[0].click()


# download_pict
img_xpath = None
img_el = None
img_url = None
cur_url = None
soup = None
div = None
el = None
list_of_files = None
element = None

def download_pict(pict_xpath, img_url):
	global img_el
	global cur_url
	global img_el
	global soup
	global div
	global el
	global list_of_files
	global element
	cur_url = None
	img_el = None
	soup = None
	div = None
	el = None
	list_of_files = None
	element = None

	# print(img_url)
	if pict_xpath:
		img_el = browser.find_element(By.XPATH, pict_xpath)
		img_url = img_el.get_attribute('src')
	if img_url == None:
		cur_url = browser.current_url
		global headers
		r = requests.get(cur_url, headers=headers, verify=False)
		# print(r.text)

		soup = BeautifulSoup(r.text, 'html.parser')

		div = soup.find("div", {"class": "qtext"})
		img_url = div.find("img")['src']
		# print(img_url)

	list_of_files = os.listdir(os.getcwd())
	for file in list_of_files:
		if (file.endswith('.png')) or (file.endswith('.gif')):
			print('est neudalennaya kartinka')
			print(file)
			os.remove(file)

	# print(img_el)
	# print(img_url)
	# img-responsive atto_image_button_text-bottom
	# img-responsive atto_image_button_text-bottom
	global link_xp
	if not xpath_exist(link_xp + '/a'):
		el = browser.find_element(By.XPATH, link_xp)
		# browser.execute_script("arguments[0].appendChild(arguments[1]);", el, "<a href='URL'>открыть</a>")
		browser.execute_script("arguments[0].appendChild(document.createElement('a'));", el)
	element = browser.find_element(By.XPATH, link_xp + '/a')

	browser.execute_script(f"arguments[0].setAttribute('href','{img_url}')", element)
	browser.execute_script("arguments[0].setAttribute('download','current_pict.png')", element)
	time.sleep(0.2)
	browser.execute_script("arguments[0].click();", element)
	# element.click()
	time.sleep(1)
	
	for file in os.listdir(os.getcwd()):
		if (file.endswith('.png')) or (file.endswith('.gif')):
			print(file)
			return file
	print('file ne ska4alsya')
	exit_for_prod('file ne ska4alsya')
	return False

#compare_pict
img1 = None
img2 = None

def compare_pict(file, pict_path):
	global img1
	global img2
	img1 = None
	img2 = None
	# print('VOWEL V F COMPARE PICT')
	# for i in range(len(os.listdir("C:\\progs\\bot_for_test\\picts_test2"))): # nomer testa
	img1 = Image.open(file)
	img2 = Image.open('picts\\' + pict_path)
	try:
		differences = ImageChops.difference(img1, img2)
		# print(differences.getbbox())
		if (differences.getbbox() == None):
		
			print('oddinac')
			return True

	except Exception as e:
		print(e)

	print('raznye')
	return False

#find_quest
quest_text = None
xpath = None
file = None
result = None

def find_quest(questions, main_xpath, second_xpath, img_url):
	global quest_text
	global xpath
	global file
	global result
	question = None
	result = None
	file = None
	quest_text = None
	xpath = None
	for item in questions:
		# print(item)
		quest_text = item['quest_text']
		if (quest_text['main_xpath'] == 'default'):
			# print('main_xpath ne nujno menyat')
			xpath = main_xpath
		else:
			# print('menyaem xpath')
			xpath = quest_text['main_xpath']
			# print(main_xpath)

		if (not xpath_exist(xpath)):
			continue

		if (quest_text['first_line'].endswith('.png')) or (quest_text['first_line'].endswith('.gif')):
			print(quest_text['first_line'])
			file = download_pict(quest_text['main_xpath'], img_url)
			if not file:
				return False
			result = compare_pict(file, quest_text['first_line'])
			os.remove(file)

			if (result):
				print('VOPROS PRO4TEN')
				return item
			else:
				continue

		question = browser.find_element(By.XPATH, xpath).text
		print(quest_text['first_line'])
		# print(question)

		if (((question.find(quest_text['first_line']) != -1)
			and
			not ('exact_quest' in item))
			or
			((question == quest_text['first_line'])
			and
			('exact_quest' in item))):
			if (quest_text['second_line'] == 'nothing'):
				print('VOPROS PRO4TEN')
				return item
			elif (quest_text['second_xpath'] == 'default'):
				print('second_xpath ne nujno menyat')
				xpath = second_xpath
			else:
				print('menyaem second xpath')
				xpath = quest_text['second_xpath']
				print(second_xpath)

			if (not xpath_exist(xpath)):
				continue

			if 'missing' in quest_text:
				if xpath_exist(quest_text['missing_xp']):
					missing_part_q = browser.find_element(By.XPATH, quest_text['missing_xp']).text
					if (missing_part_q.find(quest_text['missing']) != -1):
						continue

			if (quest_text['second_line'].endswith('.png')) or (quest_text['second_line'].endswith('.gif')):
				print(quest_text['second_line'])
				file = download_pict(quest_text['second_xpath'], img_url)
				if not file:
					return False
				result = compare_pict(file, quest_text['second_line'])
				os.remove(file)

				if (result):
					print('VOPROS PRO4TEN')
					return item
				else:
					continue
			
			question = browser.find_element(By.XPATH, xpath).text
			print('\t' + question)

			if (question.find(quest_text['second_line']) != -1):
				print('VOPROS PRO4TEN')
				return item
				
		else:
			continue
		
	print(f'vopros ne nawelsya')
	exit_for_prod('vopros ne nawelsya')
	return False

#solve_radio_chb
img_xpath = None
ans_xpath = None
answer = None
input_el = None

def solve_radio_chb(item, text_xp1, text_xp2, answer_xp1, answer_xp2):
	global img_xpath
	global ans_xpath
	global answer
	global input_el
	global img_el
	global img_url
	img_url = None
	img_el = None
	input_el = None
	img_xpath = None
	ans_xpath = None
	answer = None
	print(item['answer'])
	if (item['text_xp1'] != 'default'):
		print('menyaem xpath v radio chb')
		text_xp1 = item['text_xp1']
		text_xp2 = item['text_xp2']
		answer_xp1 = item['answer_xp1']
		answer_xp2 = item['answer_xp2']
	i=0
	if (item['answer'].endswith('.png')) or (item['answer'].endswith('.gif')):
		while (xpath_exist(text_xp1 + str(i+1) + text_xp2)):
			img_xpath = text_xp1 + str(i+1) + text_xp2
			img_el = browser.find_element(By.XPATH, img_xpath)
			img_url = img_el.get_attribute('src')
			print(img_url)
			file = download_pict(None, img_url)
			if not file:
				return False
			ans_xpath = answer_xp1 + str(i+1) + answer_xp2
			answer = browser.find_element(By.XPATH, ans_xpath)
			browser.execute_script("arguments[0].removeAttribute('checked')", answer)
			
				
			# if (compare_pict(file, item['answer'])):
			# 	answer.click()
			# 	time.sleep(1)#########
			# 	os.remove(file)
			# 	return True
			# else:
			# 	time.sleep(1)#########
			# 	os.remove(file)
			# # 	browser.execute_script("arguments[0].removeAttribute('checked')", answer)
			os.remove(file)
			i += 1
	else:
		while (xpath_exist(text_xp1 + str(i+1) + text_xp2)):
			print(browser.find_element(By.XPATH, text_xp1 + str(i+1) + text_xp2).text)
			if (browser.find_element(By.XPATH, text_xp1 + str(i+1) + text_xp2).text == item['answer']):
				ans_xpath = answer_xp1 + str(i+1) + answer_xp2
				input_el = browser.find_element(By.XPATH, ans_xpath)
				browser.execute_script("arguments[0].removeAttribute('checked')", input_el)
				# input_el.click()
				return True
				# browser.execute_script("arguments[0].setAttribute('checked','checked')", answer)
			i += 1
	print('otvet ne pro4elsya')
	exit_for_prod('otvet ne pro4elsya')
	return False

#solve_chb
html_elem = None
totals = []
formuls = []
values = []
values_Variables = None
dict_of_indexes = None
list_keys = None
text_xpath = None
text_ans = None

def solve_chb(item, text_chb_xp1, text_chb_xp2, answer_chb_xp1, answer_chb_xp2):
	global img_xpath
	global ans_xpath
	global answer
	global input_el
	global img_el
	global img_url
	global file
	global html_elem
	global values_Variables
	global dict_of_indexes
	global totals 
	global formuls
	global values
	global list_keys
	global text_xpath
	global text_ans
	text_xpath = None
	text_ans = None
	list_keys = None
	values_Variables = None
	html_elem = None
	file = None
	img_url = None
	img_el = None
	input_el = None
	img_xpath = None
	ans_xpath = None
	answer = None
	print(item['answer'])
	if (item['text_chb_xp1'] != 'default'):
		print('menyaem xpath v chb')
		text_chb_xp1 = item['text_chb_xp1']
		text_chb_xp2 = item['text_chb_xp2']
		answer_chb_xp1 = item['answer_chb_xp1']
		answer_chb_xp2 = item['answer_chb_xp2']

	i=0

	if (item['answer'][0] == 'индивидуалочка'):
		global second_xpath_type1
		html_elem = browser.find_element(By.XPATH, second_xpath_type1).text
		print(html_elem)
		values_Variables = html_elem.split()
		dict_of_indexes = item['answer'][len(item['answer'])-1]
		totals = []
		formuls = []
		for	j in range(len(item['answer']) - 2):
			if isinstance(item['answer'][j+1], str):
				print('Да, это строка')
				formuls.append(item['answer'][j+1])
		print(values_Variables)
		print(formuls)
		values = []
		list_keys =  list(dict_of_indexes)
		print(dict_of_indexes)
		
		for	j in range(len(list_keys)):
			print(dict_of_indexes[f'{list_keys[j]}'])
			values.append(values_Variables[dict_of_indexes[f'{list_keys[j]}']])
		print(values)

		for	j in range(len(list_keys)):
			dict_of_indexes[f'{list_keys[j]}'] = values[j]
			print(dict_of_indexes[f'{list_keys[j]}'])

		for	j in range(len(formuls)):
			totals.append(''.join(formuls[j].split('=')[0]))
			formuls[j] = ''.join(formuls[j].split('=')[1])
			print(formuls[j])
			for k in range(len(list_keys)):
				formuls[j] = formuls[j].replace(list_keys[k], dict_of_indexes[f'{list_keys[k]}'])
				# print(formuls[j])
		print(formuls)
		
		for	j in range(len(formuls)):
			print(formuls[j])
			if (item['type_variable'] == 'int'):
				formuls[j] = int(eval(formuls[j]))
				print(formuls[j])
			if (item['type_variable'] == 'float'):
				formuls[j] = float(eval(formuls[j]))
				print(formuls[j])

		while (xpath_exist(text_chb_xp1 + str(i+1) + text_chb_xp2)):
			text_xpath = text_chb_xp1 + str(i+1) + text_chb_xp2
			text_ans = browser.find_element(By.XPATH, text_xpath).text

			ans_xpath = answer_chb_xp1 + str(i+1) + answer_chb_xp2
			answer = browser.find_element(By.XPATH, ans_xpath)
			browser.execute_script("arguments[0].removeAttribute('checked')", answer)
			# for j in range(len(formuls)):
			# 	# print(str(totals[j]))
			# 	if (text_ans.find(' ' + str(formuls[j])) != -1
			# 		and
			# 		text_ans.find(totals[j]) != -1
			# 		):
			# 		# ans_xpath = answer_chb_xp1 + str(i+1) + answer_chb_xp2
			# 		# answer = browser.find_element(By.XPATH, ans_xpath)
			# 		# browser.execute_script("arguments[0].setAttribute('type','text')", answer)
			# 		# time.sleep(0.2)
			# 		# answer.clear()
			# 		# answer.send_keys('1')
			# 		answer.click()
			# 		totals[j] = "asdasdqwe"
			# 		break
			i += 1

		print(item['answer'][0])

	
	while (xpath_exist(text_chb_xp1 + str(i+1) + text_chb_xp2)):
		if (text_chb_xp2.endswith('/img') or xpath_exist(text_chb_xp1 + str(i+1) + text_chb_xp2 + '/img')):
			img_xpath = text_chb_xp1 + str(i+1) + text_chb_xp2
			if not img_xpath.endswith('/img'):
				img_xpath = img_xpath + '/img'
			img_el = browser.find_element(By.XPATH, img_xpath)
			img_url = img_el.get_attribute('src')
			print(img_url)
			file = download_pict(None, img_url)
			if not file:
				return False
			ans_xpath = answer_chb_xp1 + str(i+1) + answer_chb_xp2
			answer = browser.find_element(By.XPATH, ans_xpath)
			browser.execute_script("arguments[0].removeAttribute('checked')", answer)
			# for j in range(len(item['answer'])):
			# 	if (item['answer'][j].endswith('.png')) or (item['answer'][j].endswith('.gif')):
			# 		if (compare_pict(file, item['answer'][j])):
			# 			# ans_xpath = answer_chb_xp1 + str(i+1) + answer_chb_xp2
			# 			# answer = browser.find_element(By.XPATH, ans_xpath)
			# 			# browser.execute_script("arguments[0].setAttribute('type','text')", answer)
			# 			# time.sleep(0.2)
			# 			# answer.clear()
			# 			# answer.send_keys('1')
			# 			answer.click()
			# 			break
					# else:
					# 	browser.execute_script("arguments[0].removeAttribute('checked')", answer)

			os.remove(file)

		else:
			text_xpath = text_chb_xp1 + str(i+1) + text_chb_xp2
			print(browser.find_element(By.XPATH, text_xpath).text)
			ans_xpath = answer_chb_xp1 + str(i+1) + answer_chb_xp2
			input_el = browser.find_element(By.XPATH, ans_xpath)
			browser.execute_script("arguments[0].removeAttribute('checked')", input_el)
			# for j in range(len(item['answer'])):
			# 	if not ((item['answer'][j].endswith('.png')) or (item['answer'][j].endswith('.gif'))):
			# 		if (browser.find_element(By.XPATH, text_xpath).text == item['answer'][j]):
						
			# 			# ans_xpath = answer_chb_xp1 + str(i+1) + answer_chb_xp2
			# 			# answer = browser.find_element(By.XPATH, ans_xpath)
			# 			# browser.execute_script("arguments[0].setAttribute('type','text')", answer)
			# 			# time.sleep(0.2)
			# 			# answer.clear()
			# 			# answer.send_keys('1')
			# 			input_el.click()
			# 			break
			
		i += 1
		

	
	return True

# solve_select
quantity_ans = None
def solve_select(item, text_sel_xp1, text_sel_xp2, answer_sel_xp1, answer_sel_xp2):
	global answer
	global quantity_ans
	global img_xpath
	global img_el
	global img_url
	global file
	file = None
	img_xpath = None
	img_el = None
	img_url = None
	answer = item['answer']
	quantity_ans = item['quantity_ans']
	print(answer)
	if ('text_sel_xp1' in item):
		print('menyaem xpath v sel')
		text_sel_xp1 = item['text_sel_xp1']
		text_sel_xp2 = item['text_sel_xp2']
		answer_sel_xp1 = item['answer_sel_xp1']
		answer_sel_xp2 = item['answer_sel_xp2']

	for i in range(len(answer)):
		for j in range(len(answer)):
			if not xpath_exist(text_sel_xp1 + str(i+1) + text_sel_xp2):
				return True
			quest = browser.find_element(By.XPATH, text_sel_xp1 + str(i+1) + text_sel_xp2).text

			if (answer[j]['line'].endswith('.png')) or (answer[j]['line'].endswith('.gif')):
				img_xpath = text_sel_xp1 + str(i+1) + text_sel_xp2
				img_el = browser.find_element(By.XPATH, img_xpath)
				img_url = img_el.get_attribute('src')
				print(img_url)
				file = download_pict(None, img_url)
				if not file:
					return False
						
				if (compare_pict(file, answer[j]['line'])):
					print('sravnil pole otveta')

					for k in range(quantity_ans):
						ans_xpath = f'{answer_sel_xp1 + str(i+1) + answer_sel_xp2 + str(k+1)}]'
						print(browser.find_element(By.XPATH, ans_xpath).text)

						if (browser.find_element(By.XPATH, ans_xpath).text == answer[j]['ans']):
							select_el = browser.find_element(By.XPATH, ans_xpath)
							# browser.execute_script("arguments[0].setAttribute('selected','selected')", select_el)
							browser.execute_script("arguments[0].removeAttribute('selected')", select_el)
							break
				os.remove(file)

			elif (
				((quest.find(answer[j]['line']) != -1)
				and
				not ('exact_parse' in item))
				or
				((quest == answer[j]['line'])
				and
				('exact_parse' in item))
				):
				print('sravnil pole otveta')

				for k in range(quantity_ans):
					ans_xpath = f'{answer_sel_xp1 + str(i+1) + answer_sel_xp2 + str(k+1)}]'
					print(browser.find_element(By.XPATH, ans_xpath).text)

					if (browser.find_element(By.XPATH, ans_xpath).text == answer[j]['ans']):
						select_el = browser.find_element(By.XPATH, ans_xpath)
						# browser.execute_script("arguments[0].setAttribute('selected','selected')", select_el)
						browser.execute_script("arguments[0].removeAttribute('selected')", select_el)
						break

	return True

# solve_drag_drop
array_xp1 = None
array_xp2 = None
array_xp = None
answer_xp = None
ans_xpath = None
ans_row1 = []
main_ans_row = {}
ans_row = []
array_el = None
num_ar = None
def solve_drag_drop(item, array_xp, answer_xp):
	global array_xp1
	global array_xp2
	global ans_xpath
	global input_el
	global ans_row1
	global el
	global main_ans_row
	global ans_row
	global array_el
	global num_ar
	global file
	file = None
	array_el = None
	num_ar = None
	ans_row = []
	main_ans_row = {}
	el = None
	ans_row1 = []
	input_el = None
	ans_xpath = None
	if ('array_xp1' in item):
		# print('menyaem xpath v drag&drop')
		array_xp1 = item['array_xp1']
		array_xp2 = item['array_xp2']

	if (item['answer_xp'] != 'default'):
		# print('menyaem xpath v drag&drop')
		array_xp = item['array_xp']
		answer_xp = item['answer_xp']

	#очищение дефолтных ответов
	################
	#for k in range(len(item['answer'])):
		#ans_xpath = f'{answer_xp + str(k+2)}]'

		#if (item['answer'][0].endswith('.png')) or (item['answer'][0].endswith('.gif')):
			#ans_xpath = f'{answer_xp + str(k+1)}]'

		#input_el = browser.find_element(By.XPATH, ans_xpath)
		#browser.execute_script("arguments[0].setAttribute('type','text')", input_el)
		# print('opened', k+1, 'input for clearing')
		#time.sleep(0.2)
		#input_el.clear()
		#input_el.send_keys(0)

	# time.sleep(0.5)
	# refresh_browser()
	# time.sleep(1)
	################

	if ('array2_xp' in item):
		ans_row1 = []
		j = 2
		while (xpath_exist(f'{array_xp + str(j)}]')):
			el = browser.find_element(By.XPATH, f'{array_xp + str(j)}]').text
			if (el[0] == '‑'): #  тире это не минус
				el = '-' + el[1:]
			ans_row1.append(el)
			# time.sleep(0.1)
			j += 2
		print(ans_row1)

	elif 'multiple_arrays' in item:
		main_ans_row = {}
		for i in range(item['multiple_arrays']):
			ans_row = []
			j = 2
			while (xpath_exist(f'{array_xp1 + str(i+1) + array_xp2 + str(j)}]')):
				el = browser.find_element(By.XPATH, f'{array_xp1 + str(i+1) + array_xp2 + str(j)}]').text
				if (el[0] == '‑'): #  тире это не минус
					el = '-' + el[1:]
				ans_row.append(el)
				# time.sleep(0.1)
				j += 2
			print(ans_row)
			array_el = browser.find_element(By.XPATH, f'{array_xp1 + str(i+1)}]')
			num_ar = array_el.get_attribute("class")[-1]
			main_ans_row[f'{num_ar}'] = ans_row
		print(main_ans_row)

	elif (item['answer'][0].endswith('.png')) or (item['answer'][0].endswith('.gif')):
		time.sleep(1)

		img_urls = []
		j = 2
		while (xpath_exist(f'{array_xp + str(j)}]')):
			el = browser.find_element(By.XPATH, f'{array_xp + str(j)}]').get_attribute('src')
			print(el)
			img_urls.append(el)
			# time.sleep(0.1)
			j += 2
		print(img_urls)

	else:
		ans_row = []
		j = 2
		while (xpath_exist(f'{array_xp + str(j)}]')):
			el = browser.find_element(By.XPATH, f'{array_xp + str(j)}]').text
			print(el)
			if (el[0] == '‑'): #  тире это не минус
				el = '-' + el[1:]
			ans_row.append(el)
			# time.sleep(0.1)
			j += 2
		print(ans_row)

	print(item['answer'])
	if (item['answer'][0].endswith('.png')) or (item['answer'][0].endswith('.gif')):
		i = 0
		for j in range(len(img_urls)):
			file = download_pict(None, img_urls[j])
			if not file:
				return False
			for k in range(len(item['answer'])):
				if (compare_pict(file, item['answer'][k])):
					ans_xpath = f'{answer_xp + str(i+1)}]'
					input_el = browser.find_element(By.XPATH, ans_xpath)
					browser.execute_script("arguments[0].setAttribute('type','text')", input_el)
					# print('opened', k+1, 'input for clearing')
					time.sleep(0.2)
					input_el.clear()
					# input_el.send_keys(j+1)
					# print(img_urls[j])
					i += 1
					break
				
			os.remove(file)

	for k in range(len(item['answer'])):
		ans_xpath = f'{answer_xp + str(k+2)}]'

		if (item['answer'][0].endswith('.png')) or (item['answer'][0].endswith('.gif')):
			# ans_xpath = f'{answer_xp + str(k+1)}]'
			break

		input_el = browser.find_element(By.XPATH, ans_xpath)
		browser.execute_script("arguments[0].setAttribute('type','text')", input_el)
		# print('opened', k+1, 'input for clearing')
		time.sleep(0.2)
		input_el.clear()
		# if ('array2_xp' in item):
		# 	if item['answer'][k] in ans_row:
		# 		input_el.send_keys(ans_row.index(item['answer'][k])+1)

		# 	elif item['answer'][k] in ans_row1:
		# 		input_el.send_keys(ans_row1.index(item['answer'][k])+1)

		# 	else:
		# 		print('elem in arrays not found')
		# 		exit_for_prod('elem in arrays not found')

		# elif ('multiple_arrays' in item):
		# 	num_ar = input_el.get_attribute("class")[-1]
		# 	# for j in range(len(main_ans_row)):

		# 	if item['answer'][k] in main_ans_row[f'{num_ar}']:
		# 		input_el.send_keys(main_ans_row[f'{num_ar}'].index(item['answer'][k])+1)
		# 		print(main_ans_row[f'{num_ar}'].index(item['answer'][k])+1)
		# 	else:
		# 		print(f"elementa {item['answer'][k]} net v nujnom massive")
		# 		exit_for_prod(f"elementa {item['answer'][k]} net v nujnom massive")
		
		# elif (item['answer'][0].endswith('.png')):
			# if item['answer'][k] in img_urls:
			# 	input_el.send_keys(img_urls.index(item['answer'][k])+1)
			# 	print(img_urls.index(item['answer'][k])+1)
			# else:
			# 	print('elem of answer in array not found')
			# 	exit_for_prod('elem of answer in array not found')

			# for j in range(len(img_urls)):
			# 	file = download_pict(None, img_urls[j])
				
			# 	if (compare_pict(file, item['answer'][k])):
			# 		input_el.send_keys(j+1)
			# 		print(img_urls[j])
			# 		os.remove(file)
			# 		break
				
			# 	os.remove(file)
			
		# else:
		# 	input_el.send_keys(ans_row.index(item['answer'][k])+1)

	return True

#solve_input
new_dict_of_indexes = {}
string = None
def solve_input(item, answer_inp_xp, string_xpath):
	global img_xpath
	global ans_xpath
	global answer
	global input_el
	global img_el
	global img_url
	global file
	global html_elem
	global values_Variables
	global dict_of_indexes
	global totals 
	global formuls
	global values
	global list_keys
	global text_xpath
	global text_ans
	global new_dict_of_indexes
	global string
	string = None
	text_xpath = None
	text_ans = None
	list_keys = None
	values_Variables = None
	html_elem = None
	file = None
	img_url = None
	img_el = None
	input_el = None
	img_xpath = None
	ans_xpath = None
	answer = None
	if (item['answer_inp_xp'] != 'default'):
		print('menyaem xpath v chb')
		answer_inp_xp = item['answer_inp_xp']

	if (item['answer'] == 'skip'):
		print('skip')
		return True

	elif (item['answer'][0] == 'индивидуалочка'):
		if 'string_xpath' in item:
			print('menyaem xpath v chb')
			string_xpath = item['string_xpath']
		html_elem = browser.find_element(By.XPATH, string_xpath).text
		print(html_elem)
		values_Variables = html_elem.split()
		dict_of_indexes = {}
		dict_of_indexes = item['answer'][len(item['answer'])-1]
		totals = []
		formuls = []
		for	j in range(len(item['answer']) - 2):
			if isinstance(item['answer'][j+1], str):
				print('Да, это строка')
				formuls.append(item['answer'][j+1])
		print(values_Variables)
		print(formuls)
		values = []
		list_keys =  list(dict_of_indexes)
		print(dict_of_indexes)
		
		for	j in range(len(list_keys)):
			print(dict_of_indexes[f'{list_keys[j]}'])
			# получаем индекс который будем юзать для спаршенной строки
			index = dict_of_indexes[f'{list_keys[j]}']
			if (item['type_variable'] == 'float'):
				values.append(values_Variables[index].replace(',','.'))
			else:
				values.append(values_Variables[index])
		print(values)

		new_dict_of_indexes = {}

		for	j in range(len(list_keys)):
			if 'need_exact_value' in item:
				for k in range(len(item['need_exact_value'])):
					if ((item['need_exact_value'][k]['var'] == dict_of_indexes[f'{list_keys[j]}'])
						or
						(item['need_exact_value'][k]['var'] == list_keys[j])
						):
						# слайсим число нужной нам строки
						# if 'start' in item['need_exact_value'][k]:

						temp = re.findall('[-+]?(?:\d+(?:\.\d*)?|\.\d+)', values[j].replace(',', '.'))

						values[j] = temp[item['need_exact_value'][k]['idx']]

							# values[j] = values[j][item['need_exact_value'][k]['start']:item['need_exact_value'][k]['end']]
						# слайсим до определенного символа
						# elif 'slice_to' in item['need_exact_value'][k]:
						# 	values[j] = ''.join(values[j].split(item['need_exact_value'][k]['slice_to'])[item['need_exact_value'][k]['ind']])
						# print(values[j])
			if values[j].endswith(',') or values[j].endswith('.'):
				values[j] = values[j][:-1]
			new_dict_of_indexes[f'{list_keys[j]}'] = values[j]
			print(new_dict_of_indexes[f'{list_keys[j]}'])


		if 'system_of_equations' in item:
			for j in range(len(item['system_of_equations']['conditions'])):
				temp = item['system_of_equations']['conditions'][j].replace(item['system_of_equations']['var'], new_dict_of_indexes[f'{item["system_of_equations"]["var"]}'])
				if eval(temp):
					temp1 = formuls[j]
					formuls.append(temp1)
					break

		
		for	j in range(len(formuls)):
			totals.append(''.join(formuls[j].split('=')[0]))
			formuls[j] = ''.join(formuls[j].split('=')[1])
			print(formuls[j])
			for k in range(len(list_keys)):
				formuls[j] = formuls[j].replace(list_keys[k], new_dict_of_indexes[f'{list_keys[k]}'])
				# print(formuls[j])
		print(formuls)
		
		for	j in range(len(formuls)):
			print(formuls[j])
			if (item['type_variable'] == 'int'):
				formuls[j] = int(eval(formuls[j]))
				print(formuls[j])
			if (item['type_variable'] == 'float'):
				formuls[j] = float(eval(formuls[j]))
				print(formuls[j])

		if (item['type_variable'] == 'float'):
			precision = 2
			if html_elem.find('десятых') != -1:
				precision = 1
			if html_elem.find('сотых') != -1:
				precision = 2
			if html_elem.find('тысячных') != -1:
				precision = 3
			answer = round(formuls[len(formuls) - 1], precision)
		else:
			answer = formuls[len(formuls) - 1]

		if html_elem.find('целых') != -1:
			answer = int(formuls[len(formuls) - 1] + (0.5 if formuls[len(formuls) - 1] > 0 else -0.5))
		
		answer = str(answer)

		string = answer

		answer = string.replace('.',',')

		if (
			(string.endswith(".0") or string.endswith(".1")
			or
			string.endswith(".2") or string.endswith(".3")
			or
			string.endswith(".4") or string.endswith(".5")
			or
			string.endswith(".6") or string.endswith(".7")
			or
			string.endswith(".8") or string.endswith(".9"))
			and (html_elem.find('сотых') != -1)
			):
			answer = answer + '0'


		if html_elem.find('тысячных') != -1:
			if len(string.split('.')[1]) == 1:
				answer = answer + '00'
			elif len(string.split('.')[1]) == 2:
				answer = answer + '0'
		
		print(answer)
		answer_input = browser.find_element(By.XPATH, answer_inp_xp)
		answer_input.clear()
		# answer_input.send_keys(answer)

	else:
		print(item['answer'])
		answer_input = browser.find_element(By.XPATH, answer_inp_xp)
		answer_input.clear()
		# answer_input.send_keys(item['answer'])

	return True


def check_quest(item, array_xp, answer_xp, answer_inp_xp, string_xpath, text_xp1, text_xp2, answer_xp1, answer_xp2, text_chb_xp1, text_chb_xp2, answer_chb_xp1, answer_chb_xp2, text_sel_xp1, text_sel_xp2, answer_sel_xp1, answer_sel_xp2):
	if (item['format'] == 'radio checkbox'):
		# time.sleep(60 * random.randrange(5, 15))
		return solve_radio_chb(item, text_xp1, text_xp2, answer_xp1, answer_xp2)
	elif (item['format'] == 'checkbox'):
		# time.sleep(60 * random.randrange(10, 25))
		return solve_chb(item, text_chb_xp1, text_chb_xp2, answer_chb_xp1, answer_chb_xp2)
	elif (item['format'] == 'select'):
		# time.sleep(60 * random.randrange(20, 35))
		return solve_select(item, text_sel_xp1, text_sel_xp2, answer_sel_xp1, answer_sel_xp2)
	elif (item['format'] == 'drag&drop'):
		# time.sleep(60 * random.randrange(15, 35))
		return solve_drag_drop(item, array_xp, answer_xp)
	elif (item['format'] == 'input'):
		# time.sleep(60 * random.randrange(10, 40))
		return solve_input(item, answer_inp_xp, string_xpath)

#resolve
main_xpath = None
second_xpath = None
text_xp1 = None
text_xp2 = None
answer_xp1 = None
answer_xp2 = None
	
text_chb_xp1 = None
text_chb_xp2 = None
answer_chb_xp1 = None
answer_chb_xp2 = None

text_sel_xp1 = None
text_sel_xp2 = None
answer_sel_xp1 = None
answer_sel_xp2 = None
def resolve(data, array_xp, answer_xp, answer_inp_xp, string_xpath, img_url):
	global main_xpath
	global second_xpath
	global text_xp1
	global text_xp2
	global answer_xp1
	global answer_xp2
		
	global text_chb_xp1
	global text_chb_xp2
	global answer_chb_xp1
	global answer_chb_xp2

	global text_sel_xp1
	global text_sel_xp2
	global answer_sel_xp1
	global answer_sel_xp2
	main_xpath = data['main_xpath']
	print(main_xpath)
	second_xpath = data['second_xpath']
	print(second_xpath)

	text_xp1 = data['text_xp1']
	text_xp2 = data['text_xp2']
	answer_xp1 = data['answer_xp1']
	answer_xp2 = data['answer_xp2']
	
	text_chb_xp1 = data['text_chb_xp1']
	text_chb_xp2 = data['text_chb_xp2']
	answer_chb_xp1 = data['answer_chb_xp1']
	answer_chb_xp2 = data['answer_chb_xp2']

	text_sel_xp1 = data['text_sel_xp1']
	text_sel_xp2 = data['text_sel_xp2']
	answer_sel_xp1 = data['answer_sel_xp1']
	answer_sel_xp2 = data['answer_sel_xp2']

	item = find_quest(data['questions'], main_xpath, second_xpath, img_url)
	if item:
		check_quest(item, array_xp, answer_xp, answer_inp_xp, string_xpath, text_xp1, text_xp2, answer_xp1, answer_xp2, text_chb_xp1, text_chb_xp2, answer_chb_xp1, answer_chb_xp2, text_sel_xp1, text_sel_xp2, answer_sel_xp1, answer_sel_xp2)
		return True
	else:
		return False

def build_url(base_url, args_dict):
    # Returns a list in the structure of urlparse.ParseResult
    url_parts = list(parse.urlparse(base_url))
    url_parts[4] = parse.urlencode(args_dict)
    return parse.urlunparse(url_parts)

def execute_command(command):
	if command.split() == []:
		return
	elif command.split()[0] == 'urlparse':
		queries = dict(parse.parse_qsl(parse.urlsplit(browser.current_url).query))
		print('queries: ', queries)
		del queries['page']
		print('new queries: ', queries)
		url = browser.current_url
		print('old url: ', url + parse.urlencode(queries))
		parse.urlsplit(url).query

		print('new url: ', build_url(url, queries))

	elif command.split()[0] == 'swTo':
		browser.switch_to.window(browser.window_handles[ int(command.split()[1]) ])
	elif command.split()[0] == 'help':
		print('xpexist - 4ekaet suwestvyet li xpath na stranice', 'resolveq - probuet rewit tekuwiy vopros')
	elif command.split()[0] == 'xpex':
		print(xpath_exist(command.split()[1]))
	elif command.split()[0] == 'resq':
		global data
		global img_url
		resolve(data[f'type{type_q}'], data['array_xp'], data['answer_xp'], data['answer_inp_xp'], data['string_xpath'], img_url)
	else:
		print('unknown command, type "help" for more info')


#############==========================================================#############

accs = []
with open('accs.txt', 'r', encoding='utf-8') as file:
	for line in file:
		accs.append(line.replace('\n', '').split(None, 1))
	print(accs)


browser = webdriver.Firefox(options = option) #firefox_profile
browser.get('https://eios.sibsutis.ru/')

#prod
if mode == 2:
	# url_test = input('ссылка с кнопкой прохода на тест группы:')
	url_test = config.url_test
	context_menu_logout_xp = '/html/body/div[1]/nav/ul[2]/li[2]/div/div/div/div/div/a/span/span[1]'
	xpath_logout = '/html/body/div[1]/nav/ul[2]/li[2]/div/div/div/div/div/div/a[6]/span'
	time.sleep(1)
	for acc in accs:

		login_xpath = '//*[@id="username"]'
		browser.find_element(By.XPATH, login_xpath).send_keys(acc[0])

		# time.sleep(2)

		password_xpath = '//*[@id="password"]'
		browser.find_element(By.ID, 'password').send_keys(acc[1])
		# time.sleep(2)

		xpath = '//*[@id="loginbtn"]'
		browser.find_element(By.XPATH, xpath).click()

		time.sleep(1)
		if check_logout():
			continue

		acc_name = browser.find_element(By.XPATH, '/html/body/div[1]/nav/ul[2]/li[2]/div/div/div/div/div/a/span/span[1]').text
		print('bot logined by name: ' + acc_name)

		# оформляем заголовок чтобы посылать get запрос с авторизацией!!!
		cookie = browser.get_cookies()
		moodle_cookie = cookie[0]['name'] + '=' + cookie[0]['value']
		print(moodle_cookie)

		headers = {
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'Accept-Encoding': 'gzip, deflate, br',
			'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
			'Connection': 'keep-alive',
			'Cookie': moodle_cookie,
			'Upgrade-Insecure-Requests': '1',
			'Sec-Fetch-Dest': 'document',
			'Sec-Fetch-Mode': 'navigate',
			'Sec-Fetch-Site': 'none',
			'Sec-Fetch-User': '?1',
			'Upgrade-Insecure-Requests': '1',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
		}

	
		browser.get(url_test)
		time.sleep(1)
		if check_logout():
			continue
		
		if xpath_exist("//button[text()='Начать тестирование']"):
			WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Начать тестирование']"))).click()
		#elif xpath_exist('/html/body/div[2]/div[2]/div/div[1]/section/div[1]/div[3]/div/form/button'):
			#WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/section/div[1]/div[3]/div/form/button"))).click()
		#elif xpath_exist('/html/body/div[2]/div[2]/div/div[1]/section/div[1]/div[4]/div/form/button'):
			#WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/section/div[1]/div[4]/div/form/button"))).click()
		elif xpath_exist('//button[text()="Продолжить последнюю попытку"]'):
			WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Продолжить последнюю попытку']"))).click()
		elif xpath_exist('//button[text()="Пройти тест заново"]'):
			WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Пройти тест заново']"))).click()
		else:
			print('ne nawel knopku testa')

		print(browser.window_handles)

		if len(browser.window_handles) == 2:
			
			browser.switch_to.window(browser.window_handles[1])


		with open('data\\questions_for_1_test.json', 'r', encoding='utf-8') as file:
			data = json.load(file)

		link_xp = data['link_xp']
		check_xpath_img = data['check_xpath_img']
		second_xpath_type1 = data['type1']['second_xpath']
		main_xpath_type2 = data['type2']['main_xpath']

		time.sleep(1)

		url = browser.current_url
		queries = dict(parse.parse_qsl(parse.urlsplit(url).query))
		if 'page' in queries:
			del queries['page']
			new_url = build_url(url, queries)
			print('new url: ', new_url)
			browser.get(new_url)
			time.sleep(1)

		if check_logout():
			continue

		for i in range(40):
			time.sleep(1)
			if check_logout():
				break
			print(f'=================={i+1}==================')
			

			# get_attribute работает только вне функции
			if (xpath_exist(check_xpath_img)):
				type_q = '1'
				print('vopros s picture v p[1]')
				img_el = browser.find_element(By.XPATH, check_xpath_img)
				img_url = img_el.get_attribute('src')
			else:
				type_q = '2'
				print('vopros bez picture v p[1]')
				img_url = None

			# сократить количество аргументов
			resolve(data[f'type{type_q}'], data['array_xp'], data['answer_xp'], data['answer_inp_xp'], data['string_xpath'], img_url)

			# if (i == 0):
			# 	xpath = '/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[2]/input'
			# else:
			# 	xpath = '/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[2]/input[2]'
			id = 'mod_quiz-next-nav'
			browser.find_element(By.ID, id).click()
		print('accaunt protestirovan')

		if len(browser.window_handles) == 2:
			browser.close()
			browser.switch_to.window(browser.window_handles[0])

		# browser.find_element(By.XPATH, context_menu_logout_xp).click()
		# time.sleep(1)
		# browser.find_element(By.XPATH, xpath_logout).click()
		# time.sleep(3)
		if not check_logout():
			text_html = browser.page_source
			soup = BeautifulSoup(text_html, 'html.parser')

			url_to_logout = soup.find("a", {"data-title": "logout,moodle"})['href']
			browser.get(url_to_logout)
			time.sleep(4)

	print('successfully finished')

#dev
elif mode == 1:
	time.sleep(1)

	login_xpath = '//*[@id="username"]'
	browser.find_element(By.XPATH, login_xpath).send_keys(accs[0][0])

	# time.sleep(2)

	password_xpath = '//*[@id="password"]'
	browser.find_element(By.ID, 'password').send_keys(accs[0][1])
	# time.sleep(2)

	xpath = '//*[@id="loginbtn"]'
	browser.find_element(By.XPATH, xpath).click()

	time.sleep(0.5)

	acc_name = browser.find_element(By.XPATH, '/html/body/div[1]/nav/ul[2]/li[2]/div/div/div/div/div/a/span/span[1]').text
	print('bot logined by name: ' + acc_name)

	# оформляем заголовок чтобы посылать get запрос с авторизацией!!!
	cookie = browser.get_cookies()
	moodle_cookie = cookie[0]['name'] + '=' + cookie[0]['value']
	print(moodle_cookie)

	headers = {
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Encoding': 'gzip, deflate, br',
		'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
		'Connection': 'keep-alive',
		'Cookie': moodle_cookie,
		'Upgrade-Insecure-Requests': '1',
		'Sec-Fetch-Dest': 'document',
		'Sec-Fetch-Mode': 'navigate',
		'Sec-Fetch-Site': 'none',
		'Sec-Fetch-User': '?1',
		'Upgrade-Insecure-Requests': '1',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
	}

	# browser.get(link_na_test)

	url_test = 'https://eios.sibsutis.ru/mod/quiz/view.php?id=78495' # &page=1


	browser.get('https://eios.sibsutis.ru/mod/quiz/view.php?id=81153')
	time.sleep(1)
	try:
		WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/section/div[1]/div[3]/div/form/button"))).click()
	except Exception as e:
		print('не смог найти кнопку открытия теста')

	print(browser.window_handles)
	
	if len(browser.window_handles) == 2:
		browser.switch_to.window(browser.window_handles[1])

	
	while True:
		command = input('cmd >')
		if not (command == 'exit'):
			with open('data\\questions_for_14_15_test.json', 'r', encoding='utf-8') as file:
				data = json.load(file)

			link_xp = data['link_xp']
			check_xpath_img = data['check_xpath_img']
			second_xpath_type1 = data['type1']['second_xpath']
			main_xpath_type2 = data['type2']['main_xpath']

			if (xpath_exist(check_xpath_img)):
				type_q = '1'
				img_el = browser.find_element(By.XPATH, check_xpath_img)
				img_url = img_el.get_attribute('src')
			else:
				type_q = '2'
				img_url = None
			try:
				execute_command(command)
			except Exception as e:
				print(e)
		else:
			print('vihod iz progi')
			browser.quit()
			exit(0)
# https://eios.sibsutis.ru/mod/quiz/view.php?id=81153