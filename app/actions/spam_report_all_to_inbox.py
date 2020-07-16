import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, JavascriptException


from app.abstract import ActionAbstract
from app import utils, logger

class Spam_report_all_to_inbox(ActionAbstract):

	def apply(self):
		logger.info(f'Processing action ({self.__class__.__name__}) for ({self.isp.profile.email})...')
		driver = self.isp.driver
		profile = self.isp.profile

		# print('Start ActionChains...')
		# Go to Junk section
		driver.get('https://mail.yahoo.com/d/folders/6')

		# let javascript requests finish.
		time.sleep(5)

		# Scroll down.
		with utils.scroll_down(driver, 'div[data-test-id=virtual-list]', ignored_exceptions=(TimeoutException, JavascriptException)):
			actions = ActionChains(driver)
			# select all msgs at spam section.
			actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()

			time.sleep(5)

			# report all to inbox.
			try:
				button_not_junk = driver.find_elements_by_css_selector('button[data-test-id=toolbar-not-spam]')[0]
				button_not_junk.click()
				# click to "Not junk" button.


				time.sleep(5)
				wait = WebDriverWait(driver, 30)
				# undo_notification = (By.CSS_SELECTOR, 'div[role=status] div')
				alertdialog = (By.CSS_SELECTOR, 'div[role=alertdialog] div')

				if wait.until_not(EC.presence_of_element_located(alertdialog)):
					# print('Confirm')
					# wait to make sure the action is applied
					time.sleep(5)
			except TimeoutException:
				logger.warning(f'[{self.ACTION.name}] Timeout ({profile.email}).')
			except IndexError:
				logger.warning(f'[{self.ACTION.name}] Maybe no messages are found in Spam of ({profile.email}).')
			except Exception as e:
				logger.exception(f'[{self.ACTION.name}] ({profile.email})')
			else:
				logger.info(f'({self.ACTION.name}) {profile.email:.<40} [DONE]')
