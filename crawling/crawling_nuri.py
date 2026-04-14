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

url = 'https://ev.or.kr/nportal/partcptn/initFaqAction.do#'

driver = Chrome()
driver.get(url)

faq_list = []

for _ in range(4):
	faqs = driver.find_elements(By.CSS_SELECTOR, '.board_faq')

	for faq in faqs:
		question = faq.find_element(By.CSS_SELECTOR, '.faq_title .title').text.strip()

		answer_el = faq.find_element(By.CSS_SELECTOR, '.faq_con')
		answer = faq.find_element(By.CSS_SELECTOR, '.faq_con').get_attribute("textContent")
		answer = answer.replace('\xa0', ' ')
		answer = " ".join(answer.split()[1:])

		faq_list.append(Faq(question, answer))

	next_button = driver.find_element(By.CSS_SELECTOR, ".next.arrow")
	next_button.click()
	time.sleep(0.5)

with open('csv/nuri.csv', mode='w', encoding='utf-8', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['question', 'answer'])
    writer.writeheader()
    writer.writerows([faq.to_dict() for faq in faq_list])