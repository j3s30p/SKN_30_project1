import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import csv
	
class Faq:
	def __init__(self, question, answer):
		self.question = question
		self.answer = answer
	
	def __str__(self):
		return f'{self.question}, {self.answer}'
	
	def to_dict(self):
		return {'question':self.question, 'answer':self.answer}

def crawling(faq_list):
	faqs = driver.find_elements(By.CSS_SELECTOR, '.board_faq')

	for faq in faqs:
		question = faq.find_element(By.CSS_SELECTOR, '.faq_title .title').text.strip()

		answer = faq.find_element(By.CSS_SELECTOR, '.faq_con').get_attribute("textContent")
		answer = answer.replace('\xa0', ' ')
		answer = " ".join(answer.split()[1:])

		faq_list.append(Faq(question, answer))

url = 'https://ev.or.kr/nportal/partcptn/initFaqAction.do#'

driver = Chrome()
driver.get(url)

faq_list = []
driver.find_element(By.ID, "2").click()
time.sleep(0.5)
crawling(faq_list)
driver.find_element(By.ID, "1").click()
time.sleep(0.5)
crawling(faq_list)

with open('csv/nuri.csv', mode='w', encoding='utf-8', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['question', 'answer'])
    writer.writeheader()
    writer.writerows([faq.to_dict() for faq in faq_list])