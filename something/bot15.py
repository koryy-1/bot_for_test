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