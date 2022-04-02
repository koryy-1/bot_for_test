import time
import os
import shutil
from selenium import webdriver
# import requests
from PIL import Image, ImageChops
import json

# https://eios.sibsutis.ru/mod/quiz/attempt.php?attempt=127854&cmid=55478
# print('ссылка на тест')
# link_na_test = input()

option = webdriver.FirefoxOptions()
option.set_preference('dom.webdriver.enabled', False)
option.set_preference('dom.webnotifications.enabled', False)
option.set_preference('general.useragent.override', 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0')
option.set_preference("browser.download.folderList",2)
option.set_preference("browser.download.manager.showWhenStarting",False)
option.set_preference("browser.download.dir", 'C:\\progs\\bot_for_test')
option.set_preference("browser.helperApps.neverAsk.saveToDisk", "image/png")

# option.headless = True



# функция проверяет существование xpath в странице
def xpath_exist(url):
	try:
		browser.find_element_by_xpath(url)
		exist = True
	except Exception:
		exist = False
	return exist

def refresh_browser():
	xpath = '/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[2]/input'
	xpath1 = '/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[2]/input[2]'
	# print(browser.current_url)
	if (browser.current_url[-2:] == '39'): # количество вопросов
		browser.find_element_by_xpath(xpath).click()
		time.sleep(0.5)
		browser.find_element_by_xpath(xpath1).click()
		time.sleep(0.5)
	elif(not xpath_exist(xpath1)):
		browser.find_element_by_xpath(xpath).click()
		time.sleep(0.5)
		browser.find_element_by_xpath(xpath).click()
		time.sleep(0.5)
	else:
		browser.find_element_by_xpath(xpath1).click()
		time.sleep(0.5)
		browser.find_element_by_xpath(xpath).click()
		time.sleep(0.5)


def find_quest(questions, main_xpath, second_xpath):
	for item in questions:
		# print(item)
		quest_text = item['quest_text']
		if (quest_text['main_xpath'] == 'default'):
			print('main_xpath ne nujno menyat')
			xpath = main_xpath
		else:
			print('menyaem xpath')
			xpath = quest_text['main_xpath']
			print(main_xpath)

		if (not xpath_exist(xpath)):
			continue

		question = browser.find_element_by_xpath(xpath).text
		print(question)

		if (question == quest_text['first_line']):
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

			question = browser.find_element_by_xpath(xpath).text
			print(f'	' + question)

			if (question == quest_text['second_line']):
				print('VOPROS PRO4TEN')
				return item
		else:
			continue
		
	print(f'vopros ne nawelsya')
	exit(0)


def solve_radio_chb(answer):
	print(answer)

def solve_chb(answer):
	print(answer)

def solve_select(answer):
	print(answer)

def solve_drag_drop(answer):
	print(answer)

def check_quest(item):
	if (item['format'] == 'radio checkbox'):
		solve_radio_chb(item['answer'])
	elif (item['format'] == 'checkbox'):
		solve_chb(item['answer'])
	elif (item['format'] == 'select'):
		solve_select(item['answer'])
	elif (item['format'] == 'drag&drop'):
		solve_drag_drop(item['answer'])


def resolve(data):
	main_xpath = data['main_xpath']
	print(main_xpath)
	second_xpath = data['second_xpath']
	print(second_xpath)

	item = find_quest(data['questions'], main_xpath, second_xpath)
	check_quest(item)



def compare_pict(file):
	for x in range(1):
		img1 = Image.open(file)
		img2 = Image.open(f'picts_test2\\{x}.png')
		try:
			differences = ImageChops.difference(img1, img2)
			# print(differences.getbbox())
			if (differences.getbbox() == None):
			
				print('oddinac')

				if (x == 0):
					question_xpath = '/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[1]/p[2]'
					question = browser.find_element_by_xpath(question_xpath).text
					print(f'{i+1})	' + question)
					# print(question)

					if (question == 'Определите напряжение Uab в В, если'):
						
						xpath = '/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/span/input'
						browser.find_element_by_xpath(xpath).clear()
						browser.find_element_by_xpath(xpath).send_keys('70')

					if (question == 'Определите ток на участке цепи в мА, если'):
						
						xpath = '/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/span/input'
						browser.find_element_by_xpath(xpath).clear()
						browser.find_element_by_xpath(xpath).send_keys('5')
					return True

		except Exception as e:
			continue

	
	return False


def q_with_pict():
	question_xpath = '/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[1]/p[2]'
	question = browser.find_element_by_xpath(question_xpath).text
	print(f'{i+1})	' + question)
	time.sleep(1)
	if (question == 'Определить мощность источников в Вт, если '):

		question_xpath = '/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[1]/p[3]'
		question = browser.find_element_by_xpath(question_xpath).text
		print('		' + question)
		if (question == 'J = 9 А,  E1 = 40 В, E2 = 86 В,  R1 = R2 = R3 = R4 = R5  = 9 Ом.'):
			print('индивидуалочка')

		return True

	if (question == 'Определите токи в ветвях, если:'):

		question_xpath = '/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[1]/p[3]'
		question = browser.find_element_by_xpath(question_xpath).text
		print('		' + question)
		if (question == 'E1 = 4 В,  E2 = 2 В,  E3 = 6 В,  J1 = 8 мА,  J2 = 10 мА, '):

			ans_row = []
			for j in range(2,25,2):
				el = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div/span[{j}]').text
				if (el[0] == '‑'): # проверка на то что тире это не минус
					el = '-' + el[1:]
				ans_row.append(int(el))
				# time.sleep(0.1)
			print(ans_row)

			for k in range(6):
				ans_xpath = f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/input[{k+2}]'
				answer = browser.find_element_by_xpath(ans_xpath)
				browser.execute_script("arguments[0].setAttribute('type','text')", answer)
				# print('opened', k+1, 'input for clearing')
				time.sleep(0.2)
				answer.clear()
				if (k == 0):
					answer.send_keys(ans_row.index(2)+1)
				if (k == 1):
					answer.send_keys(ans_row.index(10)+1)
				if (k == 2):
					answer.send_keys(ans_row.index(8)+1)
				if (k == 3):
					answer.send_keys(ans_row.index(-1)+1)
				if (k == 4):
					answer.send_keys(ans_row.index(-9)+1)
				if (k == 5):
					answer.send_keys(ans_row.index(1)+1)

			return True

		if (question == 'E1 = 20 В,  E2 = 24 В,  E3 = 28 В,  Е4 = 30 В,  Е5 = 40 В,'):

			ans_row = []
			for j in range(2,25,2):
				el = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div/span[{j}]').text
				if (el[0] == '‑'): # проверка на то что тире это не минус
					el = '-' + el[1:]
				ans_row.append(int(el))
				# time.sleep(0.1)
			print(ans_row)

			for k in range(6):
				ans_xpath = f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/input[{k+2}]'
				answer = browser.find_element_by_xpath(ans_xpath)
				browser.execute_script("arguments[0].setAttribute('type','text')", answer)
				# print('opened', k+1, 'input for clearing')
				time.sleep(0.2)
				answer.clear()
				if (k == 0):
					answer.send_keys(ans_row.index(10)+1)
				if (k == 1):
					answer.send_keys(ans_row.index(-5)+1)
				if (k == 2):
					answer.send_keys(ans_row.index(-15)+1)
				if (k == 3):
					answer.send_keys(ans_row.index(-13)+1)
				if (k == 4):
					answer.send_keys(ans_row.index(2)+1)
				if (k == 5):
					answer.send_keys(ans_row.index(-3)+1)

			return True

	if (question == 'Для приведенной схемы выберите частичные схемы.'):
		print('дохуя картинок')



		return True

	if (question == 'R1 = R2 = R3 = R4 = R5 = R6 = R7 = 3 кОм'):

		ans_row = []
		for j in range(2,41,2):
			el = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div/span[{j}]').text
			if (el[0] == '‑'): # проверка на то что тире это не минус
				el = '-' + el[1:]
			ans_row.append(el)
			# time.sleep(0.1)
		print(ans_row)

		for k in range(6):
			ans_xpath = f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/input[{k+2}]'
			answer = browser.find_element_by_xpath(ans_xpath)
			browser.execute_script("arguments[0].setAttribute('type','text')", answer)
			# print('opened', k+1, 'input for clearing')
			time.sleep(0.2)
			answer.clear()
			if (k == 0):
				answer.send_keys(ans_row.index('7.5')+1)
			if (k == 1):
				answer.send_keys(ans_row.index('5')+1)
			if (k == 2):
				answer.send_keys(ans_row.index('4.5')+1)
			if (k == 3):
				answer.send_keys(ans_row.index('2')+1)
			if (k == 4):
				answer.send_keys(ans_row.index('4.5')+1)
			if (k == 5):
				answer.send_keys(ans_row.index('2')+1)

		return True



	return False














#############=========================================================================================================================#############







browser = webdriver.Firefox(options = option) #firefox_profile
browser.get('https://eios.sibsutis.ru/')

login_xpath = '//*[@id="username"]'
browser.find_element_by_xpath(login_xpath).send_keys('defersonm@mail.ru')

# time.sleep(2)

password_xpath = '//*[@id="password"]'
browser.find_element_by_id('password').send_keys('777832142Rus#')
# time.sleep(2)

xpath = '//*[@id="loginbtn"]'
browser.find_element_by_xpath(xpath).click()

time.sleep(0.5)

text1 = browser.find_element_by_xpath('/html/body/div[1]/nav/ul[2]/li[2]/div/div/div/div/div/a/span/span[1]').text
print('bot logined by name: ' + text1)


# browser.get(link_na_test)

browser.get('https://eios.sibsutis.ru/mod/quiz/attempt.php?attempt=127854&cmid=55478&page=23') # &page=1




with open('qwe.json', 'r', encoding='utf-8') as file:
	data = json.load(file)

for i in range(28):
	time.sleep(1)
	print(f'=================={i+1}==================')
	check_xpath_img = data['check_xpath_img']

	if (xpath_exist(check_xpath_img)):
		type_q = '1'
		print('vopros s picture v p[1]')
	else:
		type_q = '2'
		print('vopros bez picture v p[1]')

	resolve(data[f'type{type_q}'])


	if (i == 0):
		xpath = '/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[2]/input'
	else:
		xpath = '/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[2]/input[2]'
	browser.find_element_by_xpath(xpath).click()

	continue

	print('exit')
	exit(0)




	time.sleep(1)
	check_xpath_img = '/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[1]/p[1]/img'
	check_xpath = '/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[1]/p[1]'

	if (not xpath_exist(check_xpath_img) and xpath_exist(check_xpath)):
		question_xpath = '/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[1]/p[1]'
		question = browser.find_element_by_xpath(question_xpath).text
		print(f'{i+1})	' + question)
		if (question == 'Составьте систему уравнений по методу узловых напряжений для приведенной схемы'):

			# ans_row = []
			# for k in range(36):
			# 	ans_xpath = f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/input[{k+2}]'
			# 	answer = browser.find_element_by_xpath(ans_xpath)
			# 	browser.execute_script("arguments[0].setAttribute('type','text')", answer)
			# 	# print('opened', k+1, 'input for clearing')
			# 	time.sleep(0.2)
			# 	answer.clear()
			# 	answer.send_keys('0') # предварительно очищать строки необязательно

			# # не очищает
			# # browser.refresh()
			# refresh_browser()

			

			# for j in range(2,17,2):
			# 	ans_row.append(int(browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div/span[{j}]').text))
			# 	# time.sleep(0.1)
			# print(ans_row)

			
			for k in range(36):
				# пример лаконичного кода
				ans_xpath = f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/input[{k+2}]'
				answer = browser.find_element_by_xpath(ans_xpath)
				browser.execute_script("arguments[0].setAttribute('type','text')", answer)
				# print('opened', k+1, 'input for clearing')
				time.sleep(0.2)
				answer.clear()
				if (k == 0):
					answer.send_keys(1)
				if (k == 1):
					answer.send_keys(1)
				if (k == 2):
					answer.send_keys(2)
				if (k == 3):
					answer.send_keys(5)
				if (k == 4):
					answer.send_keys(2)
				if (k == 5):
					answer.send_keys(6)
				if (k == 6):
					answer.send_keys(2)
				if (k == 7):
					answer.send_keys(7)
				if (k == 8):
					answer.send_keys(1)
				if (k == 9):
					answer.send_keys(2)
				if (k == 10):
					answer.send_keys(5)
				if (k == 11):
					answer.send_keys(1)
				if (k == 12):
					answer.send_keys(2)
				if (k == 13):
					answer.send_keys(2)
				if (k == 14):
					answer.send_keys(8)
				if (k == 15):
					answer.send_keys(2)
				if (k == 16):
					answer.send_keys(9)
				if (k == 17):
					answer.send_keys(2)
				if (k == 18):
					answer.send_keys(2)
				if (k == 19):
					answer.send_keys(6)
				if (k == 20):
					answer.send_keys(2)
				if (k == 21):
					answer.send_keys(8)
				if (k == 22):
					answer.send_keys(1)
				if (k == 23):
					answer.send_keys(3)
				if (k == 24):
					answer.send_keys(2)
				if (k == 25):
					answer.send_keys(10)
				if (k == 26):
					answer.send_keys(3)
				if (k == 27):
					answer.send_keys(2)
				if (k == 28):
					answer.send_keys(7)
				if (k == 29):
					answer.send_keys(2)
				if (k == 30):
					answer.send_keys(9)
				if (k == 31):
					answer.send_keys(2)
				if (k == 32):
					answer.send_keys(10)
				if (k == 33):
					answer.send_keys(1)
				if (k == 34):
					answer.send_keys(4)
				if (k == 35):
					answer.send_keys(4)

		if (question == 'В результате анализа работы электрической цепи исходная схема была преобразована в схему с эквивалентным генератором тока'):

			question_xpath = '/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[1]/p[3]'
			question = browser.find_element_by_xpath(question_xpath).text
			print('		' + question)
			if (question == 'Jкз = 42 мА,  RэгJ = 6 кОм,  Rн = 12 кОм.'):

				ans_row = []
				for j in range(2,25,2):
					el = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div/span[{j}]').text
					if (el[0] == '‑'): # проверка на то что тире это не минус
						el = '-' + el[1:]
					ans_row.append(int(el))
					# time.sleep(0.1)
				print(ans_row)

				for k in range(3):
					ans_xpath = f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/input[{k+2}]'
					answer = browser.find_element_by_xpath(ans_xpath)
					browser.execute_script("arguments[0].setAttribute('type','text')", answer)
					# print('opened', k+1, 'input for clearing')
					time.sleep(0.2)
					answer.clear()
					if (k == 0):
						answer.send_keys(ans_row.index(14)+1)
					if (k == 1):
						answer.send_keys(ans_row.index(6)+1)
					if (k == 2):
						answer.send_keys(ans_row.index(252)+1)

		if (question == 'По заданной схеме определите: '):
			for x in range(6):
				# '/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[1]/td[1]'
				# '/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[4]/td[1]/p'
				quest = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[{x+1}]/td[1]').text
				print(quest)
				max_sel = 9
				if (quest == 'Количество уравнений по первому закону Кирхгофа'):
					for k in range(max_sel):
						if (browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[{x+1}]/td[2]/select/option[{k+1}]').text == '4'):
							print('detected		' + browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[{x+1}]/td[2]/select/option[{k+1}]').text)
							answer = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[{x+1}]/td[2]/select/option[{k+1}]')
							browser.execute_script("arguments[0].setAttribute('selected','selected')", answer)
							break
				if (quest == 'Количество уравнений по второму закону Кирхгофа'):
					for k in range(max_sel):
						if (browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[{x+1}]/td[2]/select/option[{k+1}]').text == '2'):
							print('detected		' + browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[{x+1}]/td[2]/select/option[{k+1}]').text)
							answer = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[{x+1}]/td[2]/select/option[{k+1}]')
							browser.execute_script("arguments[0].setAttribute('selected','selected')", answer)
							break
				if (quest == 'Количество частичных схем по методу наложения'):
					for k in range(max_sel):
						if (browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[{x+1}]/td[2]/select/option[{k+1}]').text == '5'):
							print('detected		' + browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[{x+1}]/td[2]/select/option[{k+1}]').text)
							answer = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[{x+1}]/td[2]/select/option[{k+1}]')
							browser.execute_script("arguments[0].setAttribute('selected','selected')", answer)
							break
				if (quest == 'Количество неизвестных токов в схеме'):
					for k in range(max_sel):
						if (browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[{x+1}]/td[2]/select/option[{k+1}]').text == '6'):
							print('detected		' + browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[{x+1}]/td[2]/select/option[{k+1}]').text)
							answer = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[{x+1}]/td[2]/select/option[{k+1}]')
							browser.execute_script("arguments[0].setAttribute('selected','selected')", answer)
							break
				if (quest == 'Количество уравнений по методу контурных токов'):
					for k in range(max_sel):
						if (browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[{x+1}]/td[2]/select/option[{k+1}]').text == '2'):
							print('detected		' + browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[{x+1}]/td[2]/select/option[{k+1}]').text)
							answer = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[{x+1}]/td[2]/select/option[{k+1}]')
							browser.execute_script("arguments[0].setAttribute('selected','selected')", answer)
							break
				if (quest == 'Количество уравнений по методу узловых напряжений'):
					for k in range(max_sel):
						if (browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[{x+1}]/td[2]/select/option[{k+1}]').text == '3'):
							print('detected		' + browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[{x+1}]/td[2]/select/option[{k+1}]').text)
							answer = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[{x+1}]/td[2]/select/option[{k+1}]')
							browser.execute_script("arguments[0].setAttribute('selected','selected')", answer)
							break

		if (question == 'Частичная схема - это'):
			for k in range(5):
				if (browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/div/div/p').text[-3:] == 'ия '):
					print('detected		' + browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/div/div/p').text)
					answer = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/input')
					answer.click()
					# browser.execute_script("arguments[0].setAttribute('checked','checked')", answer)

		if (question == 'При определении сопротивления эквивалентного генератора исследуемая схема заменяется на'):
			for k in range(4):
				if (browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/div/div/p').text == 'пассивный двухполюсник'):
					print('detected		' + browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/div/div/p').text)
					answer = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/input')
					answer.click()
					# browser.execute_script("arguments[0].setAttribute('checked','checked')", answer)


	elif(xpath_exist(check_xpath_img)):
		img_el = browser.find_element_by_xpath(check_xpath_img)
		img_url = img_el.get_attribute('src')
		# print(img_url)

		element = browser.find_element_by_xpath('/html/body/div[1]/div[2]/header/div/div/div/div[2]/div[1]/nav/ol/li[10]/a')
		browser.execute_script(f"arguments[0].setAttribute('href','{img_url}')", element)
		browser.execute_script("arguments[0].setAttribute('download','current_pict.png')", element)
		element.click()

		for file in os.listdir("C:\\progs\\bot_for_test"):
			if (file.endswith('.png')):
				print(file)
				break
		# shutil.move(file, 'current_pict.png')

		# перебираем изображения в папке
		result = compare_pict(file)

		# удаляет текущую картинку
		os.remove(file)

		if (not result):
			q_with_pict()



	else:
		# При расчете схемы методом законов Кирхгофа число уравнений по первому закону Кирхгофа равно
		for k in range(5):
			if (browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/div/div/p').text == 'числу узлов минус один'):
				print('detected		' + browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/div/div/p').text)
				answer = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/input')
				answer.click()
				# browser.execute_script("arguments[0].setAttribute('checked','checked')", answer)



	if (i == 0):
		xpath = '/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[2]/input'
	else:
		xpath = '/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[2]/input[2]'
	browser.find_element_by_xpath(xpath).click()

print('successfully finished')