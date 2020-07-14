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

	click.secho(f'Total emails: {len(profiles_list)}', fg='bright_black')
	logger.info(f'Processing ({ACTION.name}) ...')

	for profile in profiles_list:
		try:
			isp = Yahoo(profile)
			isp.login()
			isp.do_action(ACTION)
			isp.quit()

		except WebDriverException as e:
			if 'Message: Reached error page' in str(e):
				logger.warning(f'Please check your internet connection of your server/RDP')
			else:
				logger.exception('Exception occured')
		except KeyboardInterrupt:
			logger.info('Stopped')
		except Exception as e:
			# exc_type, exc_value, exc_tb = sys.exc_info()
			# traceback.print_exception(exc_type, exc_value, exc_tb)
			logger.exception('Exception occured')



if __name__ == '__main__':
	main()
