import csv
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from PIL import Image
from io import BytesIO
import os
import shutil
import datetime
import pyautogui

#semaine pas affichee dans le champ de vision ; todo
#local path : done


class groupe:
	def __init__(self,nom,parent,css,type='normal'):
		self.css=css
		self.nom=nom
		self.parent=parent
		self.isClicked=False
		self.type=type
    
	def __str__(self):
		if self.parent==None:
			return '{nom = ' + self.nom+', parent=' +'None' +', css=None}'		
		else:
			return '{nom = ' + self.nom+', parent=' +self.parent.nom +', css=' +self.css + '}'


	def famille(self):
		obj=self
		L=[obj]
		while(True): # recupere les css des parents succesifs
			obj=obj.parent
			if obj.nom== 'src' : #il n'y a plus de parents
				break
			else:
				L.append(obj)
		L=L[::-1] # renvoie dans l'ordre des clicks	
		return L	

	def cChemin(self): # retourn une liste de string contenant le chemin en css
		L=self.famille()
		ret=[]
		for l in L:
			ret.append(l.css)
		return ret

	def rChemin(self): #de meme que xchemin mais avec le chemin en dossiers locaux
		L=self.famille()
		ret='.//pic//'
		RET=[]
		for l in L:
			s=l.nom[:]
			if '_' in s:
				s=s.replace('_','-')
			ret+=s+'//'
			RET.append(ret)
		return RET

	def click(self,driver):
		time.sleep(0.2)
		scroll="""/html/body/div[1]/div[1]/div/div[2]/div[2]/div[1]/div/div[1]/div/div[1]"""
		el=driver.find_elements_by_xpath(scroll)[0]

		famille=self.famille()

		for obj in famille:
			#remonte la page
			time.sleep(0.2)
			action = webdriver.common.action_chains.ActionChains(driver)
			action.move_to_element_with_offset(el,5,10)
			for i in range(100):
				action.click()
			action.perform()
			###
			totalCount=0
			while not(obj.isClicked):
				time.sleep(0.2)
				totalCount+=1
				if totalCount>50:
					raise Exception('Overtime : item a clicker non trouve')
				try:
					driver.find_element_by_css_selector(obj.css).click()
					obj.isClicked=True
				except:
					action = webdriver.common.action_chains.ActionChains(driver)
					action.move_to_element_with_offset(el, 5, 500)
					for i in range(3):
						action.click()
					action.perform()
			if obj.type=='edt':
				obj.isClicked=False
		time.sleep(0.5)
		
	def refresh_picture(self,driver,nom):
		self.click(driver)
		#screen & sauvegarde
		png = driver.get_screenshot_as_png()
		im = Image.open(BytesIO(png))
		im = im.crop((317, 5, 1902, 785))
		path=self.rChemin()
		try:
			path=path[:3]
		except :
			pass
		for r in path:
			try:
				os.mkdir(r)
			except:
				pass
		im.save(r+nom)







class super_groupe: #super groupe destine a contenir les sous groupes

	def __init__(self):
		self.liste_groupes=[groupe('src',None,None)] #tous les groupes ont pour commun le groupe 'src'
		self.liste_edt=[] #liste des edt

		self.append_groupes('.\\data\\dossiers_principaux.csv')
		self.append_groupes('.\\data\\classes.csv')
		self.append_groupes('.\\data\\groupes.csv')
		self.append_groupes('.\\data\\edt.csv',edt=True)
	def __str__(self):
		ret='[ Super groupe, contenant : \n'
		for p in self.liste_groupes:
			ret+=str(p)+'\n'
		return ret+']'

	def append_groupes(self,path,edt=False): #on ajoute des groupes a la liste, avec les fichiers
		liste_txt=list(csv.reader(open(path,'r')))[1:]
		for d in liste_txt:
			parent=None
			for f in self.liste_groupes: #On cherche l'objet parent du dossier actuel avec son nom
				if d[1]==f.nom:
					parent=f
			if parent==None:
				raise Exception(str(d) + "Parent non trouvé")
			obj=groupe(d[0],parent,d[2])
			if edt:
				obj=groupe(d[0],parent,d[2],'edt')
				self.liste_edt.append(obj)
			else:
				obj=groupe(d[0],parent,d[2])
			self.liste_groupes.append(obj)


	def find_by_name(self,name):
		for d in self.liste_groupes:
			if d.nom==name:
				return d
		raise Exception('Name not found :' + name)

	def update_all(self, driver):
		date=datetime.date.today()
		d=date.day
		m=date.month
		y=date.year

		for i in range(3):
			for l in self.liste_edt:
				driver.find_elements_by_xpath("//*[contains(text(), 'Semaine {}')]".format(datetime.date(y,m,d).isocalendar()[1]+i))[0].click()
				l.refresh_picture(driver,'semaine_{}.png'.format(i))


driver = webdriver.Firefox()
driver.maximize_window()
driver.get("https://edt.insa-strasbourg.fr/direct/index.jsp")
driver.find_element_by_xpath("""//*[@id="username"]""").send_keys("")
driver.find_element_by_xpath("""//*[@id="password"]""").send_keys("")
driver.find_element_by_xpath("""//*[@id="password"]""").send_keys(Keys.ENTER)
time.sleep(10)

monSG=super_groupe()
monSG.update_all(driver)

shutil.make_archive('archivepic','zip','pic')

driver.get('https://www.pythonanywhere.com/login/?next=/')
driver.find_element_by_xpath("""//*[@id="id_auth-username"]""").send_keys("Dakaryon")
driver.find_element_by_xpath("""//*[@id="id_auth-password"]""").send_keys("michelmichel")
driver.find_element_by_xpath('''//*[@id="id_next"]''').click()
time.sleep(1)
driver.get('https://www.pythonanywhere.com/user/Dakaryon/files/home/Dakaryon/mysite')
time.sleep(2)
driver.find_element_by_css_selector('#id_upload_button').click()
pyautogui.write(os.getcwd()+'\\' + 'archivepic.zip')
pyautogui.press('enter')
time.sleep(10)
driver.quit()