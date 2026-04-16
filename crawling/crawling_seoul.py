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

url = 'https://news.seoul.go.kr/env/archives/517115#sns_elem_dropdownmenu'

driver = Chrome()
driver.get(url)

faq_list = []

question_links = driver.find_elements(By.CSS_SELECTOR, '.qlist a')

for link in question_links:
	question = link.find_element(By.CSS_SELECTOR, 'span:not(.num)').text.strip()

	href = link.get_attribute('href')          # 예: https://...#cont1-18
	answer_id = href.split('#')[-1]            # cont1-18

	answer_el = driver.find_element(By.ID, answer_id)
	answer = answer_el.get_attribute('textContent').strip()
	faq_list.append(Faq(question, answer))

with open('crawling/csv/seoul.csv', mode='w', encoding='utf-8', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['question', 'answer'])
    writer.writeheader()
    writer.writerows([faq.to_dict() for faq in faq_list])