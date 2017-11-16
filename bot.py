import praw
import math
import sys
import re
import time
from .exceptions import MissingParenthesesException
from .components import Expression, nth_index
from .settings import OPERATORS, VERSION, INFO_STRING, CONSTANTS

# OAUTH AUTHENTICATION CODE OMITTED

def replace_values(li, string, ind1, ind2):
	if len(li) == 3:
		return [string]
	else:
		li[ind1:ind2] = ''
		li.components.insert(ind1, string)
		return li
	
def operator_evals(expression):
	while len(expression) > 1:
		j = len(expression)
		for i in range(j):
			if any(i in expression for i in OPERATORS) == False: break
			if expression[i] in OPERATORS:
				operator = expression[i]
				num1 = float(expression[i-1])
				num2 = float(expression[i+1]) if operator != '!' else None
				if operator == '^':
					expression = replace_values(expression, str(num1**num2), i-1, i+2)
				elif operator == '!':
					expression = replace_values(expression, math.factorial(num1), i-1, i+1)
				elif operator == '*':
					expression = replace_values(expression, str(num1*num2), i-1, i+2)
				elif operator == '/':
					expression = replace_values(expression, str(num1/num2), i-1, i+2)
				elif operator == '%':
					expression = replace_values(expression, str(num1%num2), i-1, i+2)
				elif operator == '+':
					expression = replace_values(expression, str(num1+num2), i-1, i+2)
				elif operator == '-':
					expression = replace_values(expression, str(num1-num2), i-1, i+2)
			elif expression[i] in CONSTANTS.keys():
				expression[i] = CONSTANTS[expression[i]]
	return expression[0]


def process_expression(expression, parentheses=False):
	# Iterates through every operator in list of OPERATORS to see if 
	# they occur in the expression. If they do, it performs the operations
	# however many times they occur. Then the broken down expression is
	# replaced with the evaluation.
	def recursive_parentheses(expression):
		for k in range(expression.sub_expression_count):
			j = len(expression)
			for i in range(j):
				if expression[i] == '(' or expression[i] != ')':
					if '(' in expression[i+1:]:
						continue
					elif ')' in expression[i:] and expression[i] == '(':
						close_par_index=expression[i:].index(')') + i
						expression=replace_values(expression, operator_evals(expression[i+1:close_par_index]), i, close_par_index+1)
						break
	if '(' in expression:
		recursive_parentheses(expression)
	expression = operator_evals(expression)
	return expression
						
						
						
def scan_subreddit(sub):
	subreddit = DMMB.subreddit(sub)
	global step_by_step
	for comment in subreddit.stream.comments():
		# Checks to see if the comment is a request to the Math bot.
		try:
			if comment.body.startswith('!domath'):
				print 'Math request from u/{0}'.format(comment.author.name)
				expr = comment.body.replace('!domath', '').replace(' ', '')
				print "Evaluating {0}".format(expr)
				expr = Expression(expr)
				ans=process_expression(expr)
				comment.reply("The answer is {0}!".format(ans) + INFO_STRING)
				step_by_step = []
				time.sleep(3)
		except praw.exceptions.APIException as e:
			cooldown_time = [float(mins) for mins in str(e) if mins.isdigit()][0] * 60;
			print 'Rate limit reached. Waiting for {0} seconds...'.format(cooldown_time)
			time.sleep(cooldown_time)
		
		except MissingParenthesesException:
			comment.reply("You're missing a closing parentheses!" + INFO_STRING)
		
"""		except Exception as e:
			if 'division by zero' in str(e):
				comment.reply("You can't divide by zero! You should've known better." + INFO_STRING)
			else:
				print str(e)
				comment.reply("Oops! There's something wrong! I can't solve this problem!" + INFO_STRING)
				time.sleep(3) """
	
	
def main(args):
	print "Starting DoMyMathBot Version {0}".format(VERSION)
	scan_subreddit(args)