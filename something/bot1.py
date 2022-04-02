import time
import os
import shutil
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
# import requests
from PIL import Image, ImageChops
import cv2
# import urllib.request

test = 1

# print('ссылка на тест')
# link_na_test = input()

option = webdriver.FirefoxOptions()
option.set_preference('dom.webdriver.enabled', False)
option.set_preference('dom.webnotifications.enabled', False)
option.set_preference('general.useragent.override', 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0')
option.set_preference("browser.download.folderList",2)
option.set_preference("browser.download.manager.showWhenStarting",False)
option.set_preference("browser.download.dir", 'C:\\progs\\бот для тестов')
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
	



def compare_pict(file):
	for x in range(5):
		img1 = Image.open(file)
		img2 = Image.open(f'picts_test1\\{x}.png')
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


				if (x == 1):
					question_xpath = '/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[1]/p[2]'
					question = browser.find_element_by_xpath(question_xpath).text
					print(f'{i+1})	' + question)
					# print(question)

					if (question == 'Определите напряжение Uab в В, если'):
						
						xpath = '/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/span/input'
						browser.find_element_by_xpath(xpath).clear()
						browser.find_element_by_xpath(xpath).send_keys('-20')

					if (question == 'Определите ток на участке цепи в мА, если'):

						xpath = '/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/span/input'
						browser.find_element_by_xpath(xpath).clear()
						browser.find_element_by_xpath(xpath).send_keys('-1')
					return True

				if (x == 2):
					
					ans_row = []
					for k in range(6):
						ans_xpath = f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/input[{k+2}]'
						answer = browser.find_element_by_xpath(ans_xpath)
						browser.execute_script("arguments[0].setAttribute('type','text')", answer)
						print('opened', k+1, 'input for clearing')
						time.sleep(0.2)
						answer.clear()
						answer.send_keys('0')

					# не очищает
					# browser.refresh()
					refresh_browser()


					for j in range(2,19,2):
						ans_row.append(int(browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div/span[{j}]').text))
						# time.sleep(0.1)
					print(ans_row)

					
					for k in range(6):
						ans_xpath = f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/input[{k+2}]'
						answer = browser.find_element_by_xpath(ans_xpath)
						browser.execute_script("arguments[0].setAttribute('type','text')", answer)
						print('opened', k+1, 'input for answer')
						time.sleep(0.2)
						answer.clear()
						if (k == 0):
							answer.send_keys(ans_row.index(3)+1)
						if (k == 1):
							answer.send_keys(ans_row.index(5)+1)
						if (k == 2):
							answer.send_keys(ans_row.index(1)+1)
						if (k == 3):
							answer.send_keys(ans_row.index(1)+1)
						if (k == 4):
							answer.send_keys(ans_row.index(3)+1)
						if (k == 5):
							answer.send_keys(ans_row.index(2)+1)
					return True

				if (x == 3):
					
					ans_row = []
					for k in range(6):
						ans_xpath = f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/input[{k+2}]'
						answer = browser.find_element_by_xpath(ans_xpath)
						browser.execute_script("arguments[0].setAttribute('type','text')", answer)
						print('opened', k+1, 'input for clearing')
						time.sleep(0.2)
						answer.clear()
						answer.send_keys('0')

					# не очищает
					# browser.refresh()
					refresh_browser()


					for j in range(2,19,2):
						ans_row.append(int(browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div/span[{j}]').text))
						# time.sleep(0.1)
					print(ans_row)

					
					for k in range(6):
						ans_xpath = f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/input[{k+2}]'
						answer = browser.find_element_by_xpath(ans_xpath)
						browser.execute_script("arguments[0].setAttribute('type','text')", answer)
						print('opened', k+1, 'input for answer')
						time.sleep(0.2)
						answer.clear()
						if (k == 0):
							answer.send_keys(ans_row.index(4)+1)
						if (k == 1):
							answer.send_keys(ans_row.index(6)+1)
						if (k == 2):
							answer.send_keys(ans_row.index(2)+1)
						if (k == 3):
							answer.send_keys(ans_row.index(2)+1)
						if (k == 4):
							answer.send_keys(ans_row.index(3)+1)
						if (k == 5):
							answer.send_keys(ans_row.index(1)+1)
					return True

				if (x == 4):
					
					ans_row = []
					for k in range(6):
						ans_xpath = f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/input[{k+2}]'
						answer = browser.find_element_by_xpath(ans_xpath)
						browser.execute_script("arguments[0].setAttribute('type','text')", answer)
						print('opened', k+1, 'input for clearing')
						time.sleep(0.2)
						answer.clear()
						answer.send_keys('0')

					# не очищает
					# browser.refresh()
					refresh_browser()


					for j in range(2,19,2):
						ans_row.append(int(browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div/span[{j}]').text))
						# time.sleep(0.1)
					print(ans_row)

					
					for k in range(6):
						ans_xpath = f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/input[{k+2}]'
						answer = browser.find_element_by_xpath(ans_xpath)
						browser.execute_script("arguments[0].setAttribute('type','text')", answer)
						print('opened', k+1, 'input for answer')
						time.sleep(0.2)
						answer.clear()
						if (k == 0):
							answer.send_keys(ans_row.index(4)+1)
						if (k == 1):
							answer.send_keys(ans_row.index(6)+1)
						if (k == 2):
							answer.send_keys(ans_row.index(2)+1)
						if (k == 3):
							answer.send_keys(ans_row.index(1)+1)
						if (k == 4):
							answer.send_keys(ans_row.index(3)+1)
						if (k == 5):
							answer.send_keys(ans_row.index(2)+1)
					return True


		except Exception as e:
			continue

	
	return False







def q_with_pict():
	question_xpath = '/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[1]/p[2]'
	question = browser.find_element_by_xpath(question_xpath).text
	print(f'{i+1})	' + question)
	time.sleep(1)
	# задача про перетаскивание
	# if (question == 'Для приведенной схемы определить'):
	# 	ans_row = []
	# 	for k in range(6):
	# 		if (xpath_exist(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[1]/p[{k+3}]/span[2]')):
	# 			answer = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/input[{k+2}]')

	# 			browser.execute_script("arguments[0].setAttribute('type','text')", answer)
	# 			print('opened', k+1, 'input for clearing')
	# 			time.sleep(0.2)
	# 			answer.clear()
	# 			answer.send_keys('0')

	# 	# не очищает
	# 	# browser.refresh()
	# 	refresh_browser()

	# 	for j in range(2,19,2):
	# 		ans_row.append(int(browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div/span[{j}]').text))
	# 		# time.sleep(0.1)
	# 	print(ans_row)
	# 	for k in range(6):
	# 		answer = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[1]/p[{k+3}]')
	# 		browser.execute_script("arguments[0].setAttribute('class','')", answer)
	# 		print(browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[1]/p[{k+3}]').text)
	# 		print(ans_row.index(3))
	# 		if (browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[1]/p[{k+3}]').text == '1. Количество узлов  \nпусто'):
	# 			print('read 1 question')
	# 			answer = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/input[{k+2}]')

	# 			browser.execute_script("arguments[0].setAttribute('type','text')", answer)
	# 			time.sleep(0.2)
	# 			answer.clear()
	# 			answer.send_keys(ans_row.index(3)+1)
	# 			print(ans_row.index(3)+1)
	# 		if (browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[1]/p[{k+3}]').text == '2. Количество ветвей  \nпусто'):
	# 			print('read 2 question')
	# 			answer = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/input[{k+2}]')

	# 			browser.execute_script("arguments[0].setAttribute('type','text')", answer)
	# 			time.sleep(0.2)
	# 			answer.clear()
	# 			answer.send_keys(ans_row.index(5)+1)
	# 			print(ans_row.index(5)+1)
	# 		if (browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[1]/p[{k+3}]').text == '3. Количество источников ЭДС  \nпусто'):
	# 			print('read 3 question')
	# 			answer = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/input[{k+2}]')

	# 			browser.execute_script("arguments[0].setAttribute('type','text')", answer)
	# 			time.sleep(0.2)
	# 			answer.clear()
	# 			answer.send_keys(ans_row.index(1)+1)
	# 			print(ans_row.index(1)+1)
	# 		if (browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[1]/p[{k+3}]').text == '4. Количество источников тока  \nпусто'):
	# 			print('read 4 question')
	# 			answer = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/input[{k+2}]')

	# 			browser.execute_script("arguments[0].setAttribute('type','text')", answer)
	# 			time.sleep(0.2)
	# 			answer.clear()
	# 			answer.send_keys(ans_row.index(1)+1)
	# 			print(ans_row.index(1)+1)
	# 		if (browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[1]/p[{k+3}]').text == '5. Количество независимых контуров  \nпусто'):
	# 			print('read 5 question')
	# 			answer = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/input[{k+2}]')

	# 			browser.execute_script("arguments[0].setAttribute('type','text')", answer)
	# 			time.sleep(0.2)
	# 			answer.clear()
	# 			answer.send_keys(ans_row.index(3)+1)
	# 			print(ans_row.index(3)+1)
	# 		if (browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[1]/p[{k+3}]').text == '6. Количество независимых контуров без источников тока  \nпусто'):
	# 			print('read 6 question')
	# 			answer = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/input[{k+2}]')

	# 			browser.execute_script("arguments[0].setAttribute('type','text')", answer)
	# 			time.sleep(0.2)
	# 			answer.clear()
	# 			answer.send_keys(ans_row.index(2)+1)
	# 			print(ans_row.index(2)+1)
	# 	return True


	if (question == 'Определить токи в ветвях схемы, если'):
		question_xpath = '/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[1]/p[3]'
		question = browser.find_element_by_xpath(question_xpath).text
		print(question)
		if (question == 'J = 5 мА, R1 = 8 кОм, R2 = 6 кОм, R3 = 4 кОм.'):
			ans_row = []
			for k in range(3):
				ans_xpath = f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/input[{k+2}]'
				answer = browser.find_element_by_xpath(ans_xpath)
				browser.execute_script("arguments[0].setAttribute('type','text')", answer)
				print('opened', k+1, 'input for clearing')
				time.sleep(0.2)
				answer.clear()
				answer.send_keys('0') # предварительно очищать строки необязательно

			# не очищает
			# browser.refresh()
			refresh_browser()

			

			for j in range(2,17,2):
				ans_row.append(int(browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div/span[{j}]').text))
				# time.sleep(0.1)
			print(ans_row)

			
			for k in range(3):
				# пример лаконичного кода
				ans_xpath = f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/input[{k+2}]'
				answer = browser.find_element_by_xpath(ans_xpath)
				browser.execute_script("arguments[0].setAttribute('type','text')", answer)
				print('opened', k+1, 'input for clearing')
				time.sleep(0.2)
				answer.clear()
				if (k == 0):
					answer.send_keys(ans_row.index(5)+1)
				if (k == 1):
					answer.send_keys(ans_row.index(2)+1)
				if (k == 2):
					answer.send_keys(ans_row.index(3)+1)
			


				# пример грязного кода
				# answer = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[1]/p[{k+3}]')
				# browser.execute_script("arguments[0].setAttribute('class','')", answer)
				# print(browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[1]/p[{k+3}]').text)
				# print(ans_row.index(3))
				# if (browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[1]/p[{k+3}]').text == '1. Количество узлов  \nпусто'):
				# 	print('read 1 question')
				# 	answer = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/input[{k+2}]')

				# 	browser.execute_script("arguments[0].setAttribute('type','text')", answer)
				# 	time.sleep(0.2)
				# 	answer.clear()
				# 	answer.send_keys(ans_row.index(3)+1)
				# 	print(ans_row.index(3)+1)
				# if (browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[1]/p[{k+3}]').text == '2. Количество ветвей  \nпусто'):
				# 	print('read 2 question')
				# 	answer = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/input[{k+2}]')

				# 	browser.execute_script("arguments[0].setAttribute('type','text')", answer)
				# 	time.sleep(0.2)
				# 	answer.clear()
				# 	answer.send_keys(ans_row.index(5)+1)
				# 	print(ans_row.index(5)+1)
				# if (browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[1]/p[{k+3}]').text == '3. Количество источников ЭДС  \nпусто'):
				# 	print('read 3 question')
				# 	answer = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/input[{k+2}]')

				# 	browser.execute_script("arguments[0].setAttribute('type','text')", answer)
				# 	time.sleep(0.2)
				# 	answer.clear()
				# 	answer.send_keys(ans_row.index(1)+1)
				# 	print(ans_row.index(1)+1)
				# if (browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[1]/p[{k+3}]').text == '4. Количество источников тока  \nпусто'):
				# 	print('read 4 question')
				# 	answer = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/input[{k+2}]')

				# 	browser.execute_script("arguments[0].setAttribute('type','text')", answer)
				# 	time.sleep(0.2)
				# 	answer.clear()
				# 	answer.send_keys(ans_row.index(1)+1)
				# 	print(ans_row.index(1)+1)
				# if (browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[1]/p[{k+3}]').text == '5. Количество независимых контуров  \nпусто'):
				# 	print('read 5 question')
				# 	answer = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/input[{k+2}]')

				# 	browser.execute_script("arguments[0].setAttribute('type','text')", answer)
				# 	time.sleep(0.2)
				# 	answer.clear()
				# 	answer.send_keys(ans_row.index(3)+1)
				# 	print(ans_row.index(3)+1)
				# if (browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[1]/p[{k+3}]').text == '6. Количество независимых контуров без источников тока  \nпусто'):
				# 	print('read 6 question')
				# 	answer = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/input[{k+2}]')

				# 	browser.execute_script("arguments[0].setAttribute('type','text')", answer)
				# 	time.sleep(0.2)
				# 	answer.clear()
				# 	answer.send_keys(ans_row.index(2)+1)
				# 	print(ans_row.index(2)+1)




	# if (question == 'Определить токи в ветвях схемы, если'):
	# 	question_xpath = '/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[1]/p[3]'
	# 	question = browser.find_element_by_xpath(question_xpath).text
		print(question)
		if (question == 'Е = 6 В, R1 = 1 кОм, R2 = 3 кОм.'):
			ans_row = []
			for k in range(3):
				ans_xpath = f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/input[{k+2}]'
				answer = browser.find_element_by_xpath(ans_xpath)
				browser.execute_script("arguments[0].setAttribute('type','text')", answer)
				print('opened', k+1, 'input for clearing')
				time.sleep(0.2)
				answer.clear()
				answer.send_keys('0')

			# не очищает
			# browser.refresh()
			refresh_browser()


			for j in range(2,19,2):
				ans_row.append(int(browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div/span[{j}]').text))
				# time.sleep(0.1)
			print(ans_row)

			
			for k in range(3):
				ans_xpath = f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/input[{k+2}]'
				answer = browser.find_element_by_xpath(ans_xpath)
				browser.execute_script("arguments[0].setAttribute('type','text')", answer)
				print('opened', k+1, 'input for answer')
				time.sleep(0.2)
				answer.clear()
				if (k == 0):
					answer.send_keys(ans_row.index(8)+1)
				if (k == 1):
					answer.send_keys(ans_row.index(6)+1)
				if (k == 2):
					answer.send_keys(ans_row.index(2)+1)
		return True


	if (question == 'Определите значение источника энергии Е1 в В, если'):
		question_xpath = '/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[1]/p[3]'
		question = browser.find_element_by_xpath(question_xpath).text
		print(question)
		
		if (question == 'I = 3 мА,   E2 = 12 В,  R1 = 7 кОм, R2 = 9 кОм.'):
			ans_xpath = f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/span/input'
			answer = browser.find_element_by_xpath(ans_xpath)
			time.sleep(0.2)
			answer.clear()
			answer.send_keys('60')
			return True

		if (question == 'I = 8 мА,   E2 = 70 В,  R1 = 5 кОм, R2 = 7 кОм, R3 = 8 кОм.'):
			ans_xpath = f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/span/input'
			answer = browser.find_element_by_xpath(ans_xpath)
			time.sleep(0.2)
			answer.clear()
			answer.send_keys('90')
			return True


	if (question == 'Определить токи в ветвях схемы, если '):
		question_xpath = '/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[1]/p[3]'
		question = browser.find_element_by_xpath(question_xpath).text
		print(question)
		if (question == 'J = 20 мА,  R1= 10 кОм, R2 = 10 кОм,  R3 = 5 кОм.'):
			ans_row = []
			for k in range(4):
				ans_xpath = f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/input[{k+2}]'
				answer = browser.find_element_by_xpath(ans_xpath)
				browser.execute_script("arguments[0].setAttribute('type','text')", answer)
				print('opened', k+1, 'input for clearing')
				time.sleep(0.2)
				answer.clear()
				answer.send_keys('0') # предварительно очищать строки необязательно

			# не очищает
			# browser.refresh()
			refresh_browser()

			for j in range(2,19,2):
				ans_row.append(int(browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div/span[{j}]').text))
				# time.sleep(0.1)
			print(ans_row)

			
			for k in range(4):
				# пример лаконичного кода
				ans_xpath = f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/input[{k+2}]'
				answer = browser.find_element_by_xpath(ans_xpath)
				browser.execute_script("arguments[0].setAttribute('type','text')", answer)
				print('opened', k+1, 'input for clearing')
				time.sleep(0.2)
				answer.clear()
				if (k == 0):
					answer.send_keys(ans_row.index(5)+1)
				if (k == 1):
					answer.send_keys(ans_row.index(5)+1)
				if (k == 2):
					answer.send_keys(ans_row.index(10)+1)
				if (k == 3):
					answer.send_keys(ans_row.index(20)+1)
		return True


	if (question == ''):
		question_xpath = '/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[1]/p[4]'
		question = browser.find_element_by_xpath(question_xpath).text
		print(question)

		if (question == 'Е = 10 В, R1 = 1 Ом,  R2 = 3 Ом,  R3 =  4 Ом, R4 = 1 Ом,  R5 = 2 Ом.'):
			ans_row = []
			for k in range(4):
				ans_xpath = f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/input[{k+2}]'
				answer = browser.find_element_by_xpath(ans_xpath)
				browser.execute_script("arguments[0].setAttribute('type','text')", answer)
				print('opened', k+1, 'input for clearing')
				time.sleep(0.2)
				answer.clear()
				answer.send_keys('0') # предварительно очищать строки необязательно

			# не очищает
			# browser.refresh()
			refresh_browser()

			for j in range(2,23,2):
				el = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div/span[{j}]').text
				if (el[0] == '‑'): # дополнительная проверка на то что '‑' не является '-'
					el = '-' + el[1]
				ans_row.append(int(el))
				# time.sleep(0.1)
			print(ans_row)
			
			
			for k in range(4):
				# пример лаконичного кода
				ans_xpath = f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/input[{k+2}]'
				answer = browser.find_element_by_xpath(ans_xpath)
				browser.execute_script("arguments[0].setAttribute('type','text')", answer)
				print('opened', k+1, 'input for clearing')
				time.sleep(0.2)
				answer.clear()
				if (k == 0):
					answer.send_keys(ans_row.index(2)+1)
				if (k == 1):
					answer.send_keys(ans_row.index(1)+1)
				if (k == 2):
					answer.send_keys(ans_row.index(4)+1)
				if (k == 3):
					answer.send_keys(ans_row.index(6)+1)
			return True

		if (question == 'Е1 = 60 В,   E2 = 12 В,  R1 = 7 кОм, R2 = 9 кОм.'):
			ans_row = []
			for k in range(2):
				ans_xpath = f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/input[{k+2}]'
				answer = browser.find_element_by_xpath(ans_xpath)
				browser.execute_script("arguments[0].setAttribute('type','text')", answer)
				print('opened', k+1, 'input for clearing')
				time.sleep(0.2)
				answer.clear()
				answer.send_keys('0') # предварительно очищать строки необязательно

			# не очищает
			# browser.refresh()
			refresh_browser()

			for j in range(2,19,2):
				el = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div/span[{j}]').text
				if (el[0] == '‑'): # дополнительная проверка на то что '‑' не является '-'
					el = '-' + el[1:]
				ans_row.append(int(el))
				# time.sleep(0.1)
			print(ans_row)
			
			
			for k in range(2):
				# пример лаконичного кода
				ans_xpath = f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/input[{k+2}]'
				answer = browser.find_element_by_xpath(ans_xpath)
				browser.execute_script("arguments[0].setAttribute('type','text')", answer)
				print('opened', k+1, 'input for clearing')
				time.sleep(0.2)
				answer.clear()
				if (k == 0):
					answer.send_keys(ans_row.index(180)+1)
				if (k == 1):
					answer.send_keys(ans_row.index(-36)+1)
			return True


		if (question == 'Е = 10 В, R1 = 2 Ом,  R2 = 3 Ом,  R3 =  5 Ом.'):
			ans_row = []
			for k in range(4):
				ans_xpath = f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/input[{k+2}]'
				answer = browser.find_element_by_xpath(ans_xpath)
				browser.execute_script("arguments[0].setAttribute('type','text')", answer)
				print('opened', k+1, 'input for clearing')
				time.sleep(0.2)
				answer.clear()
				answer.send_keys('0') # предварительно очищать строки необязательно

			# не очищает
			# browser.refresh()
			refresh_browser()

			for j in range(2,19,2):
				el = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div/span[{j}]').text
				if (el[0] == '‑'): # дополнительная проверка на то что '‑' не является '-'
					el = '-' + el[1:]
				ans_row.append(int(el))
				# time.sleep(0.1)
			print(ans_row)
			
			
			for k in range(4):
				# пример лаконичного кода
				ans_xpath = f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/input[{k+2}]'
				answer = browser.find_element_by_xpath(ans_xpath)
				browser.execute_script("arguments[0].setAttribute('type','text')", answer)
				print('opened', k+1, 'input for clearing')
				time.sleep(0.2)
				answer.clear()
				if (k == 0):
					answer.send_keys(ans_row.index(-10)+1)
				if (k == 1):
					answer.send_keys(ans_row.index(3)+1)
				if (k == 2):
					answer.send_keys(ans_row.index(5)+1)
				if (k == 3):
					answer.send_keys(ans_row.index(-5)+1)
			return True


	if (question == 'Определить мощность на резисторах, если'):
		question_xpath = '/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[1]/p[3]'
		question = browser.find_element_by_xpath(question_xpath).text
		print(question)
		if (question == 'E = 20 В, R1 = 2 Ом, R2 = 3 Ом, R3 = 5 Ом.'):
			ans_row = []
			for k in range(3):
				ans_xpath = f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/input[{k+2}]'
				answer = browser.find_element_by_xpath(ans_xpath)
				browser.execute_script("arguments[0].setAttribute('type','text')", answer)
				print('opened', k+1, 'input for clearing')
				time.sleep(0.2)
				answer.clear()
				answer.send_keys('0') # предварительно очищать строки необязательно

			# не очищает
			# browser.refresh()
			refresh_browser()

			for j in range(2,19,2):
				ans_row.append(int(browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div/span[{j}]').text))
				# time.sleep(0.1)
			print(ans_row)

			
			for k in range(3):
				# пример лаконичного кода
				ans_xpath = f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/input[{k+2}]'
				answer = browser.find_element_by_xpath(ans_xpath)
				browser.execute_script("arguments[0].setAttribute('type','text')", answer)
				print('opened', k+1, 'input for clearing')
				time.sleep(0.2)
				answer.clear()
				if (k == 0):
					answer.send_keys(ans_row.index(8)+1)
				if (k == 1):
					answer.send_keys(ans_row.index(12)+1)
				if (k == 2):
					answer.send_keys(ans_row.index(20)+1)
		return True


	if (question == 'Определить ток в ветви с источником  в мА, если'):
		question_xpath = '/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[1]/p[3]'
		question = browser.find_element_by_xpath(question_xpath).text
		print(question)
		
		if (question == 'Е = 24 В, R1 = 2 кОм, R2 = 10 кОм, R3 = 5 кОм, R4 = 8 кОм, R5 = 2 кОм.'):
			ans_xpath = f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/span/input'
			answer = browser.find_element_by_xpath(ans_xpath)
			time.sleep(0.2)
			answer.clear()
			answer.send_keys('4')
			return True

		if (question == 'Е = 50 В, R1 = 3 кОм, R2 = 2 кОм, R3 = 10 кОм, R4 = 8 кОм, R5 = 2 кОм.'):
			ans_xpath = f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/span/input'
			answer = browser.find_element_by_xpath(ans_xpath)
			time.sleep(0.2)
			answer.clear()
			answer.send_keys('5')
			return True


	if (question == 'Определите ток в контуре в мА, если'):
		question_xpath = '/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[1]/p[3]'
		question = browser.find_element_by_xpath(question_xpath).text
		print(question)
		
		if (question == 'E1 = 28 В,   E2 = 12 В,  R1 = 1 кОм, R2 = 3 кОм.'):
			ans_xpath = f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/span/input'
			answer = browser.find_element_by_xpath(ans_xpath)
			time.sleep(0.2)
			answer.clear()
			answer.send_keys('4')
			return True
		
		if (question == 'E1 = 28 В,   E2 = 12 В,  R1 = 14 кОм, R2 = 8 кОм, R3 = 18 кОм.'):
			ans_xpath = f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/span/input'
			answer = browser.find_element_by_xpath(ans_xpath)
			time.sleep(0.2)
			answer.clear()
			answer.send_keys('1')
			return True
		

	if (question == 'Определить показания измерительных приборов'): # Е = 12 В
		ans_row = []
		for k in range(2):
			ans_xpath = f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/input[{k+2}]'
			answer = browser.find_element_by_xpath(ans_xpath)
			browser.execute_script("arguments[0].setAttribute('type','text')", answer)
			print('opened', k+1, 'input for clearing')
			time.sleep(0.2)
			answer.clear()
			answer.send_keys('0') # предварительно очищать строки необязательно

		# не очищает
		# browser.refresh()
		refresh_browser()

		for j in range(2,19,2):
			ans_row.append(int(browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div/span[{j}]').text))
			# time.sleep(0.1)
		print(ans_row)

		
		for k in range(2):
			# пример лаконичного кода
			ans_xpath = f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/input[{k+2}]'
			answer = browser.find_element_by_xpath(ans_xpath)
			browser.execute_script("arguments[0].setAttribute('type','text')", answer)
			print('opened', k+1, 'input for answer')
			time.sleep(0.2)
			answer.clear()
			if (k == 0):
				answer.send_keys(ans_row.index(2)+1)
			if (k == 1):
				answer.send_keys(ans_row.index(9)+1)
		return True
		print('выход из проги')
		exit(0)

	return False

#############=========================================================================================================================#############







browser = webdriver.Firefox(options = option) #firefox_profile
browser.get('https://eios.sibsutis.ru/')

# cookies = {'name': 'MoodleSession', 'value': 'eca04mnko3h5g4frsavvnf3dmo', 'path': '/', 'domain': 'eios.sibsutis.ru', 'secure': True, 'httpOnly': False, 'sameSite': 'None'}
# for cookie in cookies:
# 	browser.add_cookie(cookie)

# time.sleep(2)

# browser.refresh()


login_xpath = '//*[@id="username"]'
browser.find_element_by_xpath(login_xpath).send_keys('domnichev5050@gmail.com')

# time.sleep(2)

password_xpath = '//*[@id="password"]'
browser.find_element_by_id('password').send_keys('Eios*00top')
# time.sleep(2)

xpath = '//*[@id="loginbtn"]'
browser.find_element_by_xpath(xpath).click()

time.sleep(0.5)

text1 = browser.find_element_by_xpath('/html/body/div[1]/nav/ul[2]/li[2]/div/div/div/div/div/a/span/span[1]').text
print('bot logined by name: ' + text1)

# old = [{'name': 'MoodleSession', 'value': 'd4q0flhnuksn1h2ast603ocat1', 'path': '/', 'domain': 'eios.sibsutis.ru', 'secure': True, 'httpOnly': False, 'sameSite': 'None'}]
# new = browser.get_cookies()
# print(new)
# print(old == new)
# browser.quit()

# https://eios.sibsutis.ru/mod/quiz/attempt.php?attempt=273157&cmid=46863

if (test == 1):
	# browser.get(link_na_test) # &page=1
	url_test = 'https://eios.sibsutis.ru/mod/quiz/attempt.php?attempt=273383&cmid=78843' # &page=1

	print('vvodniy test? da/net')
	nado = input()
	if nado == 'da':
		browser.get('https://eios.sibsutis.ru/mod/quiz/attempt.php?attempt=273383&cmid=78843')
		# time.sleep(1)
		# WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/section/div[1]/div[3]/div/form/button"))).click()

		# print(browser.window_handles)

		# browser.switch_to.window(browser.window_handles[1])

		# print(browser.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div[1]/section/div/div/div/form/div/div[1]/div[2]/div/div[1]').text)
		# el = WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[1]/section/div/div/div/form/div/div[1]/div[2]/div/div[1]"))).text
		# print(el)
	else:
		browser.get(url_test)

	for i in range(1):

		time.sleep(1)
		check_xpath = '/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[1]/p[1]/img'
		check_xpath1 = '/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[1]/p[1]'

		if (not xpath_exist(check_xpath) and xpath_exist(check_xpath1)):
			question_xpath = '/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[1]/p[1]'
			question = browser.find_element_by_xpath(question_xpath).text
			print(f'{i+1})	' + question)

			if (question == 'Выберите правильные утверждения.'):
				question_xpath = '/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[1]/p[2]'
				question = browser.find_element_by_xpath(question_xpath).text
				print('		' + question)
				if (question == 'Амперметр - измерительный прибор, который '):

					for k in range(6):
						if ((browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/div/div/p').text == 'включается последовательно в электрическую цепь')
							or
							(browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/div/div/p').text == 'имеет малое внутреннее сопротивление')
							or
							(browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/div/div/p').text == 'предназначен для определения тока в электрической цепи')
							):
							print('detected		' + browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/div/div/p').text)
							answer = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/input[1]')

							browser.execute_script("arguments[0].setAttribute('type','text')", answer)
							time.sleep(0.2)
							answer.clear()
							answer.send_keys('1')

			
				elif (question == 'Вольтметр - измерительный прибор, который '):

					for k in range(6):
						if ((browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/div/div/p').text == 'должен обладать бесконечно большим внутренним сопротивлением')
							or
							(browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/div/div/p').text == 'подключается параллельно нагрузке или источнику энергии')
							or
							(browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/div/div/p').text == 'предназначен для определения напряжения в электрической цепи')
							):
							print('detected		' + browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/div/div/p').text)
							answer = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/input[1]')


							browser.execute_script("arguments[0].setAttribute('type','text')", answer)
							time.sleep(0.2)
							answer.clear()
							answer.send_keys('1')

			if (question == ' Первый закон Кирхгофа гласит:'):
				for k in range(5):
					if (browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/div/div/p').text == 'Алгебраическая сумма токов, сходящихся в любом узле электрической цепи, равна нулю'):
						print('detected		' + browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/div/div/p').text)
						answer = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/input')

						browser.execute_script("arguments[0].setAttribute('checked','checked')", answer)

			if (question == 'Выберите пассивные элементы'):
				for k in range(7):
					if ((browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/div/div/p').text == 'C')
						or
						(browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/div/div/p').text == 'L')
						or
						(browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/div/div/p').text == 'R')
						):
						print('detected		' + browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/div/div/p').text)
						answer = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/input[1]')

						browser.execute_script("arguments[0].setAttribute('type','text')", answer)
						time.sleep(0.2)
						answer.clear()
						answer.send_keys('1')

			if (question == 'Место соединения трех или более элементов'):
				for k in range(5):
					if (browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/div/div/p').text == 'узел'):
						print('detected		' + browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/div/div/p').text)
						answer = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/input')

						browser.execute_script("arguments[0].setAttribute('checked','checked')", answer)

			if (question == 'Как соединены элементы?'):
				if (browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[1]/td[1]/p').text == 'Элементы подключены к одной и той же паре узлов и к ним приложено одинаковое напряжение'):
					for k in range(4):
						if (browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[1]/td[2]/select/option[{k+1}]').text == 'параллельное соединение'):
							print('detected		' + browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[1]/td[2]/select/option[{k+1}]').text)
							answer = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[1]/td[2]/select/option[{k+1}]')

							browser.execute_script("arguments[0].setAttribute('selected','selected')", answer)
					for k in range(4):
						if (browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[2]/td[2]/select/option[{k+1}]').text == 'последовательное соединение'):
							print('detected		' + browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[2]/td[2]/select/option[{k+1}]').text)
							answer = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[2]/td[2]/select/option[{k+1}]')

							browser.execute_script("arguments[0].setAttribute('selected','selected')", answer)
				else:
					for k in range(4):
						if (browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[1]/td[2]/select/option[{k+1}]').text == 'последовательное соединение'):
							print('detected		' + browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[1]/td[2]/select/option[{k+1}]').text)
							answer = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[1]/td[2]/select/option[{k+1}]')

							browser.execute_script("arguments[0].setAttribute('selected','selected')", answer)
					for k in range(4):
						if (browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[2]/td[2]/select/option[{k+1}]').text == 'параллельное соединение'):
							print('detected		' + browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[2]/td[2]/select/option[{k+1}]').text)
							answer = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[2]/td[2]/select/option[{k+1}]')

							browser.execute_script("arguments[0].setAttribute('selected','selected')", answer)

			if (question == 'Выберите соответствующие определения'):
				if (browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[1]/td[1]/p').text == 'Участок цепи, содержащий источники энергии, называется'):
					for k in range(5):
						if (browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[1]/td[2]/select/option[{k+1}]').text == 'активным'):
							print('detected		' + browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[1]/td[2]/select/option[{k+1}]').text)
							answer = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[1]/td[2]/select/option[{k+1}]')

							browser.execute_script("arguments[0].setAttribute('selected','selected')", answer)
					for k in range(5):
						if (browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[2]/td[2]/select/option[{k+1}]').text == 'пассивным'):
							print('detected		' + browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[2]/td[2]/select/option[{k+1}]').text)
							answer = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[2]/td[2]/select/option[{k+1}]')

							browser.execute_script("arguments[0].setAttribute('selected','selected')", answer)
				if (browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[1]/td[1]/p').text == 'Участок цепи, состоящий только из резисторов, называется'):
					for k in range(5):
						if (browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[1]/td[2]/select/option[{k+1}]').text == 'пассивным'):
							print('detected		' + browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[1]/td[2]/select/option[{k+1}]').text)
							answer = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[1]/td[2]/select/option[{k+1}]')

							browser.execute_script("arguments[0].setAttribute('selected','selected')", answer)
					for k in range(5):
						if (browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[2]/td[2]/select/option[{k+1}]').text == 'активным'):
							print('detected		' + browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[2]/td[2]/select/option[{k+1}]').text)
							answer = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[2]/td[2]/select/option[{k+1}]')

							browser.execute_script("arguments[0].setAttribute('selected','selected')", answer)

			if (question == 'Закон Ома для полной цепи гласит:'):
				for k in range(5):
					if (browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/div/div/p').text == 'Ток прямо пропорционален ЭДС и обратно пропорционален полному сопротивлению цепи'):
						print('detected		' + browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/div/div/p').text)
						answer = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/input')

						browser.execute_script("arguments[0].setAttribute('checked','checked')", answer)

			if (question == 'Контур, содержащий хотя бы одну новую ветвь'):
				for k in range(5):
					if (browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/div/div/p').text == 'независимый контур'):
						print('detected		' + browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/div/div/p').text)
						answer = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/input')

						browser.execute_script("arguments[0].setAttribute('checked','checked')", answer)

			if (question == 'Графическое изображение электрической цепи, показывающее способ соединения элементов'):
				for k in range(5):
					if (browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/div/div/p').text == 'электрическая схема'):
						print('detected		' + browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/div/div/p').text)
						answer = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/input')

						browser.execute_script("arguments[0].setAttribute('checked','checked')", answer)

			if (question == 'Один или несколько последовательно соединенных элементов между двумя узлами'):
				for k in range(5):
					if (browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/div/div/p').text == 'ветвь'):
						print('detected		' + browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/div/div/p').text)
						answer = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/input')

						browser.execute_script("arguments[0].setAttribute('checked','checked')", answer)

			if (question == 'Закон Ома для участка цепи гласит:'):
				for k in range(5):
					if (browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/div/div/p').text == 'Ток прямо пропорционален напряжению на участке цепи и обратно пропорционален сопротивлению этого участка'):
						print('detected		' + browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/div/div/p').text)
						answer = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/input')

						browser.execute_script("arguments[0].setAttribute('checked','checked')", answer)

			if (question == 'Какое сопротивление должен иметь:'):
				for k in range(4):
					if (browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/div/div/p').text == 'а) малое;    б) большое'):
						print('detected		' + browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/div/div/p').text)
						answer = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/input')

						browser.execute_script("arguments[0].setAttribute('checked','checked')", answer)

			if (question == 'Второй закон Кирхгофа гласит:'):
				for k in range(5):
					if (browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/div/div/p').text == 'Алгебраическая сумма напряжений на элементах контура равна алгебраической сумме ЭДС в этом контуре'):
						print('detected		' + browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/div/div/p').text)
						answer = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/input')

						browser.execute_script("arguments[0].setAttribute('checked','checked')", answer)

			if (question == 'Выберите активные элементы'):
				for k in range(7):
					if ((browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/div/div/p').text == 'J')
						or
						(browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/div/div/p').text == 'E')
						):
						print('detected		' + browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/div/div/p').text)
						answer = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/input[1]')

						browser.execute_script("arguments[0].setAttribute('type','text')", answer)
						time.sleep(0.2)
						answer.clear()
						answer.send_keys('1')

			if (question == 'Для каждого источника энергии выберите соответствующее внутреннее сопротивление'):
				for x in range(4):
					# '/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[1]/td[1]'
					# '/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[4]/td[1]/p'
					quest = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[{x+1}]/td[1]').text
					print(quest)
					if (quest == 'Реальный источник ЭДС'):
						for k in range(5):
							if (browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[{x+1}]/td[2]/select/option[{k+1}]').text == 'внутреннее сопротивление мало'):
								print('detected		' + browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[{x+1}]/td[2]/select/option[{k+1}]').text)
								answer = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[{x+1}]/td[2]/select/option[{k+1}]')
								browser.execute_script("arguments[0].setAttribute('selected','selected')", answer)
								break
					if (quest == 'Реальный источник тока'):
						for k in range(5):
							if (browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[{x+1}]/td[2]/select/option[{k+1}]').text == 'внутреннее сопротивление велико'):
								print('detected		' + browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[{x+1}]/td[2]/select/option[{k+1}]').text)
								answer = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[{x+1}]/td[2]/select/option[{k+1}]')
								browser.execute_script("arguments[0].setAttribute('selected','selected')", answer)
								break
					if (quest == 'Идеальный источник тока'):
						for k in range(5):
							if (browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[{x+1}]/td[2]/select/option[{k+1}]').text == 'внутреннее сопротивление равно бесконечности'):
								print('detected		' + browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[{x+1}]/td[2]/select/option[{k+1}]').text)
								answer = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[{x+1}]/td[2]/select/option[{k+1}]')
								browser.execute_script("arguments[0].setAttribute('selected','selected')", answer)
								break
					if (quest == 'Идеальный источник ЭДС'):
						for k in range(5):
							if (browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[{x+1}]/td[2]/select/option[{k+1}]').text == 'внутреннее сопротивление равно нулю'):
								print('detected		' + browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[{x+1}]/td[2]/select/option[{k+1}]').text)
								answer = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[{x+1}]/td[2]/select/option[{k+1}]')
								browser.execute_script("arguments[0].setAttribute('selected','selected')", answer)
								break

			if (question == 'Определите параметры эквивалентного источника энергии, если известно:'):
				ans_row = []
				for k in range(8):
					ans_xpath = f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/input[{k+2}]'
					answer = browser.find_element_by_xpath(ans_xpath)
					browser.execute_script("arguments[0].setAttribute('type','text')", answer)
					print('opened', k+1, 'input for clearing')
					time.sleep(0.2)
					answer.clear()
					answer.send_keys('0') # предварительно очищать строки необязательно

				# не очищает
				# browser.refresh()
				refresh_browser()

				for j in range(2,19,2):
					ans_row.append(int(browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div/span[{j}]').text))
					# time.sleep(0.1)
				print(ans_row)

				
				for k in range(8):
					# пример лаконичного кода
					ans_xpath = f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/input[{k+2}]'
					answer = browser.find_element_by_xpath(ans_xpath)
					browser.execute_script("arguments[0].setAttribute('type','text')", answer)
					print('opened', k+1, 'input for clearing')
					time.sleep(0.2)
					answer.clear()
					if (k == 0):
						answer.send_keys(ans_row.index(1)+1)
					if (k == 1):
						answer.send_keys(ans_row.index(100)+1)
					if (k == 2):
						answer.send_keys(ans_row.index(10)+1)
					if (k == 3):
						answer.send_keys(ans_row.index(20)+1)
					if (k == 4):
						answer.send_keys(ans_row.index(50)+1)
					if (k == 5):
						answer.send_keys(ans_row.index(10)+1)
					if (k == 6):
						answer.send_keys(ans_row.index(200)+1)
					if (k == 7):
						answer.send_keys(ans_row.index(100)+1)

			if (question == 'Определить показания измерительных приборов'): # Е = 12 В
				ans_row = []
				for k in range(2):
					ans_xpath = f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/input[{k+2}]'
					answer = browser.find_element_by_xpath(ans_xpath)
					browser.execute_script("arguments[0].setAttribute('type','text')", answer)
					print('opened', k+1, 'input for clearing')
					time.sleep(0.2)
					answer.clear()
					answer.send_keys('0') # предварительно очищать строки необязательно

				# не очищает
				# browser.refresh()
				refresh_browser()

				for j in range(2,19,2):
					ans_row.append(int(browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div/span[{j}]').text))
					# time.sleep(0.1)
				print(ans_row)

				
				for k in range(2):
					# пример лаконичного кода
					ans_xpath = f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/input[{k+2}]'
					answer = browser.find_element_by_xpath(ans_xpath)
					browser.execute_script("arguments[0].setAttribute('type','text')", answer)
					print('opened', k+1, 'input for answer')
					time.sleep(0.2)
					answer.clear()
					if (k == 0):
						answer.send_keys(ans_row.index(1)+1)
					if (k == 1):
						answer.send_keys(ans_row.index(4)+1)
					
						



		elif(xpath_exist(check_xpath)):
			img_el = browser.find_element_by_xpath(check_xpath)
			img_url = img_el.get_attribute('src')
			# print(img_url)

			element = browser.find_element_by_xpath('/html/body/div[1]/div[2]/header/div/div/div/div[2]/div[1]/nav/ol/li[10]/a')
			browser.execute_script(f"arguments[0].setAttribute('href','{img_url}')", element)
			browser.execute_script("arguments[0].setAttribute('download','current_pict.png')", element)
			element.click()

			for file in os.listdir("C:\\progs\\бот для тестов"):
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
			# Замкнутый путь, проходящий через несколько ветвей
			for k in range(5):
				if (browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/div/div/p').text == 'контур'):
					print('detected		' + browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/div/div/p').text)
					answer = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/input')
					browser.execute_script("arguments[0].setAttribute('checked','checked')", answer)



		if (i == 0):
			xpath = '/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[2]/input'
		else:
			xpath = '/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[2]/input[2]'
		browser.find_element_by_xpath(xpath).click()

print('successfully finished')

