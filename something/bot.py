import time
from selenium import webdriver

test = 9



option = webdriver.FirefoxOptions()
option.set_preference('dom.webdriver.enabled', False)
option.set_preference('dom.webnotifications.enabled', False)
option.set_preference('general.useragent.override', 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0')
# option.headless = True

browser = webdriver.Firefox(options = option)
browser.get('https://eios.sibsutis.ru/course/view.php?id=1521')

# cookies = {'name': 'MoodleSession', 'value': 'eca04mnko3h5g4frsavvnf3dmo', 'path': '/', 'domain': 'eios.sibsutis.ru', 'secure': True, 'httpOnly': False, 'sameSite': 'None'}
# for cookie in cookies:
# 	browser.add_cookie(cookie)

# time.sleep(2)

# browser.refresh()


login_xpath = '//*[@id="username"]'
browser.find_element_by_xpath(login_xpath).send_keys('dima.tryshkanov89@mail.ru')

# time.sleep(2)

password_xpath = '//*[@id="password"]'
browser.find_element_by_id('password').send_keys('Ogubot22.')
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


# for i in range(5):
# 	# browser.get(f"https://eios.sibsutis.ru/mod/quiz/attempt.php?attempt=271228&cmid=79499&page={i}")
# 	browser.get(f"https://eios.sibsutis.ru/mod/quiz/attempt.php?attempt=271228&cmid=79499&page=2")
# 	time.sleep(1)
# 	question_xpath = '/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[1]/p[1]'
# 	question = browser.find_element_by_xpath(question_xpath).text
# 	print(f'{i+1})	' + question)
# 	answer = driver.find_element_by_id('q309175_14_p1').send_keys('1')
# 	answer = driver.find_element_by_id('q309175_14_p2').send_keys('1')
if (test == 15):
	browser.get(f'https://eios.sibsutis.ru/mod/quiz/attempt.php?attempt=271228&cmid=79499&page=8')
	time.sleep(1)
	question_xpath = '/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[1]/p[1]'
	question = browser.find_element_by_xpath(question_xpath).text
	print(question)

	if (question == 'Определить ослабление фильтра верхних частот при частоте, стремящейся к бесконечности, если порядок фильтра равен 5:'):

		for k in range(8):
			if (browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div/span[{k+1}]').text == 'Amin'):
				choice = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div/span[{k+1}]')
				num_choice = choice.get_attribute('class')
				print(num_choice)
				num_choice = num_choice[15]
				print(num_choice)
				break
		answer = browser.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/input[2]')
		answer1 = browser.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/input[3]')
		
		browser.execute_script("arguments[0].setAttribute('type','text')", answer)
		browser.execute_script("arguments[0].setAttribute('type','text')", answer1)
		time.sleep(1)
		answer.clear()
		answer.send_keys(num_choice)
		answer1.clear()
		answer1.send_keys(num_choice)
		# '/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div/span[1]'

		# browser.get(f"https://eios.sibsutis.ru/mod/quiz/attempt.php?attempt=271228&cmid=79499&page=3")

		xpath = '/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[2]/input[2]'
		browser.find_element_by_xpath(xpath).click()

		# '//*[@id="yui_3_17_2_1_1623413497143_81"]'

if (test == 1):
	for i in range(2):
		browser.get(f'https://eios.sibsutis.ru/mod/quiz/attempt.php?attempt=268523&cmid=46863&page={i}')
		time.sleep(1)
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

				if (i == 0):
					xpath = '/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[2]/input'
				else:
					xpath = '/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[2]/input[2]'
				browser.find_element_by_xpath(xpath).click()
		
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

				if (i == 0):
					xpath = '/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[2]/input'
				else:
					xpath = '/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[2]/input[2]'
				browser.find_element_by_xpath(xpath).click()

if (test == 9):
	# for i in range(1): цикл здесь нужен чтобы переходить с вопроса на вопрос, аргументом x в range(x) ставим количество вопросов, напр. 39 или 49, нумерация начинается с 0, но пока что цикл не используем
	# в питоне должна быть строгая табуляция, если где-то табуляции больше или меньше чем требуется, то вылезет ошибка
	browser.get(f'https://eios.sibsutis.ru/mod/quiz/attempt.php?attempt=272380&cmid=99763&page=22') # здесь query параметр должен быть таким page=22, тк делаем 23 вопрос, то есть номер page отвечает за номер вопроса
	time.sleep(1)
	question_xpath = '/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[1]/p'
	question = browser.find_element_by_xpath(question_xpath).text
	print(f'{23})	' + question)

	if (question == 'В уравнениях четырехполюсника в А-параметрах безразмерными являются коэффициенты:'):
		question_xpath = '/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[1]'
		question = browser.find_element_by_xpath(question_xpath).text
		print('		' + question)
		if (question == 'Выберите один или несколько ответов:'): # обязательно нужно копировать весь текст заключенный в html тегах, где-то на конце может быть пробел, а где-то его нет, иначе if может не сработать
			print(browser.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[1]/div/div/p').text)
			# этот принт приводит пример как выглядит содержимое элемента по xpath даже если там есть другие теги

			for k in range(4):
				# сравниваем текст в формате который выводит принт на 167 строке
				if ((browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/div/div/p').text == 'А11')
					or
					(browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/div/div/p').text == 'А22')
					):
					print('detected		' + browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/div/div/p').text)
					# detected я по приколу писал, в остальном все правильно
					answer = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[1]/div[2]/div/div[2]/div[2]/div[{k+1}]/input[1]')

					browser.execute_script("arguments[0].setAttribute('type','text')", answer)
					time.sleep(0.2)
					answer.clear()
					answer.send_keys('1')

			if (i == 0):
				xpath = '/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[2]/input'
			else:
				xpath = '/html/body/div[1]/div[2]/div/div[1]/section/div[1]/form/div/div[2]/input[2]'
			browser.find_element_by_xpath(xpath).click()
