import time
import random
import click

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, JavascriptException


from app.abstract import ActionAbstract
from app import utils, logger

class Spam_open_messages(ActionAbstract):

	def apply(self):
		logger.info(f'Processing action ({self.__class__.__name__}) for ({self.isp.profile.email})...')
		driver = self.isp.driver
		profile = self.isp.profile

		# print('Start ActionChains...')
		# Go to spam section.
		driver.get('https://mail.yahoo.com/d/folders/6')

		# let javascript requests finish.
		time.sleep(5)

		# Scroll down.
		with utils.scroll_down(driver, 'div[data-test-id=virtual-list]', ignored_exceptions=(JavascriptException,)):
			actions = ActionChains(driver)
			time.sleep(2)
			# Archive all messages.
			try:
				messages = driver.find_elements_by_css_selector('a[data-test-id=message-list-item]')
				messages[0].click()

				last_message = random.randint(min(60, len(messages)), min(120, len(messages)))
				click.secho(f'({profile.email}) Total messages {len(messages)}: {last_message} messages will be openned.', fg='bright_black')

				with click.progressbar(length=last_message, label=f'Openning messages ({profile.email})...', show_pos=True) as bar:
					for i, message in enumerate(messages):
						actions = ActionChains(driver)
						actions.send_keys(Keys.ARROW_RIGHT)
						# add start to the current message.
						if random.random() <= 0.3:
							actions.send_keys('l')
						actions.perform()

						# show the progress
						# print(f'\r{i+1}/{last_message}', end='')

						bar.update(1) # +=1 each time

						# clear the all chained actions (is not working, it's a bug in selenium source code).
						# actions.reset_actions()

						time.sleep(random.uniform(3, 5))
						# stop openning messages.
						if i == last_message:
							break

			except TimeoutException:
				logger.warning(f'({self.ACTION.name}) {profile.email:.<40} [WARNING]')
			except Exception as e:
				logger.exception(f'[{self.ACTION.name}] {profile.email:.<40} [Error]')
			else:
				logger.info(f'({self.ACTION.name}) {profile.email:.<40} [DONE]')
