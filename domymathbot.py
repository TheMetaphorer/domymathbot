import praw
import math
import sys
import re
import time

VERSION = "2017.0.4"
INFO_STRING = """

----

^^^bot ^^^by ^^^u/TheMetaphorer [^^^GitHub](http://github.com/TheMetaphorer/domymathbot) ^^^Version ^^^{0}
""".format(VERSION)

operators = ['^','*', '/','%', '+', '-']	

# OAUTH AUTHENTICATION CODE OMITTED.

def replace_values(li, string, ind1, ind2):
	print li
	if len(li) == 3:
		return [string]
	else:
		li[ind1:ind2] = ''
		li.insert(ind1, string)
		return li
		
# Tests to see how many times an operator occurs
# in an expression.
def operator_in_expression(operator, expression):
	occurrences = expression.count(operator)
	return occurrences if occurrences > 0 else False
	
def operator_evals(operator, occurrences, expression):
	if occurrences:
		for i in range(occurrences):
			print expression
			position = expression.index(operator)
			num1 = float(expression[position-1])
			num2 = float(expression[position+1])
			if operator == '^':
				expression = replace_values(expression, str(num1**num2), position-1,position+2)
			elif operator == '*':
				expression = replace_values(expression, str(num1*num2), position-1,position+2)
			elif operator == '/':
				expression = replace_values(expression, str(num1/num2), position-1,position+2)
			elif operator == '%':
				expression = replace_values(expression, str(num1%num2), position-1,position+2)
			elif operator == '+':
				expression = replace_values(expression, str(num1+num2), position-1,position+2)
			elif operator == '-':
				expression = replace_values(expression, str(num1-num2), position-1,position+2)
	return expression
def process_expression(expression):
	# Iterates through every operator in list of operators to see if 
	# they occur in the expression. If they do, it performs the operations
	# however many times they occur. Then the broken down expression is
	# replaced with the evaluation.
	expression = re.split(r'([0-9.e]+|\^\*/%\+\-)', expression)
	while '' in expression: expression.remove('')
	print expression
	for operator in operators:
		expression = operator_evals(operator, operator_in_expression(operator, expression), expression)
	for i in range(len(expression)):
		expression[i] = float(expression[i])
	return sum(expression)

def scan_subreddit(sub):
	subreddit = dmmb.subreddit(sub)
	for comment in subreddit.stream.comments():
		# Checks to see if the comment is a request to the Math bot.
		try:
			if comment.body.startswith('!domath'):
				print 'Math request from u/{0}'.format(comment.author.name)
				expr = comment.body.replace('!domath', '').replace(' ', '')
				print expr
				comment.reply("The answer is {0}!".format(process_expression(expr)) + INFO_STRING)
				time.sleep(2.2)
		except praw.exceptions.APIException as e:
			cooldown_time = [float(mins) for mins in str(e) if mins.isdigit()][0] * 60;
			print 'Rate limit reached. Waiting for {0} seconds...'.format(cooldown_time)
			time.sleep(cooldown_time)
			scan_subreddit(sub)
		
		except Exception as e:
			if 'division by zero' in str(e):
				comment.reply("You can't divide by zero! You should've known better." + INFO_STRING)
			comment.reply("Oops! There's something wrong! I can't solve this problem!" + INFO_STRING)
			time.sleep(2.2)
		
scan_subreddit('test')