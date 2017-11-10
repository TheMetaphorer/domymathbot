import praw
import math
import sys
import re
import time


VERSION = "2017.0.2"

operators = ['^','*', '/','%', '+', '-']	

#OAUTH AUTHENTICATION CODE OMITTED.

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
	occurences = expression.count(operator)
	return occurences if occurences > 0 else False

def process_expression(expression):
	# Iterates through every operator in list of operators to see if 
	# they occur in the expression. If they do, it performs the operations
	# however many times they occur. Then the broken down expression is
	# replaced with the evaluation.
	expression = re.split(r'([0-9.]+|\^\*/%\+\-)', expression)
	while '' in expression: expression.remove('')
	print expression
	for operator in operators:
		if operator == "^":
			occurences = operator_in_expression(operator, expression)
			if occurences:
				for i in range(occurences):
					position = expression.index(operator)
					base = int(expression[position-1])
					exp = int(expression[position+1])
					expression = replace_values(expression, str(base ** exp), position-1,position+2)
		elif operator == "*":
			occurences = operator_in_expression(operator, expression)
			if occurences:
				for i in range(occurences):
					position = expression.index(operator)
					print position
					factor1 = int(expression[position-1])
					factor2 = int(expression[position+1])
					expression = replace_values(expression, str(factor1*factor2), position-1,position+2)
					print expression
		elif operator == "/":
			occurences = operator_in_expression(operator, expression)
			if occurences:
				for i in range(occurences):
					position = expression.index(operator)
					dividend = int(expression[position-1])
					divisor = int(expression[position+1])
					expression = replace_values(expression, str(dividend/divisor), position-1,position+2)
		elif operator == "%":
			occurences = operator_in_expression(operator, expression)
			if occurences:
				for i in range(occurences):
					position = expression.index(operator)
					dividend = int(expression[position-1])
					divisor = int(expression[position+1])
					expression = replace_values(expression, str(dividend/divisor), position-1,position+2)
		elif operator == "+":
			occurences = operator_in_expression(operator, expression)
			if occurences:
				for i in range(occurences):
					position = expression.index(operator)
					sum1 = int(expression[position-1])
					sum2 = int(expression[position+1])
					expression = replace_values(expression, str(sum1+sum2), position-1,position+2)
		elif operator == "-":
			occurences = operator_in_expression(operator, expression)
			if occurences:
				for i in range(occurences):
					position = expression.index(operator)
					diff1 = int(expression[position-1])
					diff2 = int(expression[position+1])
					expression = replace_values(expression, str(diff1-diff2), position-1,position+2)
	for i in range(len(expression)):
		expression[i] = int(expression[i])
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
				comment.reply("""The answer is {0}!
				
----				
		
^^^bot ^^^by ^^^u/TheMetaphorer [^^^GitHub](http://github.com/TheMetaphorer/domymathbot) ^^^Version ^^^{1}
""".format(process_expression(expr), VERSION))
				time.sleep(10)
		except praw.exceptions.APIException as e:
			cooldown_time = [int(mins) for mins in str(e) if mins.isdigit()][0] * 60;
			print 'Rate limit reached. Waiting for {0} seconds...'.format(cooldown_time)
			time.sleep(cooldown_time)
			scan_subreddit(sub)
		
		except Exception:
			comment.reply("""Oops! There's something wrong! I can't solve this problem!
			
---

^^^bot ^^^by ^^^u/TheMetaphorer [^^^GitHub](http://github.com/TheMetaphorer/domymathbot) ^^^Version ^^^{0}
""".format(VERSION))
			time.sleep(10)
		
	
		
scan_subreddit('test')