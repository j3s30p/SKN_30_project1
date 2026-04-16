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
	questions = driver.find_elements(By.CSS_SELECTOR, "h2.wp-block-heading.has-medium-font-size")

	for q in questions:
		question = q.text.strip().split('. ')[1]
		answer = q.find_element(By.XPATH, "following-sibling::p[1]").text.strip()	# 바로 아래 <p> 잡기
		faq_list.append(Faq(question, answer))

url = 'https://sinoevse.com/ko/top-10-faqs-about-ev-charging-stations/'

driver = Chrome()
driver.get(url)

faq_list = []
crawling(faq_list)

with open('csv/sino.csv', mode='w', encoding='utf-8', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['question', 'answer'])
    writer.writeheader()
    writer.writerows([faq.to_dict() for faq in faq_list])