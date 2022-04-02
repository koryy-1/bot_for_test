import os
from PIL import Image, ImageChops

for file in os.listdir("C:\\progs\\бот для тестов"):
	if (file.endswith('.png')):
		print(file)
		break
img1 = Image.open(f'picts_test1\\0.png')
img2 = Image.open(f'picts_test1\\0.png')
try:
	differences = ImageChops.difference(img1, img2)
	print(differences.getbbox())
	if (differences.getbbox() == None):
		print('raznye')
	else:
		print('odin')
except Exception as e:
	print(e)
