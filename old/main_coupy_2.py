from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from PIL import Image
from io import BytesIO
import csv

def scrollUntilClick(driver, itemAClicker,semaine=0, scroll="""/html/body/div[1]/div[1]/div/div[2]/div[2]/div[1]/div/div[1]/div/div[1]"""):
	itemTrouve=False
	el=driver.find_elements_by_xpath(scroll)[0]
	counter=0
	down = True
	while not(itemTrouve):
		try:
			time.sleep(0.1)
			driver.find_element_by_xpath(itemAClicker).click()
			itemTrouve=True
		except:
			action = webdriver.common.action_chains.ActionChains(driver)
			if down:
				action.move_to_element_with_offset(el, 5, 500)
			else:
				action.move_to_element_with_offset(el,5,10)
			for i in range(11):
				action.click()
			action.perform()
			counter+=1
			if counter%3==0 :
				down=not(down)

def takeScreen(L, pathImage):
	
	# connexion a l'edt
	chrome_path = "./chrome/chromedriver.exe"
	driver = webdriver.Chrome(chrome_path)
	driver.maximize_window()
	driver.get("https://edt.insa-strasbourg.fr/direct/index.jsp")
	driver.find_element_by_xpath("""//*[@id="username"]""").send_keys("dcartiermillon01")
	driver.find_element_by_xpath("""//*[@id="password"]""").send_keys("=08fx3TdE0")
	driver.find_element_by_xpath("""//*[@id="password"]""").send_keys(Keys.ENTER)
	time.sleep(5)

	# affichage de l'element souhaité
	for i in range(len(L)):
		scrollUntilClick(driver,L[i])
	
	time.sleep(0.3)
	
	#screen & sauvegarde
	png = driver.get_screenshot_as_png()
	driver.quit()
	im = Image.open(BytesIO(png))
	im = im.crop((317, 5, 1902, 785))
	im.save(pathImage)







liste_clicks=open("liste_clics.csv")
L=list(csv.reader(liste_clicks))
takeScreen(L[1],"screenMiq3.png")