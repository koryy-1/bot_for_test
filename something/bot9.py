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