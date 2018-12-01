from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

#도서명
def completeName(incompletionName):
	try:
		#path = "/home/grad/flaskapp/app/chromedriver.exe" #드라이버 경로

		options = webdriver.ChromeOptions()
		options.add_argument('--disable-extensions')
		options.add_argument('--headless')
		options.add_argument('--disable-gpu')
		options.add_argument('--no-sandbox')

		url = "https://www.google.co.kr/"
		print("step1 : filtering")
		driver = webdriver.Chrome('/usr/local/bin/chromedriver',chrome_options=options)
		driver.get(url)
		#print('driver end')
		selected_tag_search = driver.find_element_by_css_selector('div#viewport div#searchform form#tsf div.tsf-p div.sfibbbc  div#sbtc div.sbibtd div#sfdiv div.lst-c div.gstl_0.sbib_a div#sb_ifc0 div#gs_lc0 input#lst-ib')
		selected_tag_search.send_keys('~'+incompletionName+' +알리딘')
		print("step2 : similarity")
		selected_tag_search.send_keys(Keys.ENTER)
		soup = BeautifulSoup(driver.page_source,'lxml')
		item = soup.select_one('div#main div#cnt div.mw div#rcnt div.col div#center_col div#res div#search div div#ires div#rso div.bkWMgd div.srg div.g div div.rc div.r a')
		driver.get(item['href'])
		print("step3 : searching")
		title = driver.find_element_by_css_selector('body > div:nth-child(21) > table > tbody > tr:nth-child(1) > td > div > table:nth-child(10) > tbody > tr:nth-child(1) > td > table:nth-child(1) > tbody > tr > td > a.p_topt01')
		print("step4 : find title")
		author = driver.find_element_by_css_selector('body > div:nth-child(21) > table > tbody > tr:nth-child(1) > td > div > table:nth-child(10) > tbody > tr:nth-child(1) > td > table:nth-child(2) > tbody > tr > td:nth-child(1) > a:nth-child(1)')
		print("step5 : find author")
		publisher = driver.find_element_by_css_selector('body > div:nth-child(21) > table > tbody > tr:nth-child(1) > td > div > table:nth-child(10) > tbody > tr:nth-child(1) > td > table:nth-child(2) > tbody > tr > td:nth-child(1) > a:nth-child(2)')
		includeIsbn = driver.find_element_by_css_selector('body > div:nth-child(21) > table > tbody > tr:nth-child(1) > td > div > table:nth-child(10) > tbody > tr:nth-child(2) > td > table > tbody > tr > td:nth-child(3) > div:nth-child(7) > table > tbody > tr > td')
		isbn = includeIsbn.text.split("ISBN : ")
		print("step6 : find isbn")
		#driver.quit()
		return [title.text,author.text,publisher.text,isbn[1]]
	except:
		print("Error: "+incompletionName)
		return [-1,-1]

if __name__ == "__main__":
	#print(completeName('신과 컴퓨터 네트워크'))
	print(completeName('파olge로 배우는 웹 크롤러'))