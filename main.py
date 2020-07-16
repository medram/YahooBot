import sys
import traceback
import logging
import time
import click

from selenium.common.exceptions import WebDriverException

from app import Yahoo, common, logger

# messages = list(range(10))
# total_messages = len(messages)
# print(click)
# with click.progressbar(messages,
# 						label='Openning messages...',
# 						length=total_messages,
# 						show_pos=True,
# 						color='green') as bar:
#     for x in bar:
#         time.sleep(0.5)
# exit()

# main function.
def main():
	# show an introduction about YahooBot
	common.show_introduction()

	ACTION = common.get_action()

	profiles_list = common.load_profiles_from_csv()

	logger.debug(f'Total emails: {len(profiles_list)}')
	logger.info(f'Processing ({ACTION.name}) ...')

	try:
		for i, profile in enumerate(profiles_list):
			logger.debug(f'Emails processed: {i}/{len(profiles_list)} ({round(i / len(profiles_list) * 100, 2)}%)')
			try:
				isp = Yahoo(profile)
				isp.login()
				isp.do_action(ACTION)
				isp.quit()

			except WebDriverException as e:
				if 'Message: Reached error page' in str(e):
					logger.warning(f'Please check your internet connection of your server/RDP')
				elif 'Message: Failed to decode response' in str(e):
					logger.warning(f'Message: Failed to decode response from marionette!')
				elif 'Message: permission denied' in str(e):
					logger.warning(f'Message: permission denied!')
				else:
					logger.exception('Exception occured')
			except KeyboardInterrupt:
				raise
			except Exception as e:
				# exc_type, exc_value, exc_tb = sys.exc_info()
				# traceback.print_exception(exc_type, exc_value, exc_tb)
				logger.exception('Exception occured')

		logger.debug(f'Emails processed: {len(profiles_list)}/{len(profiles_list)} (100%)')
	except KeyboardInterrupt:
		logger.info('Stopped')


if __name__ == '__main__':
	main()
