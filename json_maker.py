import time
import os
import shutil
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
# import requests
from PIL import Image, ImageChops
import json
import math

# https://eios.sibsutis.ru/mod/quiz/attempt.php?attempt=127854&cmid=55478
# print('ссылка на тест')
# link_na_test = input()

print('test v otdelnom okne? da/net')
nado = input()

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

def download_pict(pict_xpath, img_url):
	
	# print(img_el)
	print(img_url)
	
	global link_xp
	element = browser.find_element_by_xpath(link_xp)
	browser.execute_script(f"arguments[0].setAttribute('href','{img_url}')", element)
	browser.execute_script("arguments[0].setAttribute('download','current_pict.png')", element)
	element.click()
	# time.sleep(1)
	
	for file in os.listdir("C:\\progs\\bot_for_test"):
		if (file.endswith('.png')):
			print(file)
			return file
	print('file ne ska4alsya')
	exit(0)

def type_define():
# 	 "answer_inp_xp" 
# "answer_inp_xp11
#  "answer_xp1"    
# "answer_xp22"   
#  "answer_chb_xp1"
#  "answer_sel_xp1"
# "answer_sel_xp22
#  "answer_xp"    :
# "answer_xp_dr33"
	for ans_xpath in list(answer_xpaths):
		# print(ans_xpath)
		if (xpath_exist(answer_xpaths[ans_xpath])):
			# xpath = answer_xpaths[ans_xpath]
			# answer_el = browser.find_element_by_xpath(xpath)
			# answer_type = answer_el.get_attribute('type')
			print(ans_xpath)
			if (ans_xpath == 'answer_inp_xp') or (ans_xpath == 'answer_inp_xp11'):
				formatq = 'input'
			elif (ans_xpath == 'answer_xp1') or (ans_xpath == 'answer_xp22'):
				formatq = 'radio checkbox'
			elif ans_xpath == 'answer_chb_xp1':
				formatq = 'checkbox'
			elif (ans_xpath == 'answer_sel_xp1') or (ans_xpath == 'answer_sel_xp22'):
				formatq = 'select'
			elif (ans_xpath == 'answer_xp') or (ans_xpath == 'answer_xp_dr33'):
				formatq = 'drag&drop'
			return ans_xpath, formatq
	print('type not defined')
	exit(0)
# "answer_inp_xp"
# "answer_xp1"
# "answer_xp2"
# "answer_chb_xp1"
# "answer_sel_xp1"
# "answer_xp"

def parse_quest():
	if (xpath_exist(question_xpaths[0])):
		type_q = '1'
		print('vopros s picture v p[1]')
	else:
		type_q = '2'

	text_q = browser.find_element_by_xpath(question_xpaths[3]).text
	
	return type_q, text_q


def assembly_json_object(type_q, text_q, type_quest, formatq):
	sample = {
                "quest_text" : {
                    "main_xpath" : "default",
                    "first_line" : f"{text_q}",
                    "second_xpath" : "nothing",
                    "second_line" : "nothing"
                },
				"format" : f"{formatq}",
                f"{type_quest}" : "default",
				"answer" : [1]
			}
	if formatq == 'input':
		sample['type_variable'] = 'int'
	data[f'type{type_q}']['questions'].append(sample)



#############==========================================================#############




browser = webdriver.Firefox(options = option) #firefox_profile
browser.get('https://eios.sibsutis.ru/')

time.sleep(0.5)

login_xpath = '//*[@id="username"]'
browser.find_element_by_xpath(login_xpath).send_keys('vitalik.romanenko.02@inbox.ru')

# time.sleep(2)

password_xpath = '//*[@id="password"]'
browser.find_element_by_id('password').send_keys('Tm2vitalya@')
# time.sleep(2)

xpath = '//*[@id="loginbtn"]'
browser.find_element_by_xpath(xpath).click()

time.sleep(0.5)

text1 = browser.find_element_by_xpath('/html/body/div[1]/nav/ul[2]/li[2]/div/div/div/div/div/a/span/span[1]').text
print('bot logined by name: ' + text1)


# browser.get(link_na_test)
url_test = 'https://eios.sibsutis.ru/mod/quiz/attempt.php?attempt=279913&cmid=58383' # &page=1

# nado = 'da'
if nado == 'da':
	browser.get('https://eios.sibsutis.ru/mod/quiz/view.php?id=80907')
	time.sleep(1)
	WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/section/div[1]/div[3]/div/form/button"))).click()

	print(browser.window_handles)

	browser.switch_to.window(browser.window_handles[1])

	# print(browser.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div[1]/section/div/div/div/form/div/div[1]/div[2]/div/div[1]').text)
	# el = WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[1]/section/div/div/div/form/div/div[1]/div[2]/div/div[1]"))).text
	# print(el)
else:
	browser.get(url_test)



with open('sample.json', 'r', encoding='utf-8') as file:
	data = json.load(file)

link_xp = data['link_xp']

answer_xpaths = {
    "answer_inp_xp"         : "//form/div/div[1]/div[2]/div/div[2]/span/input",
	"answer_inp_xp11"         : "//form/div/div[1]/div[2]/div/div[2]/label/span/input",
    "answer_xp1"       : "//form/div/div[1]/div[2]/div/div[2]/div[2]/div[1]/input",
	"answer_xp22"       : '//form/div/div[1]/div[2]/div/div[2]/div[1]/div[1]/input',
    "answer_chb_xp1"         : "//form/div/div[1]/div[2]/div/div[2]/div/div[1]/input[2]",
    "answer_sel_xp1"         : "//form/div/div[1]/div[2]/div/div[2]/table/tbody/tr[1]/td[2]/select/option[1]",
	"answer_sel_xp22"         : "//form/div/div[1]/div[2]/div/div/p/span/select/option[1]",
    "answer_xp"    : "//form/div/div[1]/div[2]/div/div[2]/div/span[1]",
	"answer_xp_dr33"    : "//form/div/div[1]/div[2]/div/div[2]/div[2]/div/img[2]"
}
question_xpaths = [
	"//form/div/div[1]/div[2]/div/div[1]/p[1]/img",
	"//form/div/div[1]/div[2]/div/div[1]/p[1]",
	"//form/div/div[1]/div[2]/div/div[1]/p[2]",
	"//form/div/div[1]/div[2]/div/div[1]"
]
# input, radio, chb, sel, drag&drop

for i in range(40):
	time.sleep(1)
	print(f'=================={i+1}==================')

	type_quest, formatq = type_define()

	type_q, text_q = parse_quest()

	assembly_json_object(type_q, text_q, type_quest, formatq)


	if (i == 0):
		xpath = '//form/div/div[2]/input'
	else:
		xpath = '//form/div/div[2]/input[2]'
	browser.find_element_by_xpath(xpath).click()

with open('questions_for_any_test.json', 'w', encoding='utf-8') as file:
	json.dump(data, file, ensure_ascii=False, indent=4)


print('successfully finished')