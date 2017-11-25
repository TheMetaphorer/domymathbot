import praw
import math
import sys
import re
import os
import time
import logging

import functions
import settings
import utils

from .exceptions import MissingParenthesesException
from .components import Expression, nth_index


	
def configurate_logger():
	logging.basicConfig(level=logging.INFO,
	                    format='%(asctime)s %(levelname)s %(message)s',)

# Scans through a subreddit for math requests from various users
# Runs indefinitely until program is stopped: pass 'all' to sub
# to scan all comments submitted to reddit.
def scan_subreddit(sub, redis_server):
	subreddit = DMMB.subreddit(sub)
	for comment in subreddit.stream.comments():
		# Checks to see if the comment is a request to the Math bot.
		try:
			if comment.body.lower().startswith('u/domymathbot'): #and not redis_server.comment_in_database(comment):
				logging.info('Received request from u/{0}'.format(comment.author.name))
				logging.info("Evaluating {0}".format(comment.body))
				functions.process_request(comment.body, comment, redis_server, logging)
				logging.info('Saving redis cache to disk...')
				redis_server.redis.save()
				time.sleep(3)
			else:
				if redis_server.comment_in_database(comment): logging.info('Bypassed {0}; already replied'.format(comment.id))
		except praw.exceptions.APIException as e:
			cooldown_time = [float(mins) for mins in str(e) if mins.isdigit()][0] * 60;
			print 'Rate limit reached. Waiting for {0} seconds...'.format(cooldown_time)
			time.sleep(cooldown_time)
		
		except MissingParenthesesException:
			comment.reply("You're missing a closing parentheses!" + settings.INFO_STRING)
		
		except Exception as e:
			if 'division by zero' in str(e):
				logging.warning('Attempted division by zero')
				redis_server.add_comment(comment)
				logging.info('Saving redis cache to disk...')
				redis_server.redis.save()
				comment.reply("You can't divide by zero! You should've known better." + settings.INFO_STRING)
			else:
				logging.warning(str(e))
				comment.reply("Oops! There's something wrong! I can't solve this problem! I'll try again later." + settings.INFO_STRING)
				time.sleep(3)

# Main function of the bot. 
def main(args):
	redis_server = utils.BotCache('localhost', 6379, 0)
	configurate_logger()
	logging.info("Starting DoMyMathBot settings.VERSION {0}".format(settings.VERSION))
	scan_subreddit(args, redis_server)